from flask import Blueprint
from camera import VideoCamera

camera_controller = Blueprint('camera_controller', __name__)

camSing = VideoCamera()

@camera_controller.route('/')
def inIndex():
  return "INDEX OF CAMERA"
  
@camera_controller.route('/start')
def startCam():
  return "Starting Camera"

@camera_controller.route('/checkDefaultSettings')
def check():
  print(camSing.getSettings())
  return "There it is"