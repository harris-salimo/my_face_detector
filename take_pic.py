import cv2

video = cv2.VideoCapture(0)
i = 0
while True:
    check, frame = video.read()
    cv2.imshow('Capturing', frame)
    while i < 3:
        cv2.imwrite(str(i)+".jpg", frame)
        i += 1
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
