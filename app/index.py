#!/usr/bin/env python
import sys
import os

import curses
import logging
import threading

from .main_menu.employee_management import card, user
from .util import curses as curses_util
from .util import general as general_util
from .util import rfid as rfid_util
from .api.index import get_api_status, toggle_api_status
from .classes import Camera
from .classes import RFID_Reader

# Add app/ to Python Path.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

thread_logger_file_name = "thread_reader.log"
thread_logger = logging.getLogger("ThreadLogger")
thread_logger.setLevel(logging.INFO)
thread_file_handler = logging.FileHandler(thread_logger_file_name)
thread_file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)
thread_logger.addHandler(thread_file_handler)

camera = Camera()
rfid_reader = RFID_Reader(thread_logger, camera)


def handle_user_interaction(stdscr, key: str, menu):
    for item in menu:
        if key.lower() == item[0]:
            item[2](stdscr)
            return True
    return False


def main_menu(stdscr):
    menu_items = [
        ["1", "Register an Employee", user.add_user],
        ["2", "Register a Keycard", card.register_keycard],
        [
            "3",
            "Revoke an Employees Access",
            user.remove_user,
        ],
        ["4", "Toggle RFID Scanner", rfid_reader.toggle_reading],
        ["5", "Toggle Web Interface", toggle_api_status],
        ["6", "View RFID Logs", rfid_util.view_rfid_logs],
        ["q", "Quit", exit],
    ]
    curses.curs_set(0)
    stdscr.clear()

    log_thread = threading.Thread(
        target=general_util.watch_log_file, args=(thread_logger_file_name), daemon=False
    )
    log_thread.start()

    curses_util.register_colours()

    while True:
        stdscr.clear()

        curses_util.output_ascii_art(stdscr, 0)
        stdscr.addstr(
            6, 0, "Welcome to the Command Line Interface.", curses.A_UNDERLINE
        )
        curses_util.interface_status(
            stdscr, 8, rfid_reader.get_status(), get_api_status()
        )

        stdscr.addstr(12, 0, "Main Menu", curses.A_UNDERLINE)
        for idx, item in enumerate(menu_items, start=1):
            stdscr.addstr(12 + idx, 0, f"{idx}. {item[1]}", curses.color_pair(3))

        stdscr.addstr(21, 0, "Please select an option >> ")
        stdscr.addstr(22, 0, "")
        stdscr.refresh()

        key = stdscr.getch()
        handle_user_interaction(stdscr, key, menu_items)


curses.wrapper(main_menu)
