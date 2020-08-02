import snappy
import os
import subprocess
import shutil
import csv
import sys
from global_land_mask import globe
import numpy as np
import pandas as pd

def CopyCsvMask(path):
    original = os.path.join(path+r"\target.data\vector_data\eez_v11.csv")
    target = os.path.join(path+r"\eez_v11.csv")
    shutil.copyfile(original, target)

def CopyShp(path):
    with open(path+r"\target.data\vector_data\ShipDetections.csv", newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        fields=['Ships','Geometry','X co-ordinate','Y co-ordinate','Latitude','Longitude','Width','Length','Style']
        with open('final2.csv', 'w', newline='') as csvfile2:
            spamwriter = csv.writer(csvfile2, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            next(csvfile)
            next(csvfile)
            spamwriter.writerow(fields)
            for rows in spamreader:
                spamwriter.writerow(rows) 

def BorderCorrection():  
    lines = list()
    with open('final2.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        next(reader)
        for row in reader:
            lines.append(row)
            is_ocean = globe.is_ocean(float(row[4]),float(row[5]))
            if (is_ocean==False):        
                lines.remove(row)
    with open('mycsv.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)
    df = pd.read_csv('mycsv.csv')
    df.to_csv('output.csv', index=False)
    df.to_csv("output.csv", header=["Ships","Geometry","X co-ordinate","Y co-ordinate","Latitude","Longitude","Width","Length","Style"], index=False)
    f=pd.read_csv("output.csv")
    keep_col = ["Ships","Geometry","X co-ordinate","Y co-ordinate","Latitude","Longitude","Width","Length"]
    new_f = f[keep_col]
    new_f.to_csv("output.csv", index=False)

def ShipCategory():
    a=1
    b=-1
    with open('output.csv','r') as csvinput:
        with open('Final1.csv', 'w') as csvoutput:
            writer = csv.writer(csvoutput)
            for row in csv.reader(csvinput):
                b=b+1
                if(a!=1):
                    
                    if(float(row[6])>float(row[7])):
                        ar=float(row[7])
                    else:
                        ar=float(row[7])

                if(a==1):
                    a=a+1
                    writer.writerow(row+['Category','ID'])
                elif(ar<25):
                    writer.writerow(row+['Fishing_Ship',b])
                elif(ar>=25 and ar<=50):
                    writer.writerow(row+['Tugs_ship',b])
                elif(ar>=51 and ar<200):
                    writer.writerow(row+['Passenger_ship',b])
                elif(ar<=201):
                    writer.writerow(row+['Cargo_or_Tanker_ship',b])
    df = pd.read_csv('Final1.csv')
    df.to_csv('Final.csv', index=False)

def CsvToJSON():
    print('Generating GEOJSON')    
    os.system('cmd /c "csvjson --lat Latitude --lon Longitude --k Ships --crs EPSG:4269 --indent 4 Final.csv > final.json"')

def RemoveFiles():
    os.remove("Final1.csv")
    os.remove("final2.csv")
    os.remove("mycsv.csv")
    os.remove("output.csv")


def ImportVector(shapefilepath,source):
    print('Importing Vector')
    cmd=["gpt","Import-Vector","-PseparateShapes=false","-PvectorFile="+str(shapefilepath),source]
    subprocess.call(cmd)
    #gpt Import-Vector -PvectorFile=C:\Users\pahar\SAR\eez_v11.shp C:\Users\pahar\SAR\S1A_IW_GRDH_1SDV_20191004T011831_20191004T011856_029302_035471_E23D.zip

def LandSeaMask(source):
    print('Land-Sea-Mask')
    cmd=["gpt","Land-Sea-Mask","-PsourceBands=Intensity_VH","-PlandMask=false","-PuseSRTM=false","-Pgeometry=eez_v11","-PinvertGeometry=true","-PshorelineExtension=10",source]
    subprocess.call(cmd)
    #gpt Land-Sea-Mask -Pgeometry=Gulf_of_Trieste_seamask_UTM33_1 -PlandMask=false -PshorelineExtension=10 -PuseSRTM=false C:\Users\pahar\SAR\target.dim

def Calibration(source):
    print('Calibration')
    cmd=["gpt","Calibration","-PsourceBands=Intensity_VH",source]
    subprocess.call(cmd)
    
def AdaptiveThresholding(source):
    print('AdaptiveThresholding')
    cmd=["gpt","AdaptiveThresholding","-Ppfa=12.5","-PtargetWindowSizeInMeter=30",source]
    subprocess.call(cmd)
    
def ObjectDiscrimination(source):
    print('Object-Discrimination')
    cmd=["gpt","Object-Discrimination","-PminTargetSizeInMeter=30.0",source]
    subprocess.call(cmd)
    
def main():
      
    path1=r"C:\Users\pahar\SAR"
    path2=sys.argv[1]
    source=path1+'\\'+path2
    print(source)
    #source=r"C:\Users\pahar\SAR\S1A_IW_GRDH_1SDV_20191004T011831_20191004T011856_029302_035471_E23D.zip"
    
    path=r"C:\Users\pahar\SAR"
    target=path+r"\target.dim"
    shapefilepath=r"C:\Users\pahar\SAR\eez_v11.shp"
    
    #Importing Vector .shp file 
    ImportVector(shapefilepath,source)
    print(target)
    
    #Copying CSV Mask to Python Parent Folder
    CopyCsvMask(path)

    #Perform Land Masking
    LandSeaMask(target)
    print(target) 
    
    Calibration(target) 
    print(target)
    
    AdaptiveThresholding(target)
    print(target)
    
    ObjectDiscrimination(target)
    print(target)

    CopyShp(path)  
    BorderCorrection()
    ShipCategory()
    CsvToJSON()    
    RemoveFiles()
    print('END')
    
if __name__=="__main__":
    main()