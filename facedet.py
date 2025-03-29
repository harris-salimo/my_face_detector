# -*- coding: utf-8 -*-
import cv2

# read image
img = cv2.imread("test_data/test0.jpg")

# convert the test image to gray image
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# load OpenCV face detector
face_cas = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml")
faces = face_cas.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=4)

for x, y, w, h in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

# display both images
cv2.imshow("Face Detection Test", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
