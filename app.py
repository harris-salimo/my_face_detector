# -*- coding: utf-8 -*-
# import OpenCV module
import argparse
import os

import cv2

import numpy as np


# function to detect face
def detect_face(img):
    # convert the test image to gray image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # load OpenCV face detector
    face_cas = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml")
    faces = face_cas.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=4)

    # if no faces are detected then return image
    if len(faces) == 0:
        return None, None

    # extract the face
    (x, y, w, h) = faces[0]

    # return only the face part
    return gray[y: y + h, x: x + w], faces[0]


# this function will read all persons' training images, detect face #from each image
# and will return two lists of exactly same size, one list
def prepare_training_data(data_folder_path):
    # ------STEP-1--------
    # get the directories (one directory for each subject) in data folder
    dirs = os.listdir(data_folder_path)
    faces = []
    labels = []
    for dir_name in dirs:
        # our subject directories start with letter 's' so
        # ignore any non-relevant directories if any
        if not dir_name.startswith("s"):
            continue

        # ------STEP-2--------
        # extract label number of subject from dir_name
        # format of dir name = slabel
        # , so removing letter 's' from dir_name will give us label
        label = int(dir_name.replace("s", ""))

        # build path of directory containing images for current subject subject
        # sample subject_dir_path = "training-data/s1"
        subject_dir_path = data_folder_path + "/" + dir_name

        # get the images names that are inside the given subject directory
        subject_images_names = os.listdir(subject_dir_path)

        # ------STEP-3--------
        # go through each image name, read image,
        # detect face and add face to list of faces
        for image_name in subject_images_names:
            # ignore system files like .DS_Store
            if image_name.startswith("."):
                continue

            # build image path
            # sample image path = training-data/s1/1.pgm
            image_path = subject_dir_path + "/" + image_name

            # read image
            image = cv2.imread(image_path)

            # display an image window to show the image
            # cv2.imshow("Training on image...", image)
            # cv2.waitKey(100)

            # detect face
            face, rect = detect_face(image)

            # ------STEP-4--------
            # we will ignore faces that are not detected
            if face is not None:
                # add face to list of faces
                faces.append(face)

                # add label for this face
                labels.append(label)
                cv2.destroyAllWindows()
                cv2.waitKey(1)
    cv2.destroyAllWindows()
    return faces, labels


# let's first prepare our training data
# data will be in two lists of same size
# one list will contain all the faces
# and other list will contain respective labels for each face
print("Preparing data...")
faces, labels = prepare_training_data("training_data")
print("Data prepared")

# print total faces and labels
print("Total faces: ", len(faces))
print("Total labels: ", len(labels))

# create our LBPH face recognizer
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

# train our face recognizer of our training faces
face_recognizer.train(faces, np.array(labels))
face_recognizer.save("training.xml")
face_recognizer.read("training.xml")


# function to draw rectangle on image
# according to given (x, y) coordinates and
# given width and height
def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)


# function to draw text on give image starting from
# passed (x, y) coordinates.
def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)


# this function recognizes the person in image passed
# and draws a rectangle around detected face with name of the subject
def predict(test_img):
    # make a copy of the image as we don't want to chang original image
    img = test_img.copy()

    # detect face from the image
    face, rect = detect_face(img)

    # predict the image using our face recognizer
    id, conf = face_recognizer.predict(face)

    # get name of respective label returned by face recognizer
    label_text = str(labels[id])

    # draw a rectangle around face detected
    draw_rectangle(img, rect)

    # draw name of predicted person:
    draw_text(img, label_text, rect[0], rect[1] - 5)
    return img


# load test images
test_img = cv2.imread("test_data/test1.jpg")

# perform a prediction
predicted = predict(test_img)
print("Prediction complete")

# display both images
cv2.imshow("Face Recognition Test", predicted)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)
cv2.destroyAllWindows()
