import curses

import util.general as general_util

def ask_question(stdscr, question: str):
    stdscr.clear()
    stdscr.addstr(0, 0, question)
    stdscr.refresh()
    curses.echo()
    return stdscr.getstr(1, 0, 20).decode("utf-8").strip()


def register_colours():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)


def is_operational_curses(stdscr, row: int, col: int, bool_value: bool):
    if bool_value:
        stdscr.addstr(row, col, "Working and Operational", curses.color_pair(2))
    else:
        stdscr.addstr(row, col, "Disabled", curses.color_pair(1))


def output_ascii_art(stdscr, starting_row: int):
    ascii_art = [
        "    ____  ______________     _____ _________    _   ___   ____________ ",
        "   / __ \/ ____/  _/ __ \   / ___// ____/   |  / | / / | / / ____/ __ \\",
        "  / /_/ / /_   / // / / /   \__ \/ /   / /| | /  |/ /  |/ / __/ / /_/ /",
        " / _, _/ __/ _/ // /_/ /   ___/ / /___/ ___ |/ /|  / /|  / /___/ _, _/ ",
        "/_/ |_/_/   /___/_____/   /____/\____/_/  |_/_/ |_/_/ |_/_____/_/ |_|",
    ]

    for idx, text in enumerate(ascii_art, start=starting_row):
        stdscr.addstr(idx, 0, text, curses.color_pair(1))


def interface_status(stdscr, starting_row: int, rfid_status: bool, api_status: bool):
    # Interface Status
    stdscr.addstr(
        starting_row,
        0,
        "Interface Status:" + general_util.repeat(" ", 32),
        curses.color_pair(1) | curses.A_BOLD,
    )

    #   RFID Scanning
    stdscr.addstr(
        9,
        0,
        "RFID Scanning Interface:" + general_util.repeat(" ", 25),
        curses.color_pair(1) | curses.A_BOLD,
    )
    is_operational_curses(stdscr, 9, 25, rfid_status)

    #   Web Interface
    stdscr.addstr(
        10,
        0,
        "Web Interface:" + general_util.repeat(" ", 35),
        curses.color_pair(1) | curses.A_BOLD,
    )
    is_operational_curses(stdscr, 10, 15, api_status)

def send_simple(stdscr, message: str, timeout: int, row=0):
    stdscr.clear()
    stdscr.addstr(row, 0, message)
    stdscr.refresh()
    curses.napms(timeout)
