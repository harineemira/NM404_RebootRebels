import os
import subprocess
import shutil
import csv
import cv2
import sys
import math
import glob
from global_land_mask import globe
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt #3.3.0
import tensorflow as tf #2.2.0
from keras.preprocessing import image # 2.4.3
from keras.utils import np_utils
from skimage.transform import resize #0.17.2
from numpy import asarray
from PIL import ImageTk,Image
import skimage.io
from skimage.io import imread,imshow,imsave
from keras.models import Sequential
from keras.applications.vgg16 import VGG16
from keras.layers import Dense, InputLayer, Dropout
from sklearn.model_selection import train_test_split
from keras.applications.vgg16 import preprocess_input
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS = None

def Plotting():
    img = Image.open('original.png')
    rgbimg = Image.new("RGBA", img.size)
    rgbimg.paste(img)
    rgbimg.save('mid.png')

    image = Image.open('mid.png')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('Roboto-Bold.ttf', size=9)
    name = 'Ship'
    color = 'rgb(255,255,0)'

    with open('Final.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        next(reader)
        for row in reader:
            (x,y)=(int(row[2]),int(row[3]))
            name = (' ID'+row[9]+','+'L:'+row[7]+','+'W:'+row[6]+','+row[8])
            draw.text((x,y), name, fill=color, font=font)
        image.save('last.png')   

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
    os.remove("final2.csv")
    os.remove("mycsv.csv")

def VGG():
    
    #############    spliting Part
    Image.MAX_IMAGE_PIXELS = None
    lines = list()
    im = Image.open('original.tiff')
    os.mkdir('data')

    with open('output.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        next(reader)
        i=1
        for row in reader:        
            lines.append(row)
            x=float(row[2])
            y=float(row[3])
            #print(x,y)
            im_crop = im.crop((x-20,y-20,x+20,y+20))        
            im_crop.save('data/ship'+'{}.png'.format(i))        
            data = imread('data/ship'+'{}.png'.format(i))
            data = data / data.max() #normalizes data in range 0 - 255
            data = 255 * data
            img = data.astype(np.uint8)
            imgResized=cv2.resize(img, (224,224))
            cv2.imwrite('data/ship'+'{}.png'.format(i),imgResized)
            i=i+1

    ################## RESIZE AND PNG TO JPG 

    inputFolder = 'data'
    os.mkdir('Resized')
    i=1
    for img in glob.glob(inputFolder + "/*.png"):
        image=cv2.imread(img)
        imgResized=cv2.resize(image, (224,224))
        #filename ="frame%d.jpg" % count;count+=1
        cv2.imwrite("Resized/ship%d.jpg" %i, imgResized)
        i +=1

    ################### CREATE CSV      
    import pandas as pd
    a1=0
    a=1
    b=i
    a=a-1
    b=b
    with open('Resized/test.csv', 'w') as csvoutput:
        writer = csv.writer(csvoutput)
        for i in range(a,b):
            if(a1==0):
                writer.writerow(['Image_ID'])
            else:
                writer.writerow(['Resized/ship'+str(i)+'.jpg'])
            a1=a1+1
    df = pd.read_csv('Resized/test.csv')
    df.to_csv('Resized/test.csv', index=False)

    test = pd.read_csv('Resized/test.csv')
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

    test_image = []
    for img_name in test.Image_ID:
        img = plt.imread('' + img_name)
        test_image.append(img)
    test_img = np.array(test_image)
    test_image = []
    for i in range(0,test_img.shape[0]):
        a = resize(test_img[i], preserve_range=True, output_shape=(224,224)).astype(int)
        test_image.append(a)
    test_image = np.array(test_image)
    tf.keras.applications.vgg16.preprocess_input(test_image, data_format=None)


    ############ LOADING MODEL.............
    model = tf.keras.models.load_model('sar_false_rate_detection_model.h5')
    model.layers[0].input_shape#(None, 224, 224, 3)
    test_image = base_model.predict(test_image)
    print(i+1)



    # converting the images to 1-D form
    test_image = test_image.reshape(i+1, 7*7*512)

    # zero centered images
    test_image = test_image/test_image.max()

    predictions = model.predict_classes(test_image)

    print("Number of false predictions", predictions[predictions==0].shape[0], "")
    print("Number of ships", predictions[predictions==1].shape[0], "")


    print("predicted outputs")
    rounded_predictions = model.predict_classes(test_image)

    print(rounded_predictions)

    #print(rounded_predictions.ndim)

    #################################### CSV 


    lines = list()
    a=-1

    #members= input("Please enter a member's name to be deleted.")
    with open('output.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
        
            lines.append(row)
            if(a!=-1):
                
                if(rounded_predictions[a] == 0):
                    #print(rounded_predictions[a])
                    lines.remove(row)
                
            a=a+1
    with open('output1.csv', 'w') as writeFile:
        writer = csv.writer(writeFile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer = csv.writer(writeFile)
        writer.writerows(lines)
    import pandas as pd
    df = pd.read_csv('output1.csv')
    df.to_csv('output1.csv', index=False)

    ################# DELETING CREATED FOLDERS
    shutil.rmtree('data')
    shutil.rmtree('Resized')


def ShipCategory():
    a=1
    ar=2
    ar1=1
    ar2=1
    b=0
    with open('output1.csv','r') as csvinput:
        with open('Final.csv', 'w' ,newline='') as csvoutput:
            writer = csv.writer(csvoutput, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for row in csv.reader(csvinput):
                if(a!=1):
                    if(float(row[6])>float(row[7])):
                        ar=float(row[6])
                        ar1=float(row[7])
                    else:
                        ar=float(row[7])
                        ar1=float(row[6])
                ar2=ar/ar1
                ar3="{:.2f}".format(ar2) 
                print(ar3)

                if(a==1):
                    a=a+1
                    writer.writerow(row+['Category','Size Ratio','ID'])
                elif(ar<25):
                    writer.writerow(row+['Fishing_Ship',ar3,b])
                elif(ar>25 and ar<=50):
                    writer.writerow(row+['Tugs_ship',ar3,b])
                elif(ar>50 and ar<=200):
                    writer.writerow(row+['Passenger_ship',ar3,b])
                elif(ar>200 and ar<=340):
                    writer.writerow(row+['Cargo_or_Tanker_ship',ar3,b])
                b=b+1

def CsvToJSON():
    print('Generating GEOJSON')    
    os.system('cmd /c "csvjson --lat Latitude --lon Longitude --k Ships --crs EPSG:4269 --indent 4 Final.csv > final.json"')

def RemoveFiles():
    os.remove("output.csv")
    os.remove("output1.csv")
    os.remove("mid.png")
    os.remove("eez_v11.csv")


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
    
def AdaptiveThresholding(source,minTargetSize,guardWindowSize,PFA):
    print('AdaptiveThresholding')
    cmd=["gpt","AdaptiveThresholding","-Ppfa="+PFA,"-PtargetWindowSizeInMeter="+minTargetSize,"-PguardWindowSizeInMeter="+guardWindowSize,source]
    print(cmd)
    subprocess.call(cmd)
    
def ObjectDiscrimination(source):
    print('Object-Discrimination')
    cmd=["gpt","Object-Discrimination","-PminTargetSizeInMeter=30.0",source]
    subprocess.call(cmd)
    
def TkinterInput():
    master=tk.Tk()
    def set_value():
        global minTargetSize,guardWindowSize,PFA
        minTargetSize=e1.get()
        guardWindowSize=e2.get()
        PFA=e3.get()
        print("Target Window Size(SET)",minTargetSize)
        print("Guard Window Size",guardWindowSize)
        print("PFA",PFA)
        master.destroy()
    tk.Label(master,text="Target Window Size").grid(row=0)
    tk.Label(master,text="Guard Window Size").grid(row=1)
    tk.Label(master,text="PFA").grid(row=2)
    e1 = tk.Entry(master)
    e2 = tk.Entry(master)
    e3 = tk.Entry(master)
    e1.insert(0,"30")
    e2.insert(0,"500.0")
    e3.insert(0,"12.5")
    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)
    tk.Button(master,text='Enter', command=set_value).grid(row=4,column=1,sticky=tk.W,pady=4)
    tk.mainloop()
    print("Target Window Size(TKINTER)",minTargetSize)
    print("Guard Window Size",guardWindowSize)
    print("PFA",PFA)
    return minTargetSize,guardWindowSize,PFA

def main(): 
    
    minTargetSize,guardWindowSize,PFA=TkinterInput()
    print("Target Window min",minTargetSize)
    print("Guard Window max",guardWindowSize)
    print("PFA",PFA)
    
    path1=r"C:\Users\pahar\SAR"
    path2=sys.argv[1]
    source=path1+'\\'+path2
    print(source)
        
    path=r"C:\Users\pahar\SAR"
    target=path+r"\target.dim"
    shapefilepath=r"C:\Users\pahar\SAR\eez_v11.shp"
    
    Importing Vector .shp file 
    ImportVector(shapefilepath,source)
    print(target)
    
    #Copying CSV Mask to Python Parent Folder
    CopyCsvMask(path)

    #Perform Land Masking
    LandSeaMask(target)
    print(target) 

    Calibration(target) 
    print(target)
    
    AdaptiveThresholding(target,minTargetSize,guardWindowSize,PFA)
    print(target)
    
    ObjectDiscrimination(target)
    print(target)

    CopyShp(path)  
    BorderCorrection()
    VGG()
    ShipCategory()
    Plotting()
    CsvToJSON()    
    RemoveFiles()
    Plotting()
    print('END')
    
if __name__=="__main__":
    main()
