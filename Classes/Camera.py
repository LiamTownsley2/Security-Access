import picamera # type: ignore
from time import sleep
import datetime

picam = picamera.PiCamera()

class Camera:
    def __init__(self):
        self.is_recording = False
        
    def start_recording(self, seconds:int):       
        if self.is_recording:
            raise Exception("Camera is already recording")
        file_name = f"{datetime.datetime.now(datetime.timezone.utc).isoformat()}.h264"
        self.is_recording = True
        picam.start_recording(file_name)
        if seconds:
            sleep(seconds)
            self.end_recording()
            return file_name
    
    def end_recording(self):
        picam.stop_recording()
        self.is_recording = False