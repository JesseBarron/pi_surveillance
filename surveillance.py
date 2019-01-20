import cv2
import boto3
from time import sleep

cam = cv2.VideoCapture(0)
cam.set(3, 1280)
cam.set(4, 1024)
sleep(2)
cam.set(15, -8.0)
ret, image = cam.read()

if ret:
    cv2.imshow("Snapshot test", image)
    sleep(2)
    cv2.waitKey(0)
    cv2.destroyWindow('Snapshot test')
    cv2.imwrite('/home/jesse/Desktop/testing.jpg', image)
cam.release()
