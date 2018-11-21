
import tensorflow as tf
from tensorflow import keras
import letterFinder
from pathlib import Path
import cv2
import os

import MathIQGUI
#this might be a compatibility issue between windows and linux environemnts
#The line below I ad
#from Tkinter import*
import tkinter as tk

import numpy as np

 
#chris added
from keras.preprocessing.image import ImageDataGenerator
from matplotlib import pyplot
from keras import backend as K
from keras.datasets import mnist
K.set_image_dim_ordering('th')

useUI = True
trainModel=False


def main():
    my_file = Path("my_model.h5")
    (train_images, train_labels), (test_images, test_labels) = mnist.load_data()

    #train_dict = {}
    #for c in os.listdir("extracted_images"):
    #    temp_array = []
    #    if os.path.isdir("extracted_images/" + c):
    #        print("Reading " + c + "...")
    #        for i in os.listdir("extracted_images/" + c):
    #            temp_array.append(cv2.imread("extracted_images/" + c + "/" + i))
    #        train_dict[c] = temp_array

    train_images = train_images / 255.0
    test_images = test_images / 255.0

    #chris added
    #train_images = train_images.reshape(train_images.shape[0], 1, 28, 28)
    #test_images = test_images.reshape(test_images.shape[0], 1, 28, 28)

    #train_images = train_images.astype('float32')
    #test_images = test_images.astype('float32')

    #model = ImageDataGenerator(rotation_range=90)
    #model.fit(train_images)
    #model = ImageDataGenerator(featurewise_center=True, featurewise_std_normalization=True)
   # model.fit(train_images)
    #model = ImageDataGenerator(zca_whitening=True)
   #model.fit(train_images)
    #model = ImageDataGenerator(rotation_range=90)
    #model.fit(train_images)
    #model = ImageDataGenerator(width_shift_range=shift, height_shift_range=shift)
    #model.fit(train_images)
    #model = ImageDataGenerator(horizontal_flip=True, vertical_flip=True)
    #model.fit(train_images)



    if trainModel == True:
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True)

        test_datagen = ImageDataGenerator(rescale=1./255)

        train_generator = train_datagen.flow_from_directory(
            directory=r"./extracted_images",
            target_size=(28, 28),
            color_mode="rgb",
            batch_size=32,
            class_mode="binary",
            shuffle=True,
            seed=42)
        validation_generator = test_datagen.flow_from_directory(
            directory=r"./extracted_images",
            target_size=(28, 28),
            color_mode="rgb",
            batch_size=32,
            class_mode="binary",
            shuffle=True,
            seed=42)

    
    if my_file.exists():
        model = keras.models.load_model("my_model.h5")
        model.compile(optimizer=tf.train.AdamOptimizer(),
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])
    else:
        #model = keras.Sequential([
        #    keras.layers.Flatten(input_shape=(28, 28)),
        #    keras.layers.Dense(128, activation=tf.nn.relu),
        #    keras.layers.Dense(82, activation=tf.nn.softmax)
        #])
        model = keras.Sequential()
        model.add(keras.layers.Conv2D(32, (3,3), input_shape = (3, 28, 28), activation = 'relu'))
        model.add(keras.layers.Flatten())
        model.add(keras.layers.Dense(129, activation=tf.nn.relu))
        model.add(keras.layers.Dense(82, activation=tf.nn.softmax))

        model.compile(optimizer=tf.train.AdamOptimizer(),
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])
        #model.fit(train_images, train_labels, epochs=5)
        #for symb in train_dict:

         #   temp_array = []
         #   imgs = train_dict[symb]

         #   if symb == "0":
         #       count = 0
         #       while count < count(imgs):
         #           temp_array.append(0)
         #           count += 1
         #       model.fit(np.array(imgs, 'float64'), np.array(temp_array), epochs=5)




        model.fit_generator(
		        train_generator,
		        steps_per_epoch=2000,
		        epochs=5,
		        validation_data=validation_generator,
		        validation_steps=800,
                workers=8)
        model.save("my_model.h5")


    #test_loss, test_acc = model.evaluate(test_images, test_labels)
    #print('Test accuracy:', test_acc)

    trial_images = None
    if useUI:
        UI = MathIQGUI.UserInterface(model)

    else:
        trial_images = letterFinder.img_to_array("IMG_6524.JPG")
        #postAnalysis(model, trial_images)
        print(model.evaluate_generator(generator=validation_generator, steps=1000, workers=4))
        print(train_generator.class_indices)


def postAnalysis(model, trial_images):
    for i in trial_images:
        cv2.imshow("Make Sure These All Look Right", i)
        cv2.waitKey(0)
    predictions = model.predict(np.array(trial_images.copy(), 'float64'))

    count = 0
    trial_labels = []
    while count < len(predictions):
        print("This is my prediction: ", np.argmax(predictions[count]))
        actual = input("What is it supposed to be? ->")
        trial_labels.append(actual)
        count += 1

    model.fit(np.array(trial_images.copy(), 'float64'), np.array(trial_labels), epochs=5)


if __name__ == "__main__":
    main()