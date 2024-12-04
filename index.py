#!/usr/bin/env python
from dotenv import load_dotenv
load_dotenv()

import curses
import threading
import logging
import Util

from Classes.RFID_Reader import RFID_Reader
from AWS import DynamoDB, S3
from Classes.GPIO_Pin import GPIO_Pin
from Classes.Camera import Camera

Util.initialise_gpio_pins()
rfid_reader = RFID_Reader()

thread_logger = logging.getLogger("ThreadLogger")
thread_logger.setLevel(logging.INFO)
thread_file_handler = logging.FileHandler("thread_reader.log")
thread_file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
thread_logger.addHandler(thread_file_handler)

def validate_key(user, text):
    if not user: return False
    if not text == "secret": return False
    return True

def start_reader():
    try:
        while True:
            thread_logger.info("start_reader() running.")
            id, text = rfid_reader.read_key()
            thread_logger.info(f"Card Read: ({id}) {text}")
            user = DynamoDB.get_user_by_card(str(id))
            print(f"\t {user}")
            is_valid = validate_key(user, text)
            thread_logger.info(f"Key Valid: {is_valid}")
            thread_logger.info(f"*{'VALID' if is_valid else 'INVALID'} TAG READ* | ID: {id} | Text: '{text}'")
            if is_valid:
                DynamoDB.register_entry(str(id), user['UserID'])
                entries = DynamoDB.get_entries_count(user['UserID'])
                thread_logger.info(f"You have entered this building {entries} time(s) before.")
                green_led = GPIO_Pin(12) # The Green LED represents unlocking the door.
                green_led.enable(3)
            else:
                camera = Camera()
                file_name = camera.start_recording(id, 5)
                upload_url = S3.upload_to_s3(file_name, "cmp408-cctv-recordings", f"cctv-footage/{file_name}")
                thread_logger.info(f"S3 Upload Link: {upload_url}")
    except Exception as e:
        thread_logger.error(e)


def add_user(stdscr):
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Enter full name of the Employee (or type 'back' to return):")
        stdscr.refresh()

        curses.echo()
        employee_name = stdscr.getstr(1, 0, 20).decode("utf-8").strip()
        
        if employee_name.lower() == "back":
            stdscr.clear()
            stdscr.addstr(0, 0, "Returning to the main menu...")
            stdscr.refresh()
            curses.napms(1000)
            break
        
        try:
            user = DynamoDB.register_user(employee_name)
            select_key_registration = input("Would you like to register a keycard at this time? (Y/n)\n> ")
            if select_key_registration == "" or "y" in select_key_registration.lower():
                register_keycard(user)
        
            stdscr.clear()
            stdscr.addstr(0, 0, f"Employee '{employee_name}' added successfully!")
        except:
            stdscr.clear()
            stdscr.addstr(0, 0, f"There was an issue whilst adding '{employee_name}'! Please try again.")
        finally:
            stdscr.refresh()
            curses.napms(3000)
            break

def remove_user(stdscr):
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Enter the ID of the Employee that should be removed (or type 'back' to return):")
        stdscr.refresh()

        curses.echo()
        employee_id = stdscr.getstr(1, 0, 20).decode("utf-8").strip()
        
        if employee_id.lower() == "back":
            stdscr.clear()
            stdscr.addstr(0, 0, "Returning to the main menu...")
            stdscr.refresh()
            curses.napms(1000)
            break
        
        try:
            DynamoDB.delete_user(employee_id)
            stdscr.clear()
            stdscr.addstr(0, 0, f"User '{employee_id}' removed successfully!")
        except:
            stdscr.clear()
            stdscr.addstr(0, 0, f"There wasan issue whilst deleting '{employee_id}'! Please try again.")
        finally:
            stdscr.refresh()
            curses.napms(3000)
            break        
def register_keycard(stdscr, employee_id=None):
    while True:
        while employee_id is None:
            stdscr.clear()
            stdscr.addstr(0, 0, "Enter the Employee's ID (or type 'back' to return):")
            stdscr.refresh()

            curses.echo()
            _employee_id = stdscr.getstr(1, 0, 20).decode("utf-8").strip()
        
            if _employee_id.lower() == "back":
                stdscr.clear()
                stdscr.addstr(0, 0, "Returning to the main menu...")
                stdscr.refresh()
                curses.napms(1000)
                break
        
        try:
            user = DynamoDB.get_user(employee_id)
            id, _ = rfid_reader.read_key()
            users_holding_card = DynamoDB.get_users_by_card(str(id))
            if len(users_holding_card) > 0:
                DynamoDB.remove_all_links_to_card(id)
                
            DynamoDB.register_card_to_user(employee_id, str(id))
            
            stdscr.clear()
            stdscr.addstr(0, 0, f"User '{employee_id}' has had their Keycard Registered successfully!")
        except:
            stdscr.clear()
            stdscr.addstr(0, 0, f"There was an issue whilst deleting '{employee_id}'! Please try again.")
        finally:
            stdscr.refresh()
            curses.napms(3000)
            break

def display_log(stdscr, log_file):
    # Set up curses
    curses.curs_set(0)  # Hide the cursor
    stdscr.clear()

    # Loop to continuously update the screen
    while True:
        stdscr.clear()
        stdscr.border(0)

        # Read the contents of the log file
        try:
            with open(log_file, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            lines = ["Log file not found."]

        # Calculate the available window size
        height, width = stdscr.getmaxyx()

        # Display the last lines that fit in the window
        start_line = max(0, len(lines) - (height - 2))  # Leave space for borders
        for i, line in enumerate(lines[start_line:], start=1):
            if i >= height - 1:  # Avoid exceeding the window height
                break
            stdscr.addstr(i, 1, line[:width-2])  # Trim line to fit width

        stdscr.refresh()
        curses.napms(1000)

    
def main_menu(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    
    rfid_enabled = False
    web_enabled = False
    
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    
    while True:
        stdscr.clear()

        stdscr.addstr(0, 0, "    ____  ______________     _____ _________    _   ___   ____________ ", curses.color_pair(1))
        stdscr.addstr(1, 0, "   / __ \/ ____/  _/ __ \   / ___// ____/   |  / | / / | / / ____/ __ \\", curses.color_pair(1))
        stdscr.addstr(2, 0, "  / /_/ / /_   / // / / /   \__ \/ /   / /| | /  |/ /  |/ / __/ / /_/ /", curses.color_pair(1))
        stdscr.addstr(3, 0, " / _, _/ __/ _/ // /_/ /   ___/ / /___/ ___ |/ /|  / /|  / /___/ _, _/ ", curses.color_pair(1))
        stdscr.addstr(4, 0, "/_/ |_/_/   /___/_____/   /____/\____/_/  |_/_/ |_/_/ |_/_____/_/ |_|", curses.color_pair(1))
        
        stdscr.addstr(6, 0, "Welcome to the Command Line Interface.", curses.A_UNDERLINE)
        stdscr.addstr(8,0,"Interface Status:                                ", curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(9, 0, "RFID Scanning Interface:                         ", curses.color_pair(1) | curses.A_BOLD)
        if rfid_enabled:
            stdscr.addstr(9, 25, f"Working and Operational", curses.color_pair(2))
        else:
            stdscr.addstr(9, 25, f"Disabled", curses.color_pair(2))
        
        stdscr.addstr(10, 0, "Web Interface:                                   ", curses.color_pair(1) | curses.A_BOLD)
        if web_enabled:
            stdscr.addstr(10, 15, f"Working and Operational", curses.color_pair(2))
        else:
            stdscr.addstr(10, 15, f"Disabled", curses.color_pair(1))
        
        
        stdscr.addstr(12, 0, "Main Menu", curses.A_UNDERLINE)   
        stdscr.addstr(13, 0, "1. Register an Employee", curses.color_pair(3))
        stdscr.addstr(14, 0, "2. Register a Keycard", curses.color_pair(3))
        stdscr.addstr(15, 0, "3. Revoke an Employees Access", curses.color_pair(3))
        stdscr.addstr(16, 0, "4. Toggle RFID Scanner", curses.color_pair(3))
        stdscr.addstr(17, 0, "5. Toggle Web Interface", curses.color_pair(3))
        stdscr.addstr(18, 0, "6. Display Thread Log", curses.color_pair(3))
        stdscr.addstr(18, 0, "q. Quit", curses.color_pair(3))
        
        stdscr.addstr(20, 0, "Please select an option >> ")
        
        stdscr.refresh()

        key = stdscr.getch()
        if key == ord('1'):
            add_user(stdscr)
        elif key == ord('3'):
            remove_user(stdscr)
        elif key == ord('4'):
            rfid_enabled = not rfid_enabled
            reader_thread = threading.Thread(target=start_reader, daemon=True)
            reader_thread.start()
        elif key == ord('5'):
            web_enabled = not web_enabled
        elif key == ord('6'):
            display_log(stdscr, "thread_reader.log")
        elif key == ord('q'):
            break

curses.wrapper(main_menu)
