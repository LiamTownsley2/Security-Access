from mfrc522 import SimpleMFRC522
from GPIO_Pin import GPIO_Pin
from Camera import Camera
import Util
from Database import get_user_by_card

def validate_key(user, text):
    if not user: return False
    if not text == "secret": return False
    return True

class RFID_Reader:
    def __init__(self):
        self.reader = SimpleMFRC522()
        
    def read_key(self):
        print("Awaiting Key Presentation...")
        id, text = self.reader.read()
        filtered_text = Util.clean_text(text)
        
        user = get_user_by_card(id)
        is_valid = validate_key(user, filtered_text)
        print(f"*{'VALID' if is_valid else 'INVALID'} TAG READ* | ID: {id} | Text: {filtered_text}")
        print(f"\t{user}")
        if is_valid:
            green_led = GPIO_Pin(12) # The Green LED represents unlocking the door.
            green_led.enable(3)
        else:
            camera = Camera()
            camera.start_recording(id, 5)