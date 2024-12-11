from RPi.GPIO import cleanup, setwarnings, setmode, BCM # type: ignore
import re
import random
import time

def generate_unique_id():
    timestamp = int(time.time() * 1000)
    random_number = random.randint(1000, 9999)
    return f"{timestamp}{random_number}"

def clean_text(text):
    filtered_text = re.sub(r'\W+', '', text)
    return filtered_text

def initialise_gpio_pins():
    setwarnings(False)
    cleanup()
    setmode(BCM)
    
def cleanup_gpio():
    cleanup()