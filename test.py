import argparse

import cv2


def detect_face(img):
    # convert the test image to gray image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # load OpenCV face detector
    face_cas = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml")
    faces = face_cas.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=4)

    for x, y, w, h in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return img


parser = argparse.ArgumentParser(description="Simple System for recognizing someone")
group = parser.add_mutually_exclusive_group()
group.add_argument("--video-file", type=str, help="specify the path of the video file")
group.add_argument("--image-file", type=str, help="specify the path of the image file")
group.add_argument("--builtin-camera", action="store_true", help="use the bult-in camera (Real Time Mode)")
args = parser.parse_args()

if args.image_file is not None:
    # read image
    img = cv2.imread(args.image_file)

    # display both images
    cv2.imshow("Face Detection From Image", detect_face(img))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if args.builtin_camera:
    cap = cv2.VideoCapture(0)
    while True:
        check, frame = cap.read()
        cv2.imshow('Face Detection From Camera', detect_face(frame))
        key = cv2.waitKey(0)
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
