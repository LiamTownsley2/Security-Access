#!/usr/bin/env python
from dotenv import load_dotenv
load_dotenv()

import curses
import threading
import logging
import Util.general, Util.curses, Util.rfid

from queue import Queue
from Classes.RFID_Reader import RFID_Reader
from AWS import db
from Classes.Camera import Camera
from API.index import toggle_api_status, get_api_status
Util.general.initialise_gpio_pins()

thread_logger_file_name = "thread_reader.log"
thread_logger = logging.getLogger("ThreadLogger")
thread_logger.setLevel(logging.INFO)
thread_file_handler = logging.FileHandler(thread_logger_file_name)
thread_file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
thread_logger.addHandler(thread_file_handler)

camera = Camera()
rfid_reader = RFID_Reader(thread_logger)
log_queue = Queue()

def add_user(stdscr):
    while True:
        employee_name = Util.curses.ask_question(stdscr, "Enter full name of the Employee (or type 'back' to return):")
        if employee_name.lower() == "back":
            Util.curses.send_simple(stdscr, "Returning to the main menu...", 1000)
            break

        try:
            user = db.register_user(employee_name)
            if confirm_keycard_registration(stdscr):
                register_keycard(stdscr, user)
            Util.curses.send_simple(stdscr, f"Employee '{employee_name}' added successfully!", 2000)
        except Exception as e:
            Util.curses.send_simple(stdscr, f"There was an issue while adding '{employee_name}': {str(e)}", 1000)
        break

def confirm_keycard_registration(stdscr):
    return Util.curses.ask_question(stdscr, "Would you like to register a keycard? (Y/n):").lower() in ("", "y")

def remove_user(stdscr):
    while True:
        employee_id = Util.curses.ask_question(stdscr, "Enter the ID of the Employee that should be removed (or type 'back' to return):")
        if employee_id.lower() == "back":
            Util.curses.send_simple(stdscr, "Returning to the main menu...", 1000)
            break
        
        try:
            db.delete_user(employee_id)
            Util.curses.send_simple(stdscr, f"User '{employee_id}' removed successfully!", 2000)
        except:
            Util.curses.send_simple(stdscr, f"There was an issue whilst deleting '{employee_id}'! Please try again.", 2000)
        break
    
def register_keycard(stdscr, employee_id=None):
    if employee_id is None:
        employee_id = Util.curses.ask_question(stdscr, "Enter the Employee ID or type 'back' to return:")
        if employee_id.lower() == "back":
            Util.curses.send_simple(stdscr, "Returning to the main menu...", 1000)
            return

    try:
        user = db.get_user(employee_id)
        stdscr.addstr(2, 0, "Awaiting Key Presentation..........")
        stdscr.refresh()

        id, _ = rfid_reader.read_key()
        if db.get_user_by_card(str(id), get_all=True):
            db.remove_all_links_to_card(id)

        db.register_card_to_user(employee_id, str(id))
        Util.curses.send_simple(stdscr, f"User '{employee_id}' has had their Keycard Registered successfully!", 2000)
    except:
        Util.curses.send_simple(stdscr, f"Error registering keycard for '{employee_id}'.", 2000)

def handle_user_interaction(stdscr, key:str, menu):
    for item in menu:
        if key.lower() == item[0]:
            item[2](stdscr)
            return True
    return False

def main_menu(stdscr):
    menu_items = [
        ["1", "Register an Employee", add_user],
        ["2", "Register a Keycard", register_keycard],
        ["3", "Revoke an Employees Access", remove_user],
        ["4", "Toggle RFID Scanner", rfid_reader.toggle_reading],
        ["5", "Toggle Web Interface", toggle_api_status],
        ["6", "View RFID Logs", Util.rfid.view_rfid_logs],
        ["q", "Quit", exit]
    ]
    curses.curs_set(0)
    stdscr.clear()
    
    log_thread = threading.Thread(target=Util.general.watch_log_file, args=(thread_logger_file_name, log_queue), daemon=False)
    log_thread.start()
    
    Util.curses.register_colours()
    
    while True:
        stdscr.clear()

        Util.curses.output_ascii_art(stdscr, 0)
        stdscr.addstr(6, 0, "Welcome to the Command Line Interface.", curses.A_UNDERLINE)
        Util.curses.interface_status(stdscr, 8, rfid_reader.get_status(), get_api_status())
        
        stdscr.addstr(12, 0, "Main Menu", curses.A_UNDERLINE)
        for idx, item in enumerate(menu_items, start=1):
            stdscr.addstr(12 + idx, 0, f"{idx}. {item[1]}", curses.color_pair(3))
          
        stdscr.addstr(21, 0, "Please select an option >> ")
        stdscr.addstr(22, 0, "")
        stdscr.refresh()

        key = stdscr.getch()
        handle_user_interaction(stdscr, key, menu_items)

curses.wrapper(main_menu)