import picamera # type: ignore
from time import sleep
import datetime

picam = picamera.PiCamera()

class Camera:
    def __init__(self):
        self.is_recording = False
        
    def start_recording(self, seconds:int, user_id:str = None):       
        file_name = datetime.datetime.now(datetime.timezone.utc).isoformat() if user_id else user_id
        file_name = f"{file_name}.h264"
        self.is_recording = True
        picam.start_recording(file_name)
        if seconds:
            sleep(seconds)
            self.end_recording()
            return file_name
    
    def end_recording(self):
        picam.stop_recording()
        self.is_recording = False