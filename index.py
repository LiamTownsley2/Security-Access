#!/usr/bin/env python
from dotenv import load_dotenv
load_dotenv()

import curses
import threading
import logging
import Util
import time
import os

from queue import Queue
from Classes.RFID_Reader import RFID_Reader
from AWS import S3, db
from Classes.GPIO_Pin import GPIO_Pin
from Classes.Camera import Camera
from API.index import initialize_api
Util.initialise_gpio_pins()

thread_logger_file_name = "thread_reader.log"
thread_logger = logging.getLogger("ThreadLogger")
thread_logger.setLevel(logging.INFO)
thread_file_handler = logging.FileHandler(thread_logger_file_name)
thread_file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
thread_logger.addHandler(thread_file_handler)

rfid_reader = RFID_Reader(thread_logger)
log_queue = Queue()
camera = Camera()

def validate_key(user, text):
    if not user: return False
    if not text == "secret": return False
    return True

def record_and_upload(seconds:int, id = None):
    file_name = camera.start_recording(seconds)
    segmentation_path = id if id is not None else "non-identified"
    upload_url = S3.upload_to_s3(file_name, "cmp408-cctv-recordings", f"cctv-footage/{segmentation_path}/{file_name}")
    os.remove(file_name)
    return upload_url

def start_reader():
    try:
        while True:
            thread_logger.info("start_reader() running.")
            id, text = rfid_reader.read_key()
            thread_logger.info(f"Card Read: ({id}) {text}")
            user = db.get_user_by_card(str(id))
            thread_logger.info(f"\t {user}")
            is_valid = validate_key(user, text)
            thread_logger.info(f"Key Valid: {is_valid}")
            thread_logger.info(f"*{'VALID' if is_valid else 'INVALID'} TAG READ* | ID: {id} | Text: '{text}'")
            
            if is_valid:
                record_and_upload(5, user['UserID'])
                
                db.register_entry(str(id), user['UserID'])
                entries = db.get_entries_count(user['UserID'])
                thread_logger.info(f"You have entered this building {entries} time(s) before.")
                green_led = GPIO_Pin(12) # The Green LED represents unlocking the door.
                green_led.enable(3)
            else:
                record_and_upload(5)

    except Exception as e:
        thread_logger.error(e)

def send_simple_notification(stdscr, message:str, timeout:int, row = 0):
    stdscr.clear()
    stdscr.addstr(row, 0, message)
    stdscr.refresh()
    curses.napms(timeout)

def add_user(stdscr):
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Enter full name of the Employee (or type 'back' to return):")
        stdscr.refresh()

        curses.echo()
        employee_name = stdscr.getstr(1, 0, 20).decode("utf-8").strip()
        
        if employee_name.lower() == "back":
            send_simple_notification(stdscr, "Returning to the main menu...", 1000)
            break
        
        try:
            user = db.register_user(employee_name)
            stdscr.clear()
            stdscr.addstr(0, 0, "Would you like to register a keycard at this time? (Y/n): ")
            stdscr.refresh()
            curses.echo()

            select_key_registration = stdscr.getstr(1, 0, 20).decode("utf-8").strip().lower()
            if select_key_registration in ("", "y"):
                register_keycard(stdscr, user)

            send_simple_notification(stdscr, f"Employee '{employee_name}' added successfully!", 2000)
        except Exception as e:
            send_simple_notification(stdscr, f"There was an issue while adding '{employee_name}': {str(e)}", 1000)
        break

def remove_user(stdscr):
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Enter the ID of the Employee that should be removed (or type 'back' to return):")
        stdscr.refresh()

        curses.echo()
        employee_id = stdscr.getstr(1, 0, 20).decode("utf-8").strip()
        
        if employee_id.lower() == "back":
            send_simple_notification(stdscr, "Returning to the main menu...", 1000)
            break
        
        try:
            db.delete_user(employee_id)
            send_simple_notification(stdscr, f"User '{employee_id}' removed successfully!", 2000)
        except:
            send_simple_notification(stdscr, f"There was an issue whilst deleting '{employee_id}'! Please try again.", 2000)

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
                send_simple_notification(stdscr, "Returning to the main menu...", 1000)
                break
        
        try:
            user = db.get_user(employee_id)
            stdscr.addstr(2, 0, "Awaiting Key Presentation..........")
            stdscr.refresh()

            id, _ = rfid_reader.read_key()
            users_holding_card = db.get_users_by_card(str(id))
            if len(users_holding_card) > 0:
                db.remove_all_links_to_card(id)
                
            db.register_card_to_user(employee_id, str(id))
            
            send_simple_notification(stdscr, f"User '{employee_id}' has had their Keycard Registered successfully!", 2000)
        except:
            send_simple_notification(stdscr, f"There was an issue whilst deleting '{employee_id}'! Please try again.", 2000)
            break
        
def watch_log_file(file_path, log_queue):
    with open(file_path, 'r') as log_file:
        log_file.seek(0, 2)
        while True:
            line = log_file.readline()
            if line:
                log_queue.put(line)
            else:
                time.sleep(0.1)

def view_rfid_logs(stdscr, log_queue):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.clear()
    
    stdscr.addstr(0, 0, "Log Viewer (Press 'q' to quit):")
    
    log_lines = []
    while True:
        try:
            key = stdscr.getkey()
            if key == 'q':
                break
        except curses.error:
            pass
        
        while not log_queue.empty():
            log_lines.append(log_queue.get())
        
        log_lines = log_lines[-20:]
        
        for idx, line in enumerate(log_lines, start=1):
            stdscr.addstr(idx, 0, line.strip())
        
        stdscr.refresh()
        time.sleep(0.1)
            
def main_menu(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    
    rfid_enabled = False
    web_enabled = False

    log_thread = threading.Thread(target=watch_log_file, args=(thread_logger_file_name, log_queue), daemon=False)
    log_thread.start()
    
    api_thread = threading.Thread(target=initialize_api, daemon=False)
    api_thread.start()
    
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    
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
            stdscr.addstr(9, 25, f"Disabled", curses.color_pair(1))
        
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
        stdscr.addstr(18, 0, "6. View RFID Logs", curses.color_pair(3))
        stdscr.addstr(19, 0, "q. Quit", curses.color_pair(3))
        
        stdscr.addstr(21, 0, "Please select an option >> ")
        
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
            curses.wrapper(view_rfid_logs, log_queue)

        elif key == ord('q'):
            break

curses.wrapper(main_menu)
