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

def not_implemented():
    raise NotImplementedError

menu = [
    ("Toggle RFID Reader", start_reader),
    ("Add an Employee", not_implemented),
    ("Remove an Employee", not_implemented),
    ("Register a Keycard", not_implemented),
]

def main_menu():
        print("Welcome to the RFID App! Please select from the following options:")
        for idx, item in enumerate(menu):
            print(f"{idx + 1}. {item[0]}")

        selection = input("> ")
        try:
            menu[int(selection)][1]() # Execute Menu function
        except Exception as e:
            print(f"Error in selection: {e}")
if __name__ == "__main__":
    while True:
        main_menu()