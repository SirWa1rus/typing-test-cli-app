"""Typing test CLI app: the curses user interface.

Run in Git Bash on Windows with:   winpty python main.py
All the scoring/typing logic lives in logic.py; this file only draws the
screen and reads keys.
"""

import curses
import os
import sys
import time

import logic

# Make Esc respond instantly (curses otherwise waits ~1s to see if Esc is the
# start of a longer key sequence like an arrow key). Must be set before curses starts.
os.environ.setdefault("ESCDELAY", "25")

KEY_ESC = 27
BACKSPACE_KEYS = {curses.KEY_BACKSPACE, 8, 127}
ENTER_KEYS = {curses.KEY_ENTER, 10, 13, 459}  # 459 = keypad Enter on Windows

LEFT_MARGIN = 2

# Color pair numbers (set up in init_colors)
GREEN, RED, GREEN_BOX, RED_BOX, HIGHLIGHT = 1, 2, 3, 4, 5

BRIGHT_WHITE = 15  # color 7 (COLOR_WHITE) is often light gray; 15 is true white


def init_colors():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(GREEN, curses.COLOR_GREEN, -1)
    curses.init_pair(RED, curses.COLOR_RED, -1)
    curses.init_pair(GREEN_BOX, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(RED_BOX, curses.COLOR_BLACK, curses.COLOR_RED)
    # R5.1: black text on a white box for the button the user is on.
    white = BRIGHT_WHITE if curses.COLORS > BRIGHT_WHITE else curses.COLOR_WHITE
    curses.init_pair(HIGHLIGHT, curses.COLOR_BLACK, white)


def highlight_attr():
    """The white-box style (R5.1); reverse video if the terminal has no colors."""
    return curses.color_pair(HIGHLIGHT) if curses.has_colors() else curses.A_REVERSE


def safe_addstr(win, row, col, text, attr=0):
    """addstr that ignores curses.error (e.g. writing off the edge of a small window)."""
    try:
        win.addstr(row, col, text, attr)
    except curses.error:
        pass


def centered(win, row, text, attr=0):
    _, cols = win.getmaxyx()
    safe_addstr(win, row, max(0, (cols - len(text)) // 2), text, attr)


def handle_resize(key):
    """React to the terminal being zoomed (Ctrl+scroll) or resized (R4.1).

    Returns True if `key` was a resize event. On Windows (PDCurses) curses must
    be told to re-read the window size; other systems update it automatically.
    The screens re-read getmaxyx() on every redraw, so the layout then follows.
    """
    if key != curses.KEY_RESIZE:
        return False
    if sys.platform == "win32":
        try:
            curses.resize_term(0, 0)
        except curses.error:
            pass
    return True


def draw_buttons(win, buttons):
    """Draw logic.Button objects; the selected one gets the white box (R5.1)."""
    for b in buttons:
        safe_addstr(win, b.row, b.col, b.text, highlight_attr() if b.selected else curses.A_NORMAL)


# --- Screens ---------------------------------------------------------------------

def vertical_menu(stdscr, title, options, esc_hint):
    """Draw a numbered vertical menu. Returns the chosen index, or None for Esc.

    Arrows move, number keys jump to an option, Enter selects.
    """
    stdscr.timeout(-1)
    selected = 0
    labels = [f"{i + 1}. {option}" for i, option in enumerate(options)]
    while True:
        stdscr.erase()
        rows, cols = stdscr.getmaxyx()
        centered(stdscr, rows // 2 - 3, title, curses.A_BOLD)
        draw_buttons(stdscr, logic.vertical_menu_buttons(labels, selected, cols, rows))
        centered(stdscr, rows - 1, f"Arrows: move   Enter: select   Esc: {esc_hint}", curses.A_DIM)
        stdscr.refresh()

        key = stdscr.getch()
        if key == KEY_ESC:
            return None
        if key in (curses.KEY_LEFT, curses.KEY_UP):
            selected = logic.move_selection(selected, -1, len(options))
        elif key in (curses.KEY_RIGHT, curses.KEY_DOWN):
            selected = logic.move_selection(selected, 1, len(options))
        elif ord("1") <= key < ord("1") + len(options):
            selected = key - ord("1")
        elif key in ENTER_KEYS:
            return selected


def main_menu(stdscr):
    """Standard/Custom choice. Returns "standard", "custom", or None for Esc."""
    choice = vertical_menu(stdscr, "Typing Test",
                           ["Standard typing test", "Custom typing test"], "quit")
    return None if choice is None else ["standard", "custom"][choice]


def choose_difficulty(stdscr):
    """Easy/Medium/Hard choice. Returns a logic difficulty, or None for Esc (back to menu)."""
    labels = [d.capitalize() for d in logic.DIFFICULTIES]
    choice = vertical_menu(stdscr, "Choose difficulty", labels, "back to menu")
    return None if choice is None else logic.DIFFICULTIES[choice]


def ask_custom_text(stdscr):
    """Let the user type a path to a .txt file until it loads.

    Returns the cleaned test text, or None if Esc was pressed (back to menu).
    """
    stdscr.timeout(-1)
    path = ""
    error = ""
    while True:
        stdscr.erase()
        rows, cols = stdscr.getmaxyx()
        safe_addstr(stdscr, 0, LEFT_MARGIN, "Custom Typing Test", curses.A_BOLD)
        safe_addstr(stdscr, 2, LEFT_MARGIN, "Path to a .txt file "
                    f"({logic.MIN_CUSTOM_CHARS}-{logic.MAX_CUSTOM_CHARS} characters):")
        # Show the end of long paths so the part being typed stays visible.
        visible = path[-(cols - 2 * LEFT_MARGIN - 3):] if cols > 2 * LEFT_MARGIN + 3 else ""
        safe_addstr(stdscr, 4, LEFT_MARGIN, "> " + visible)
        safe_addstr(stdscr, 4, LEFT_MARGIN + 2 + len(visible), " ", curses.A_REVERSE)  # fake cursor
        if error:
            safe_addstr(stdscr, 6, LEFT_MARGIN, error, curses.color_pair(RED))
        centered(stdscr, rows - 1, "Enter: start   Esc: back to menu", curses.A_DIM)
        stdscr.refresh()

        key = stdscr.getch()
        if key == KEY_ESC:
            return None
        if key in ENTER_KEYS:
            try:
                return logic.load_custom_text(path)
            except logic.CustomTextError as e:
                error = str(e)
        elif key in BACKSPACE_KEYS:
            path = path[:-1]
        elif 32 <= key <= 126:
            path += chr(key)


def countdown(stdscr):
    """Show 5..1 before the test. Returns False if the user pressed Esc."""
    stdscr.timeout(50)  # getch waits at most 50 ms so the countdown keeps moving
    end = time.monotonic() + logic.COUNTDOWN_SECONDS
    while (left := end - time.monotonic()) > 0:
        stdscr.erase()
        rows, cols = stdscr.getmaxyx()
        centered(stdscr, rows // 2 - 1, "Get ready...")
        centered(stdscr, rows // 2 + 1, str(int(left) + 1), curses.A_BOLD)
        centered(stdscr, rows // 2 + 3, logic.zoom_tip(cols))
        centered(stdscr, rows - 1, "Esc: quit", curses.A_DIM)
        stdscr.refresh()
        key = stdscr.getch()
        handle_resize(key)
        if key == KEY_ESC:
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
    rows, cols = stdscr.getmaxyx()
    safe_addstr(stdscr, 0, LEFT_MARGIN, "Typing Test", curses.A_BOLD)
    safe_addstr(stdscr, 1, LEFT_MARGIN, f"Time left: {seconds_left:2d}s    Esc: quit")
    # R4.2: the text block sits in the middle of the screen.
    for i, (row, col) in enumerate(logic.centered_positions(test.target, cols, rows)):
        safe_addstr(stdscr, row, col, test.target[i], char_attr(test, i))
    centered(stdscr, rows - 1, logic.zoom_tip(cols), curses.A_DIM)  # R4.1
    stdscr.refresh()


def run_test(stdscr, text):
    """Run one 45-second test on `text`. Returns (wpm, percent) or None if Esc was pressed."""
    test = logic.TypingTest(text)
    stdscr.timeout(100)  # wake up every 100 ms to update the timer
    start = time.monotonic()
    while True:
        elapsed = time.monotonic() - start
        if elapsed >= logic.TEST_SECONDS or test.is_finished():
            break
        draw_test(stdscr, test, int(logic.TEST_SECONDS - elapsed + 0.999))
        key = stdscr.getch()
        if handle_resize(key):
            continue  # redraw at the new size
        if key == KEY_ESC:
            return None
        if key in BACKSPACE_KEYS:
            test.backspace()
        elif 32 <= key <= 126:  # printable characters (including space)
            test.type_char(chr(key))
    elapsed = min(time.monotonic() - start, logic.TEST_SECONDS)
    wpm = logic.calculate_wpm(test.correct_count(), elapsed)
    return wpm, logic.percent_beaten(wpm)


def show_results(stdscr, wpm, percent, difficulty=None):
    """Show the score with a Retry/Menu/Quit menu. Returns "retry", "menu", or "quit".

    `difficulty` is shown under the WPM for standard tests (None for custom tests).
    """
    curses.flushinp()  # throw away keys typed as time ran out
    stdscr.timeout(-1)  # wait for keys normally again
    options = ["Retry", "Menu", "Quit"]
    selected = 0
    while True:
        stdscr.erase()
        rows, cols = stdscr.getmaxyx()
        mid = rows // 2
        centered(stdscr, mid - 3, f"{wpm:.0f} WPM", curses.A_BOLD)
        if difficulty is not None:
            centered(stdscr, mid - 2, f"Difficulty: {difficulty.capitalize()}", curses.A_DIM)
        centered(stdscr, mid - 1, f"You typed faster than {percent:.0f}% of people")
        draw_buttons(stdscr, logic.button_row(options, selected, cols, mid + 2))
        centered(stdscr, rows - 1, "Left/Right: move   Enter: select   Esc: quit", curses.A_DIM)
        stdscr.refresh()

        key = stdscr.getch()
        if key == KEY_ESC:
            return "quit"
        if key == curses.KEY_LEFT:
            selected = logic.move_selection(selected, -1, len(options))
        elif key == curses.KEY_RIGHT:
            selected = logic.move_selection(selected, 1, len(options))
        elif key in ENTER_KEYS:
            return options[selected].lower()


def app(stdscr):
    try:
        curses.curs_set(0)  # hide the blinking terminal cursor
    except curses.error:
        pass
    init_colors()
    stdscr.keypad(True)  # turn arrow keys into curses.KEY_LEFT etc.
    while True:  # main menu loop
        mode = main_menu(stdscr)
        if mode is None:
            return
        custom_text = None
        difficulty = None
        if mode == "custom":
            custom_text = ask_custom_text(stdscr)
            if custom_text is None:
                continue  # Esc: back to the main menu
        else:
            difficulty = choose_difficulty(stdscr)
            if difficulty is None:
                continue  # Esc: back to the main menu
        while True:  # Retry loop: same mode (custom text or difficulty) each time
            if not countdown(stdscr):
                return
            if custom_text is not None:
                text = custom_text
            else:
                text = logic.generate_text(difficulty=difficulty)
            result = run_test(stdscr, text)
            if result is None:
                return
            choice = show_results(stdscr, *result, difficulty)
            if choice == "quit":
                return
            if choice == "menu":
                break


if __name__ == "__main__":
    curses.wrapper(app)
