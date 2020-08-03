
import cv2 # for capturing videos
import math # for mathematical operations
import matplotlib.pyplot as plt #3.3.0
import pandas as pd
import tensorflow as tf #2.3.0
from keras.preprocessing import image # 2.4.3
import numpy as np
from keras.utils import np_utils
from skimage.transform import resize #0.17.2
from numpy import asarray
from PIL import ImageTk,Image
import skimage.io
import cv2
import csv
import numpy as np
from skimage.io import imread,imshow,imsave
import glob
import os
from keras.models import Sequential
from keras.applications.vgg16 import VGG16
from keras.layers import Dense, InputLayer, Dropout
from sklearn.model_selection import train_test_split
from keras.applications.vgg16 import preprocess_input

'''
data = pd.read_csv('mapping.csv')
X = [ ]     # creating an empty array
for img_name in data.Image_ID:
    img = plt.imread('' + img_name)
    X.append(img)  # storing each image in array X
X = np.array(X)    # converting list to array
y = data.Class
dummy_y = np_utils.to_categorical(y) 
image = []
for i in range(0,X.shape[0]):
    a = resize(X[i], preserve_range=True, output_shape=(224,224)).astype(int)      # reshaping to 224*224*3
    image.append(a)
X = asarray(image)

#X = preprocess_input(X, mode='tf')      # preprocessing the input data
tf.keras.applications.vgg16.preprocess_input(X, data_format=None)

X_train, X_valid, y_train, y_valid = train_test_split(X, dummy_y, test_size=0.3, random_state=42)    # preparing the validation set


base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
X_train = base_model.predict(X_train)
X_valid = base_model.predict(X_valid)
X_train.shape, X_valid.shape
X_train = X_train.reshape(206, 7*7*512)      # converting to 1-D
X_valid = X_valid.reshape(89, 7*7*512)
train = X_train/X_train.max()      # centering the data
X_valid = X_valid/X_train.max()
# i. Building the model
model = Sequential()
model.add(InputLayer((7*7*512,)))    # input layer
model.add(Dense(units=1024, activation='sigmoid')) # hidden layer
model.add(Dense(2, activation='softmax'))    # output layer
model.summary()
# ii. Compiling the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# iii. Training the model
model.fit(train, y_train, epochs=10, validation_data=(X_valid, y_valid))
model.save("sar_false_rate_detection_model.h5")
print("model done")



Image.MAX_IMAGE_PIXELS = None
lines = list()
im = Image.open('original.tiff')
#os.mkdir('data')

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
        
        im_crop.save('ship'+'{}.png'.format(i))
        
        data = imread('ship'+'{}.png'.format(i))
        data = data / data.max() #normalizes data in range 0 - 255
        data = 255 * data
        img = data.astype(np.uint8)
        imgResized=cv2.resize(img, (224,224))
        cv2.imwrite('data/ship'+'{}.png'.format(i),imgResized)
        i=i+1




inputFolder = 'data'
#os.mkdir('Resized')
i=0
for img in glob.glob(inputFolder + "/*.png"):
    image=cv2.imread(img)
    imgResized=cv2.resize(image, (224,224))
    #filename ="frame%d.jpg" % count;count+=1
    cv2.imwrite("Resized/ship%d.jpg" %i, imgResized)
    i +=1
    


        

     


        

a1=0
a=1
b=i
a=a-1
b=b
with open('test.csv', 'w') as csvoutput:
    writer = csv.writer(csvoutput)
    for i in range(a,b):
        if(a1==0):
            writer.writerow(['Image_ID'])
        else:
            writer.writerow(['Resized/ship'+str(i)+'.jpg'])
        a1=a1+1
df = pd.read_csv('test.csv')
df.to_csv('Resized/test.csv', index=False)

'''
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









       
































