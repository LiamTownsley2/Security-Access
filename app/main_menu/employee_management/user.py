from ..employee_management import confirm_keycard_registration, register_keycard
from aws import db
import util.curses


def add_user(stdscr):
    while True:
        employee_name = util.curses.ask_question(
            stdscr, "Enter full name of the Employee (or type 'back' to return):"
        )
        if employee_name.lower() == "back":
            util.curses.send_simple(stdscr, "Returning to the main menu...", 1000)
            break

        try:
            user = db.register_user(employee_name)
            if confirm_keycard_registration(stdscr):
                register_keycard(stdscr, user)
            util.curses.send_simple(
                stdscr, f"Employee '{employee_name}' added successfully!", 2000
            )
        except Exception as e:
            util.curses.send_simple(
                stdscr,
                f"There was an issue while adding '{employee_name}': {str(e)}",
                1000,
            )
        break


def remove_user(stdscr):
    while True:
        employee_id = util.curses.ask_question(
            stdscr,
            "Enter the ID of the Employee that should be removed (or type 'back' to return):",
        )
        if employee_id.lower() == "back":
            util.curses.send_simple(stdscr, "Returning to the main menu...", 1000)
            break

        try:
            db.delete_user(employee_id)
            util.curses.send_simple(
                stdscr, f"User '{employee_id}' removed successfully!", 2000
            )
        except Exception:
            util.curses.send_simple(
                stdscr,
                f"There was an issue whilst deleting '{employee_id}'! Please try again.",
                2000,
            )
        break
