import cv2
import imutils

defaultThreshSettings = {
  "thresh": 50,
  "maxVal": 120,
  "erodeIteration": 10
}

class VideoCamera():
  def __init__(self, initThreshSettings = None):
    if initThreshSettings is None:
      self.threshSettings = defaultThreshSettings.copy()

  def getSettings(self):
    return self.threshSettings