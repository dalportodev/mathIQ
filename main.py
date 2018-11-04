import tensorflow as tf
from tensorflow import keras
import letterFinder
from pathlib import Path
import cv2

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
K.set_image_dim_ordering('th')

useUI = False


def main():
    my_file = Path("my_model.h5")
    (train_images, train_labels), (test_images, test_labels) = keras.datasets.mnist.load_data()

    #chris added
    train_images = train_images.reshape(train_images.shape[0], 1, 28, 28)
    test_images = test_images.reshape(test_images.shape[0], 1, 28, 28)

    train_images = train_images.astype('float32')
    test_images = test_images.astype('float32')

    model = ImageDataGenerator(rotation_range=90)
    model.fit(train_images)

    #train_images = train_images / 255.0
    #test_images = test_images / 255.0


    if my_file.exists():
        model = keras.models.load_model("my_model.h5")
        model.compile(optimizer=tf.train.AdamOptimizer(),
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
    else:
        model = keras.Sequential([
            keras.layers.Flatten(input_shape=(28, 28)),
            keras.layers.Dense(128, activation=tf.nn.relu),
            keras.layers.Dense(10, activation=tf.nn.softmax)
        ])

        model.compile(optimizer=tf.train.AdamOptimizer(),
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        model.fit(train_images, train_labels, epochs=5)
        model.save("my_model.h5")

    #test_loss, test_acc = model.evaluate(test_images, test_labels)
    #print('Test accuracy:', test_acc)

    trial_images = None
    if useUI:
        root = Tk()
        root.title("MathIQ")
        root.geometry("500x200")

        UI = MathIQGUI.UserInterface(root, model, postAnalysis)
        print(UI.file)
        root.mainloop()
    else:
        trial_images = letterFinder.img_to_array("IMG_6524.JPG")
        postAnalysis(model, trial_images)



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