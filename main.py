import tensorflow as tf
from tensorflow import keras
import letterFinder
from pathlib import Path
import cv2

import numpy as np
import matplotlib.pyplot as plt


def format(img_array):
    result = []
    for img in img_array:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(gray, 200, 200)
        edged = cv2.resize(edged, (28, 28), interpolation=cv2.INTER_AREA)
        edged = cv2.dilate(edged, (3, 3))
        result.append(edged)
    return result


def main():
    my_file = Path("my_model.h5")
    (train_images, train_labels), (test_images, test_labels) = keras.datasets.mnist.load_data()
    train_images = train_images / 255.0
    test_images = test_images / 255.0

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

    test_loss, test_acc = model.evaluate(test_images, test_labels)
    print('Test accuracy:', test_acc)

    trial_images = letterFinder.img_to_array("digits2.jpg")
    predictions = model.predict(np.array(trial_images, 'float64'))
    count = 0
    for p in predictions:
        print(np.argmax(p))


if __name__ == "__main__":
    main()
