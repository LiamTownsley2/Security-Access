#!/usr/bin/env python
import Util
from Classes.RFID_Reader import RFID_Reader
import Database as DB
from Classes.GPIO_Pin import GPIO_Pin
from Classes.Camera import Camera
from bson.objectid import ObjectId
from Encryptor import generate_master_password

Util.initialise_gpio_pins()
DB.connect_to_database()
rfid_reader = RFID_Reader()

def validate_key(user, text):
    if not user: return False
    if not text == "secret": return False
    return True

def start_reader():
    try:
        while True:
            id, text = rfid_reader.read_key()
            user = DB.get_user_by_card(id)
            is_valid = validate_key(user, text)
            print(f"*{'VALID' if is_valid else 'INVALID'} TAG READ* | ID: {id} | Text: {text}")
            print(f"\t{user}")
            if user and user['_id']:
                DB.register_entry(str(id), user['_id'])

            if is_valid:
                green_led = GPIO_Pin(12) # The Green LED represents unlocking the door.
                green_led.enable(3)
            else:
                camera = Camera()
                camera.start_recording(id, 5)
    except KeyboardInterrupt:
        print("\n\nReturning to Main Menu.\n\n")

def add_user():
    try:
        employee_name = input("What is this employee's FULL LEGAL name?\n> ")
        master_password = generate_master_password()
        user = DB.register_user(employee_name, generate_master_password())
        select_key_registration = input("Would you like to register a keycard at this time? (Y/n)\n> ")
        if select_key_registration == "" or "y" in select_key_registration.lower():
            register_keycard(user.inserted_id)
    except KeyboardInterrupt:
        print("\n\nReturning to Main Menu.\n\n")

def remove_user():
    try:
        employee_id = input("What is the employee's ID?\n> ")
        DB.delete_user(ObjectId(employee_id))
    except KeyboardInterrupt:
        print("\n\nReturning to Main Menu.\n\n")
    except Exception as e:
        print(f"\nThere was an error whilst removing this employee!\n{e}\n")

def register_keycard(employee_id = None):
    if employee_id is None:
            employee_id = input("What is the employee's ID?\n> ")
    
    id, _ = rfid_reader.read_key()
    users_holding_card = DB.get_users_by_card(str(id))
    if len(users_holding_card) > 0:
        DB.remove_all_links_to_card(id)
    
    DB.register_card_to_user(ObjectId(employee_id), str(id))
    return print("Card Registration Successful!")

def not_implemented():
    raise NotImplementedError

menu = [
    ("Toggle RFID Reader", start_reader),
    ("Add an Employee", add_user),
    ("Remove an Employee", remove_user),
    ("Register a Keycard", register_keycard),
]

def main_menu():
        print("Welcome to the RFID App! Please select from the following options:")
        for idx, item in enumerate(menu):
            print(f"{idx + 1}. {item[0]}")

        selection = input("> ")
        try:
            menu[int(selection) - 1][1]() # Execute Menu function
        except Exception as e:
            print(f"Error in selection: {e.with_traceback(e.__traceback__)}\n")
            
if __name__ == "__main__":
    try:
        while True:
            main_menu()
    except KeyboardInterrupt:
        print("Goodbye.")
    finally:
        Util.cleanup_gpio()