#!/usr/bin/env python
from dotenv import load_dotenv
import curses
import logging
import threading

from main_menu import employee_management
import util.curses
import util.general
import util.rfid
from api.index import get_api_status, toggle_api_status
from classes.Camera import Camera
from classes.RFID_Reader import RFID_Reader

load_dotenv()
util.general.initialise_gpio_pins()

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
        ["1", "Register an Employee", employee_management.user.add_user],
        ["2", "Register a Keycard", employee_management.card.register_keycard],
        [
            "3",
            "Revoke an Employees Access",
            employee_management.user.remove_user,
        ],
        ["4", "Toggle RFID Scanner", rfid_reader.toggle_reading],
        ["5", "Toggle Web Interface", toggle_api_status],
        ["6", "View RFID Logs", util.rfid.view_rfid_logs],
        ["q", "Quit", exit],
    ]
    curses.curs_set(0)
    stdscr.clear()

    log_thread = threading.Thread(
        target=util.general.watch_log_file, args=(thread_logger_file_name), daemon=False
    )
    log_thread.start()

    util.curses.register_colours()

    while True:
        stdscr.clear()

        util.curses.output_ascii_art(stdscr, 0)
        stdscr.addstr(
            6, 0, "Welcome to the Command Line Interface.", curses.A_UNDERLINE
        )
        util.curses.interface_status(
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
