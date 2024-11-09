import picamera # type: ignore
from time import sleep

camera = picamera.PiCamera()

class Camera:
    def start_recording(self, user_id:str, seconds:int):       
        camera.start_recording(f'{user_id}.h264')
        if seconds:
            sleep(seconds)
            self.end_recording()
    
    def end_recording(self):
        camera.stop_recording()