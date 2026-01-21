import cv2

cap = cv2.VideoCapture("../assets/intro.mp4")

print("Opened:", cap.isOpened())

ret, frame = cap.read()
print("First frame read:", ret)

cap.release()

