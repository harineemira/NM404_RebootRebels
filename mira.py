import snappy
import os
import subprocess
import shutil
import csv

def CopyCsvMask(path):
    original = os.path.join(path+r"\target.data\vector_data\eez_v11.csv")
    target = os.path.join(path+r"\eez_v11.csv")
    shutil.copyfile(original, target)

def CsvToJSON(path):
    print('Generating GEOJSON')
    with open(path+r"\target.data\vector_data\ShipDetections.csv", newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        fields=['Ships','Geometry','X co-ordinate','Y co-ordinate','Latitude','Longitude','Width','Length','Style']
        with open('Final.csv', 'w', newline='') as csvfile2:
            spamwriter = csv.writer(csvfile2, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            next(csvfile)
            next(csvfile)
            spamwriter.writerow(fields)
            for rows in spamreader:
                spamwriter.writerow(rows)      
    os.system('cmd /c "csvjson --lat Latitude --lon Longitude --k Ships --crs EPSG:4269 --indent 4 Final.csv > final.json"')
    
def ImportVector(shapefilepath,source):
    print('Importing Vector')
    cmd=["gpt","Import-Vector","-PseparateShapes=false","-PvectorFile="+str(shapefilepath),source]
    subprocess.call(cmd)
    #gpt Import-Vector -PvectorFile=C:\Users\pahar\SAR\eez_v11.shp C:\Users\pahar\SAR\S1A_IW_GRDH_1SDV_20191004T011831_20191004T011856_029302_035471_E23D.zip

def LandSeaMask(maskcsv,source):
    print('Land-Sea-Mask')
    cmd=["gpt","Land-Sea-Mask","-Pgeometry="+str(maskcsv),"-PlandMask=false","-PshorelineExtension=10","-PuseSRTM=false",source]
    subprocess.call(cmd)
    #gpt Land-Sea-Mask -Pgeometry=Gulf_of_Trieste_seamask_UTM33_1 -PlandMask=false -PshorelineExtension=10 -PuseSRTM=false C:\Users\pahar\SAR\target.dim

def Calibration(source):
    print('Calibration')
    cmd=["gpt","Calibration",source]
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

    source=r"C:\Users\pahar\SAR\S1A_IW_GRDH_1SDV_20191004T011831_20191004T011856_029302_035471_E23D.zip"
    #source=input() Get path for source
    print(source)
    path=r"C:\Users\pahar\SAR"
    target=path+r"\target.dim"
    shapefilepath=r"C:\Users\pahar\SAR\eez_v11.shp"
    
    #Importing Vector .shp file 
    ImportVector(shapefilepath,source)
    print(target)
    
    #Copying CSV Mask to Python Parent Folder
    CopyCsvMask(path)
    maskcsv='eez_v11'
    
    #Perform Land Masking
    LandSeaMask(maskcsv,target)
    print(target) 
    
    Calibration(target) 
    print(target)
    
    AdaptiveThresholding(target)
    print(target)
    
    ObjectDiscrimination(target)
    print(target)
    
    CsvToJSON(path)    
    print('END')
    
if __name__=="__main__":
    main()