from flask import Flask
from camera.index import camera_controller
app = Flask(__name__)

# Registering Blueprints
app.register_blueprint(camera_controller, url_prefix='/api/camera')


@app.route('/')
def hello_world():
  return "Hello World!"
