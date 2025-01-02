#!/usr/bin/env python
import curses
import threading

from dotenv import load_dotenv

from api.index import get_api_status, toggle_api_status
from classes.RFID_Reader import thread_log_path

# import logging
from main_menu.employee_management import card, user
from main_menu.employee_management.card import rfid_reader
from util import curses as curses_util
from util import general as general_util
from util import rfid as rfid_util

load_dotenv()

def handle_user_interaction(stdscr, key, menu):
    try:
        for item in menu:
            _chr = chr(key).lower()
            if _chr == "q":
                item[2]()
                return False
            elif _chr == item[0]:
                item[2](stdscr)
                return True
        return False
    except Exception:
        pass

def main_menu(stdscr):
    menu_items = [
        ["1", "Register an Employee", user.add_user],
        ["2", "Register a Keycard", card.register_keycard],
        [
            "3",
            "Revoke an Employees Access",
            user.remove_user,
        ],
        ["4", "Toggle RFID Scanner", rfid_reader.start],
        ["5", "Toggle Web Interface", toggle_api_status],
        ["6", "View RFID Logs", rfid_util.view_rfid_logs],
        ["q", "Quit", curses.endwin],
    ]
    curses.curs_set(0)
    stdscr.clear()

    try:
        log_thread = threading.Thread(
            target=general_util.watch_log_file, args=(thread_log_path,), daemon=False
        )
        log_thread.start()
    except KeyboardInterrupt:
        pass

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
            stdscr.addstr(12 + idx, 0, f"{item[0]}. {item[1]}", curses.color_pair(3))

        stdscr.addstr(21, 0, "Please select an option >> ")
        stdscr.addstr(22, 0, "")

        stdscr.refresh()

        key = stdscr.getch()
        response = handle_user_interaction(stdscr, key, menu_items)
        if not response:
            break


curses.wrapper(main_menu)
