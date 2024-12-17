#!/usr/bin/env python
from dotenv import load_dotenv
import curses
import logging
import threading

import MainMenu
import Util.curses
import Util.general
import Util.rfid
from API.index import get_api_status, toggle_api_status
from Classes.Camera import Camera
from Classes.RFID_Reader import RFID_Reader

load_dotenv()
Util.general.initialise_gpio_pins()

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
        ["1", "Register an Employee", MainMenu.employee_management.user.add_user],
        ["2", "Register a Keycard", MainMenu.employee_management.card.register_keycard],
        [
            "3",
            "Revoke an Employees Access",
            MainMenu.employee_management.user.remove_user,
        ],
        ["4", "Toggle RFID Scanner", rfid_reader.toggle_reading],
        ["5", "Toggle Web Interface", toggle_api_status],
        ["6", "View RFID Logs", Util.rfid.view_rfid_logs],
        ["q", "Quit", exit],
    ]
    curses.curs_set(0)
    stdscr.clear()

    log_thread = threading.Thread(
        target=Util.general.watch_log_file, args=(thread_logger_file_name), daemon=False
    )
    log_thread.start()

    Util.curses.register_colours()

    while True:
        stdscr.clear()

        Util.curses.output_ascii_art(stdscr, 0)
        stdscr.addstr(
            6, 0, "Welcome to the Command Line Interface.", curses.A_UNDERLINE
        )
        Util.curses.interface_status(
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
