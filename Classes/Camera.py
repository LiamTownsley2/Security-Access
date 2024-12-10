import picamera # type: ignore
from time import sleep
import datetime
import os
from AWS import S3

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
        
    def record_and_upload(self, seconds:int, id = None):
        file_name = self.start_recording(seconds)
        segmentation_path = id if id is not None else "non-identified"
        bucket_name, file_object = S3.upload_to_s3(file_name, f"cctv-footage/{segmentation_path}/{file_name}")
        os.remove(file_name)
        return [bucket_name, file_object]
