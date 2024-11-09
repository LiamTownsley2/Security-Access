import picamera # type: ignore
from time import sleep

camera = None

class Camera:
    def __init__(self):
        global camera
        if camera is None:
            camera = picamera.PiCamera()

    def __del__(self):
        global camera
        camera = None

    def start_recording(self, user_id:str, seconds:int):
        if camera is None:
            raise ValueError("Camera not initialised.")
        
        camera.start_recording(f'{user_id}.h264')
        if seconds:
            sleep(seconds)
            self.end_recording()
    
    def end_recording(self):
        if camera is None:
            raise ValueError("Camera not initialised.")
        
        camera.stop_recording()