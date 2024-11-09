from RPi.GPIO import cleanup, setwarnings, setmode, BCM # type: ignore
import re

def clean_text(text):
    filtered_text = re.sub(r'\W+', '', text)
    return filtered_text

def initialise_gpio_pins():
    setwarnings(False)
    cleanup()
    setmode(BCM)
    
def cleanup_gpio():
    cleanup()