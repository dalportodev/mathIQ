import cv2


def img_to_array(img_name):
    img = cv2.imread(img_name)

    sizer = 1.0
    height, width = img.shape[:2]
    while height * sizer > 1000 or width * sizer > 1000:
        sizer = sizer - 0.01

    img = cv2.resize(img, None, fx=sizer, fy=sizer)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 100, 200)

    _, contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rects = [cv2.boundingRect(c) for c in contours]
    individual_images = []
    rects.sort(key=lambda x: x[0])

    for rect in rects:
        x1, y1, x2, y2 = rect
        #cv2.rectangle(img, (x1, y1), (x1 + x2, y1 + y2), (0, 255, 0), 3)
        roi = img[y1:y1+y2, x1:x1+x2]
        height, width, chan = roi.shape
        if height != 0 and width != 0:
            roi = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA)
            roi = cv2.dilate(roi, (3, 3))
            #cv2.imshow("Test", roi)
            #cv2.waitKey(0)

            individual_images.append(roi)

    #print(img.shape[:2])
    #cv2.imshow("Test", img)
    #cv2.waitKey(0)

    return individual_images

