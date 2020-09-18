import cv2 
import numpy as np

cap = cv2.VideoCapture("./somename.mp4")
frames = 0
count = 0
interval = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / 100
length = 0
while(cap.isOpened()):
        frames += 1
        ret, frame = cap.read()
        if frame is None:
                break
        if length <= frames :
                length += interval
                cv2.imwrite("./img/" + str(count).zfill(3) + ".jpg", frame)
                count += 1
cap.release()

