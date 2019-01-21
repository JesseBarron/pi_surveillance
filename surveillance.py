from main import app
import cv2
import boto3
import time
from time import sleep
from os import getcwd


cam = cv2.VideoCapture(0)

if app['config'].DEBUG == True:
    cam.set(3, 1280)
    cam.set(4, 1024)
    sleep(2)
    cam.set(10, 12)
    cam.set(15, 18.0)

ret, image = cam.read()

if ret:
    cv2.imshow("Snapshot test", image)
    sleep(2)
    cv2.waitKey(0)
    cv2.destroyWindow('Snapshot test')

    cwd = getcwd()
    imageName = 'test_image' + str(time.time()) + '.jpg'
    pathToCap = cwd + '/test_images/' + imageName

    cv2.imwrite(pathToCap, image)

print("Image Captured!")
cam.release()
