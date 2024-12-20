import util.curses as curses_util
from aws import db
from classes.RFID_Reader import RFID_Reader

rfid_reader = RFID_Reader()


def confirm_keycard_registration(stdscr):
    return curses_util.ask_question(
        stdscr, "Would you like to register a keycard? (Y/n):"
    ).lower() in ("", "y")


def register_keycard(stdscr, employee_id=None):
    global rfid_reader
    if employee_id is None:
        employee_id = curses_util.ask_question(
            stdscr, "Enter the Employee ID or type 'back' to return:"
        )
        if employee_id.lower() == "back":
            curses_util.send_simple(stdscr, "Returning to the main menu...", 1000)
            return

    try:
        db.get_user(employee_id)
        stdscr.addstr(2, 0, "Awaiting Key Presentation..........")
        stdscr.refresh()

        id, text = rfid_reader.read_key()
        stdscr.addstr(3, 0, "Key Presented........")
        stdscr.addstr(4, 0, f"ID...........{id}")
        stdscr.addstr(5, 0, f"Text.........{text}")
        stdscr.refresh()
        if db.get_user_by_card(str(id), get_all=True):
            stdscr.addstr(6, 0, "This card is shared with OTHER users!")
            stdscr.refresh()
            db.remove_all_links_to_card(id)
            stdscr.addstr(7, 0, "This card is no longer shared with other users!")
            stdscr.refresh()

        stdscr.addstr(8, 0, "Attempting to register card to Employee!")
        stdscr.refresh()
        db.register_card_to_user(employee_id, str(id))
        stdscr.addstr(9, 0, "Registered card to Employee!")
        stdscr.refresh()
        curses_util.send_simple(
            stdscr,
            f"User '{employee_id}' has had their Keycard Registered successfully!",
            2000,
        )
    except Exception:
        curses_util.send_simple(
            stdscr, f"Error registering keycard for '{employee_id}'.", 2000
        )
