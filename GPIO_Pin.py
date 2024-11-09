import RPi.GPIO as GPIO # type: ignore
from time import sleep

class GPIO_Pin:
    def __init__(self, id:int):
        self.state = False
        self.id = id
        GPIO.setup(self.id, GPIO.OUT)
        
    def enable(self, seconds:int):
        GPIO.output(self.id, GPIO.HIGH)
        self.state = True
        if seconds:
            sleep(seconds)
            self.disable()
    
    def disable(self):
        GPIO.output(self.id, GPIO.LOW)
        self.state = False