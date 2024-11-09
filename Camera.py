import picamera
from time import sleep

class Camera:
    def __init__(self):
        self.camera = picamera.PiCamera()
    
    def start_recording(self, user_id:str, seconds:int):
        self.camera.start_recording(f'{user_id}.h264')
        if seconds:
            sleep(seconds)
            self.end_recording()
    
    def end_recording(self):
        self.camera.stop_recording()