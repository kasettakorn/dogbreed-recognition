# -*- coding: utf-8 -*-
"""Dog breed Recognition.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1E6xlsMvoFWIMwOUpZQdyMGwA0tiVE4A_
"""

!git clone https://github.com/kasettakorn/dogbreed-recognition.git

from keras.preprocessing import image
import os
import cv2
import numpy as np


images = []
labels = []
type_label = []

def load_dataset(folder):
  type_label.append(folder.split('.')[1])
  for filename in os.listdir(folder):
    try:
      img = cv2.imread(os.path.join(folder, filename))
      img = cv2.resize(img, (300,300))
      img = image.img_to_array(img)
      images.append(img)
      labels.append(folder.split(os.path.sep)[-1].split('.')[1])
    except:
      continue

for folder in sorted(os.listdir('/content/dogbreed-recognition/datasets/train')):
  if folder == '031.Borzoi':
    break
  load_dataset('/content/dogbreed-recognition/datasets/train/' + folder)
print("Finish")
print(type_label)

x = np.array(images)/255
y = np.array(labels)
print(x.shape)
print(y.shape)

from sklearn.preprocessing import LabelEncoder, OneHotEncoder
#integer encoder
integer_encoded = LabelEncoder().fit_transform(y)
integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
print(integer_encoded.shape)

#One hot encoding (binary encoded)
onehot_encoder = OneHotEncoder(sparse=False).fit_transform(integer_encoded)
y = np.array(onehot_encoder)

from sklearn.model_selection import train_test_split

(x_train, x_test, y_train, y_test) = train_test_split(x, y, test_size=0.15, random_state=42)

print(x_train.shape)
print(x_test.shape)
print(y_train.shape)
print(y_test.shape)

#Convolution NN
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Activation
from keras.models import Sequential

n_classes = len(type_label)

model = Sequential()
model.add(Conv2D(16, (3, 3), input_shape=(300,300,3), activation='relu'))
model.add(MaxPooling2D(pool_size = (3, 3)))
model.add(Activation('relu'))


model.add(Conv2D(32, (3, 3) ,activation='relu'))
model.add(MaxPooling2D(pool_size = (3, 3)))


model.add(Conv2D(70, (3, 3) ,activation='relu'))
model.add(MaxPooling2D(pool_size = (3, 3)))

model.add(Conv2D(70, (3, 3) ,activation='relu'))
model.add(Conv2D(120, (3, 3) ,activation='relu'))
model.add(Conv2D(64, (3, 3) ,activation='relu'))
model.add(MaxPooling2D(pool_size = (3, 3)))



model.add(Flatten())
model.add(Dense(150, activation='relu'))
model.add(Dense(80, activation='relu'))
model.add(Dense(40, activation='relu'))
model.add(Dense(n_classes, activation='softmax'))

model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')
print(model.summary())

import sys
from numpy import load
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from keras import backend
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten
from keras.optimizers import SGD
from keras.applications.vgg16 import VGG16
from keras.models import Model



def define_modelVGG(in_shape=(300, 300, 3), out_shape = len(type_label)):     ## class number 
    model = VGG16(include_top = False, weights='imagenet', input_shape = in_shape)
    
    for layer in model.layers:
        layer.trainable = False     
        
    model.get_layer('block5_conv1').trainable = True
    model.get_layer('block5_conv2').trainable = True
    model.get_layer('block5_conv3').trainable = True
    model.get_layer('block5_pool').trainable = True
    
    flat1 = Flatten()(model.layers[-1].output)
    class1 = Dense(128, activation = 'relu', kernel_initializer = 'he_uniform')(flat1)
    output = Dense(out_shape, activation='sigmoid')(class1)
    model = Model(inputs = model.inputs, outputs = output)
    
    model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')
    return model

model = define_modelVGG()

history = model.fit(x_train, y_train, batch_size = 32, epochs = 40)                              
model.save('dog_model.h5')

#@title
score = model.evaluate(x_test, y_test, verbose=0)
print(model.metrics_names)
print(score)

from keras.models import load_model
#import user folder
images = []
load_dataset('/content/dogbreed-recognition/datasets/valid/001.Affenpinscher')
x = np.array(images)/255

#load model
h5model = load_model('/content/dog_model.h5')
y_model = h5model.predict(x)
print(type_label)
score_model = h5model.evaluate(x_test, y_test, verbose=0)
print("Accuracy: ", score_model[0]*100, "%")

import matplotlib.pyplot as plt
fig=plt.figure(figsize=(30,30))
for i in range(4):
  ax=fig.add_subplot(1,len(x),i+1) 
  ax.imshow(cv2.cvtColor(x[i], cv2.COLOR_BGR2RGB))
  plt.title("Predicted: {}".format(type_label[np.argmax(y_model[i])]), fontdict={'fontsize': 17, 'color': 'white'})
  plt.axis('off')
plt.show()