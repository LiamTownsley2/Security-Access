from mfrc522 import SimpleMFRC522
from GPIO_Pin import GPIO_Pin
from Camera import Camera
import Util

def validate_key(id, text):
    filtered_text = Util.clean_text(text)
    is_valid = filtered_text == "secret"
    print(f"*{'VALID' if is_valid else 'INVALID'} TAG READ* | ID: {id} | Text: {filtered_text}")
    return is_valid

class RFID_Reader:
    def __init__(self):
        self.reader = SimpleMFRC522()
        
    def read_key(self):
        print("Awaiting Key Presentation...")
        id, text = self.reader.read()
        is_valid = validate_key(id, text)
        camera = Camera()

        if is_valid:
            green_led = GPIO_Pin(12) # The Green LED represents unlocking the door.
            green_led.enable(3)
        else:
            camera.start_recording(id, 5)