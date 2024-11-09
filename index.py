#!/usr/bin/env python
from mfrc522 import SimpleMFRC522
from GPIO_Pin import GPIO_Pin
from Camera import Camera
import Util

rfid_reader = SimpleMFRC522()
Util.initialise_gpio_pins()

def start_reader():
    try:
        id, text = rfid_reader.read()
        camera = Camera()
        filtered_text = Util.clean_text(text)
        is_valid = filtered_text == "secret"
        
        print(f"*{'VALID' if is_valid else 'INVALID'} TAG READ* | ID: {id} | Text: {filtered_text}")
        
        if is_valid:
            green_led = GPIO_Pin(12) # The Green LED represents unlocking the door.
            green_led.enable(3)
        else:
            camera.start_recording(id, 5)
    finally:
        Util.cleanup_gpio()

if __name__ == "__main__":
    start_reader()