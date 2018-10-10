import cv2
import PIL.ImageOps
import numpy
from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import math
from skimage.feature import hog


def img_to_array(img_name):
    img = cv2.imread(img_name)
    img = cv2.resize(img, None, fx=.3, fy=.3)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 100, 200)

    _, contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rects = [cv2.boundingRect(c) for c in contours]
    individual_images = []

    for rect in rects:
        x1, y1, x2, y2 = rect
        cv2.rectangle(img, (x1, y1), (x1 + x2, y1 + y2), (0, 255, 0), 3)
        roi = edged[y1:y1+y2, x1:x1+x2]
        height, width = roi.shape
        if height != 0 and width != 0:
            roi = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA)
            roi = cv2.dilate(roi, (3, 3))

            individual_images.append(roi)


    cv2.imshow("test", img)
    c = cv2.waitKey(0)
    if 'q' == chr(c & 255):
        QuitProgram()
    return individual_images


