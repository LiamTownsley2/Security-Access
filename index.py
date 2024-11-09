#!/usr/bin/env python
import Util
from RFID_Reader import RFID_Reader

Util.initialise_gpio_pins()

def start_reader():
    try:
        rfid_reader = RFID_Reader()
        while True:
            rfid_reader.read_key()
    finally:
        Util.cleanup_gpio()

if __name__ == "__main__":
    start_reader()