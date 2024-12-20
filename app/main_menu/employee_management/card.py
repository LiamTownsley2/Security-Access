import util.curses as curses_util
from aws import db
from app.index import rfid_reader

def confirm_keycard_registration(stdscr):
    return curses_util.ask_question(
        stdscr, "Would you like to register a keycard? (Y/n):"
    ).lower() in ("", "y")


def register_keycard(stdscr, employee_id=None):
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

        id, _ = rfid_reader.read_key()
        if db.get_user_by_card(str(id), get_all=True):
            db.remove_all_links_to_card(id)

        db.register_card_to_user(employee_id, str(id))
        curses_util.send_simple(
            stdscr,
            f"User '{employee_id}' has had their Keycard Registered successfully!",
            2000,
        )
    except Exception:
        curses_util.send_simple(
            stdscr, f"Error registering keycard for '{employee_id}'.", 2000
        )
