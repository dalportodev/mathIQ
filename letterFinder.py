import cv2
import PIL.ImageOps
import numpy
from imutils.perspective import four_point_transform
from imutils import contours
import imutils


img = cv2.imread("digits.jpg")
img = cv2.resize(img, None, fx=1.5, fy=1.5)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 11, 17, 17)
edged = cv2.Canny(gray, 200, 200)
img2, contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
avg_area = 0
for c in contours:
    avg_area = avg_area + cv2.contourArea(c)
for c in contours:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    x, y, w, h = cv2.boundingRect(approx)
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 1)
cv2.imshow("Boxes", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
