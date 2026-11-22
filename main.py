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


def option_row(options, selected):
    """Draw a horizontal menu like:   Retry   [ Menu ]   Quit"""
    return "   ".join(f"[ {o} ]" if i == selected else f"  {o}  " for i, o in enumerate(options))


# --- Screens ---------------------------------------------------------------------

def vertical_menu(stdscr, title, options, esc_hint):
    """Draw a numbered vertical menu. Returns the chosen index, or None for Esc.

    Arrows move, number keys jump to an option, Enter selects.
    """
    stdscr.timeout(-1)
    selected = 0
    while True:
        stdscr.erase()
        rows, _ = stdscr.getmaxyx()
        mid = rows // 2
        centered(stdscr, mid - 3, title, curses.A_BOLD)
        for i, option in enumerate(options):
            label = f"{i + 1}. {option}"
            attr = curses.A_REVERSE if i == selected else curses.A_NORMAL
            centered(stdscr, mid - 1 + i, f" {label} ", attr)
        centered(stdscr, rows - 1, f"Arrows: move   Enter: select   Esc: {esc_hint}", curses.A_DIM)
        stdscr.refresh()

        key = stdscr.getch()
        if key == KEY_ESC:
            return None
        if key in (curses.KEY_LEFT, curses.KEY_UP):
            selected = max(0, selected - 1)
        elif key in (curses.KEY_RIGHT, curses.KEY_DOWN):
            selected = min(len(options) - 1, selected + 1)
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
        rows, _ = stdscr.getmaxyx()
        mid = rows // 2
        centered(stdscr, mid - 3, f"{wpm:.0f} WPM", curses.A_BOLD)
        if difficulty is not None:
            centered(stdscr, mid - 2, f"Difficulty: {difficulty.capitalize()}", curses.A_DIM)
        centered(stdscr, mid - 1, f"You typed faster than {percent:.0f}% of people")
        centered(stdscr, mid + 2, option_row(options, selected))
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
