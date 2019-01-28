from imutils.video import VideoStream
import platform
import argparse
import datetime
import imutils
import time
import cv2

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="Path to the video")
ap.add_argument("-a", "--min-area", type=int, default=500, help="Minimum area size")

# Two methods are happening here
# ap.parse_args() this returns a "namespace" object, this is sort of like an object in js. it holds variables props
# and other methods of a given scope. in this case it extracts the arguments in the ArgumentParser.
# ( This is a method that belongs to the ArgumentParser() class )

# vars this extracts the proper arguments from a namespace, in this case Video and min-area from the argument parser
#(Native Python method)
args = vars(ap.parse_args())

#
# Working good example of values I could use
# thresh: 48
# maxVal: 120
# erodeIterations: 2
# 
# Threshold passes values if they're bright enough, if a pixles is part of a bigger cluster it will be passed as well
# erosion dictates how big the clusters of pixles can be 
#

controlValDefaults = {
  "thresh": 50,
  "maxVal": 120,
  "erodeIteration": 10
}

controlledVal = controlValDefaults.copy()
i = -1

# if the video argument is None, then we are reading from webcam
if args.get('video', None) is None:
  vs = VideoStream(src=0)

  # if Mac set these properties to make the picture visible
  if platform.system() == 'Darwin':
    print("Setting Video Stream props")
    vs.stream.stream.set(3, 1280)
    vs.stream.stream.set(4, 1024)
    vs.stream.stream.set(10, 12)
    vs.stream.stream.set(15, 18.0)

  # This lets the camera turn on and adjust itself to capture images
  time.sleep(2.0)
  vs.start()

# otherwise, we are reading from a video file
else:
  vs = cv2.VideoCapture(args["video"])

# initialize the first frame in the video stream
firstFrame = None

# loops over the frames of the video or webcam

while True:
  # Grab the current frame and initialize the occupied/unoccupied
  # Initialize 'Unoccupied' text
  frame = vs.read()
  frame = frame if args.get('video', None) is None else frame[1]
  text = "Unoccupied"

  # If frame could be grabbed then we've reached the end of the video
  if frame is None:
    break

  frame = imutils.resize(frame, width=500) # resizes the frame width to 500px
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Gray scale the images
  gray = cv2.GaussianBlur(gray, (21, 21), 0) # blur the images to smooth out the pixels

  # If the firstFrame is not there then we're going to repeat the loop with 
  # firsFrame assigned as gray, so the next round we can make a comparison

  if firstFrame is None:
    firstFrame = gray
    continue

  # Check the difference between the firstFrame and frame
  frameDelta = cv2.absdiff(firstFrame, gray) # Get the difference between firstFrame and currentFrame(gray)
  thresh = cv2.threshold(frameDelta, controlledVal['thresh'], controlledVal['maxVal'], cv2.THRESH_BINARY)[1] # returns a corse black and white image that exaggerates the difference
  # thresh = cv2.adaptiveThreshold(frameDelta, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY+cv.THRESH_OTSU, 23, 2)

  # Diealate the image (fill in any holes) find the contours of the threshold image
  thresh = cv2.erode(thresh, None, iterations=controlledVal['erodeIteration'])
  cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  cnts = imutils.grab_contours(cnts)

  for c in cnts:
    # if cntrs are too small ignore it
    area = args.get('min-area') if args.get('min-area') is int else 500
    if cv2.contourArea(c) < area:
      continue
    # Compute the bounding box for contour, draw it on frame, and update text

    (x, y, w, h) = cv2.boundingRect(c)
    cv2.rectangle(frame, ( x, y ), ( x +  w, y + h ), ( 0, 255, 0 ), 2)
    text = "Occupied"

  cv2.imshow('Test Frame', frame)
  cv2.imshow('Test Delta', frameDelta)
  cv2.imshow('Thresh Test', thresh)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
  elif cv2.waitKey(1) & 0xff == ord('r'):
    print("reseting firstFrame")
    firstFrame = gray
  elif cv2.waitKey(1) & 0xff == 32:
    i += 1
    if i > len(controlledVal) - 1:
      i = 0
    print("Print Option")
    print(list(controlledVal.keys())[i])
  elif cv2.waitKey(1) & 0xff == 0:
    print("Incrementing Settings")
    print(list(controlledVal.keys())[i])
    controlledVal[list(controlledVal.keys())[i]] += 1
    print(controlledVal[list(controlledVal.keys())[i]])
  elif cv2.waitKey(1) & 0xff == 1:
    print("Reducing Settings")
    print(list(controlledVal.keys())[i])
    controlledVal[list(controlledVal.keys())[i]] -= 1
    print(controlledVal[list(controlledVal.keys())[i]])
  elif cv2.waitKey(1) & 0xff == ord('o'):
    controlledVal = controlValDefaults.copy()
    print(controlledVal)