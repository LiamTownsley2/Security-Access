import util.curses as curses_util
from aws import db

from .card import confirm_keycard_registration, register_keycard


def add_user(stdscr):
    while True:
        employee_name = curses_util.ask_question(
            stdscr, "Enter full name of the Employee (or type 'back' to return):"
        )
        if employee_name.lower() == "back":
            curses_util.send_simple(stdscr, "Returning to the main menu...", 1000)
            break

        try:
            user = db.register_user(employee_name)
            if confirm_keycard_registration(stdscr):
                register_keycard(stdscr, user)
            curses_util.send_simple(
                stdscr, f"Employee '{employee_name}' added successfully!", 2000
            )
        except Exception as e:
            curses_util.send_simple(
                stdscr,
                f"There was an issue while adding '{employee_name}': {str(e)}",
                1000,
            )
        break


def remove_user(stdscr):
    while True:
        employee_id = curses_util.ask_question(
            stdscr,
            "Enter the ID of the Employee that should be removed (or type 'back' to return):",
        )
        if employee_id.lower() == "back":
            curses_util.send_simple(stdscr, "Returning to the main menu...", 1000)
            break

        try:
            db.delete_user(employee_id)
            curses_util.send_simple(
                stdscr, f"User '{employee_id}' removed successfully!", 2000
            )
        except Exception:
            curses_util.send_simple(
                stdscr,
                f"There was an issue whilst deleting '{employee_id}'! Please try again.",
                2000,
            )
        break
