"""Typing test CLI app: the curses user interface.

Run in Git Bash on Windows with:   winpty python main.py
All the scoring/typing logic lives in logic.py; this file only draws the
screen and reads keys.
"""

import curses
import os
import time

import logic

# Make Esc respond instantly (curses otherwise waits ~1s to see if Esc is the
# start of a longer key sequence like an arrow key). Must be set before curses starts.
os.environ.setdefault("ESCDELAY", "25")

KEY_ESC = 27
BACKSPACE_KEYS = {curses.KEY_BACKSPACE, 8, 127}
ENTER_KEYS = {curses.KEY_ENTER, 10, 13, 459}  # 459 = keypad Enter on Windows

LEFT_MARGIN = 2
TEXT_TOP = 3  # screen row where the test text starts

# Color pair numbers (set up in init_colors)
GREEN, RED, GREEN_BOX, RED_BOX = 1, 2, 3, 4


def init_colors():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(GREEN, curses.COLOR_GREEN, -1)
    curses.init_pair(RED, curses.COLOR_RED, -1)
    curses.init_pair(GREEN_BOX, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(RED_BOX, curses.COLOR_BLACK, curses.COLOR_RED)


def safe_addstr(win, row, col, text, attr=0):
    """addstr that ignores curses.error (e.g. writing off the edge of a small window)."""
    try:
        win.addstr(row, col, text, attr)
    except curses.error:
        pass


def centered(win, row, text, attr=0):
    _, cols = win.getmaxyx()
    safe_addstr(win, row, max(0, (cols - len(text)) // 2), text, attr)


# --- Screens ---------------------------------------------------------------------

def countdown(stdscr):
    """Show 5..1 before the test. Returns False if the user pressed Esc."""
    stdscr.timeout(50)  # getch waits at most 50 ms so the countdown keeps moving
    end = time.monotonic() + logic.COUNTDOWN_SECONDS
    while (left := end - time.monotonic()) > 0:
        stdscr.erase()
        rows, _ = stdscr.getmaxyx()
        centered(stdscr, rows // 2 - 1, "Get ready...")
        centered(stdscr, rows // 2 + 1, str(int(left) + 1), curses.A_BOLD)
        centered(stdscr, rows - 1, "Esc: quit", curses.A_DIM)
        stdscr.refresh()
        if stdscr.getch() == KEY_ESC:
            return False
    return True


def char_attr(test, i):
    """Pick the color/style for character i of the test text."""
    status = test.status(i)
    is_space = test.target[i] == " "
    if status == logic.CORRECT:
        attr = curses.color_pair(GREEN_BOX if is_space else GREEN)
    elif status == logic.INCORRECT:
        attr = curses.color_pair(RED_BOX if is_space else RED)
    else:
        attr = curses.A_NORMAL
    if i == test.cursor:
        attr |= curses.A_UNDERLINE | curses.A_BOLD  # show where you are
    return attr


def draw_test(stdscr, test, seconds_left):
    stdscr.erase()
    _, cols = stdscr.getmaxyx()
    safe_addstr(stdscr, 0, LEFT_MARGIN, "Typing Test", curses.A_BOLD)
    safe_addstr(stdscr, 1, LEFT_MARGIN, f"Time left: {seconds_left:2d}s    Esc: quit")
    width = cols - 2 * LEFT_MARGIN
    for i, (row, col) in enumerate(logic.wrap_positions(test.target, width)):
        safe_addstr(stdscr, TEXT_TOP + row, LEFT_MARGIN + col, test.target[i], char_attr(test, i))
    stdscr.refresh()


def run_test(stdscr):
    """Run one 45-second test. Returns (wpm, percent) or None if Esc was pressed."""
    test = logic.TypingTest(logic.generate_text())
    stdscr.timeout(100)  # wake up every 100 ms to update the timer
    start = time.monotonic()
    while True:
        elapsed = time.monotonic() - start
        if elapsed >= logic.TEST_SECONDS or test.is_finished():
            break
        draw_test(stdscr, test, int(logic.TEST_SECONDS - elapsed + 0.999))
        key = stdscr.getch()
        if key == KEY_ESC:
            return None
        if key in BACKSPACE_KEYS:
            test.backspace()
        elif 32 <= key <= 126:  # printable characters (including space)
            test.type_char(chr(key))
    elapsed = min(time.monotonic() - start, logic.TEST_SECONDS)
    wpm = logic.calculate_wpm(test.correct_count(), elapsed)
    return wpm, logic.percent_beaten(wpm)


def show_results(stdscr, wpm, percent):
    """Show the score with a Retry/Quit menu. Returns "retry" or "quit"."""
    curses.flushinp()  # throw away keys typed as time ran out
    stdscr.timeout(-1)  # wait for keys normally again
    options = ["Retry", "Quit"]
    selected = 0
    while True:
        stdscr.erase()
        rows, _ = stdscr.getmaxyx()
        mid = rows // 2
        centered(stdscr, mid - 3, f"{wpm:.0f} WPM", curses.A_BOLD)
        centered(stdscr, mid - 1, f"You typed faster than {percent:.0f}% of people")
        menu = "   ".join(f"[ {o} ]" if i == selected else f"  {o}  " for i, o in enumerate(options))
        centered(stdscr, mid + 2, menu)
        centered(stdscr, rows - 1, "Left/Right: move   Enter: select   Esc: quit", curses.A_DIM)
        stdscr.refresh()

        key = stdscr.getch()
        if key == KEY_ESC:
            return "quit"
        if key == curses.KEY_LEFT:
            selected = max(0, selected - 1)
        elif key == curses.KEY_RIGHT:
            selected = min(len(options) - 1, selected + 1)
        elif key in ENTER_KEYS:
            return options[selected].lower()


def app(stdscr):
    try:
        curses.curs_set(0)  # hide the blinking terminal cursor
    except curses.error:
        pass
    init_colors()
    stdscr.keypad(True)  # turn arrow keys into curses.KEY_LEFT etc.
    while True:
        if not countdown(stdscr):
            return
        result = run_test(stdscr)
        if result is None:
            return
        if show_results(stdscr, *result) == "quit":
            return


if __name__ == "__main__":
    curses.wrapper(app)
