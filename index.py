#!/usr/bin/env python
import Util
from RFID_Reader import RFID_Reader
from Database import connect_to_database

Util.initialise_gpio_pins()
connect_to_database()
def start_reader():
    try:
        rfid_reader = RFID_Reader()
        while True:
            rfid_reader.read_key()
    finally:
        Util.cleanup_gpio()

if __name__ == "__main__":
    start_reader()