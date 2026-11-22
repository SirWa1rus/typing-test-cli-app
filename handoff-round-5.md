# Handoff: end of Round 5

For a fresh session starting the next round. Read `CLAUDE.md` first: it holds
the standing rules for every session (commits, test names, decision records,
Git Bash, winpty, history.md, layout math in logic.py, buttons). This file
describes the state of the project at the end of Round 5. It replaces
`handoff-round-4.md` and the older handoffs; where they disagree, this file is
correct.

## Current state (2026-11-22)

- **Round 1 (done):** a timed standard typing test (5 s countdown, 45 s test).
  Each character turns green or red as you type, and the results screen shows a
  WPM score and a "you beat X% of people" figure.
- **Round 2 (done):** a custom typing test from a `.txt` file (**R2.1**).
- **Round 3 (done):** Easy / Medium / Hard difficulty for the standard test
  (**R3.1**).
- **Round 4 (done):** a zoom tip for bigger text (**R4.1**) and the test text
  centered as one block at most 60 columns wide (**R4.2**).
- **Round 5 (done):**
  - **R5.1, white box on the hovered button:** on the main menu, the difficulty
    menu, and the results screen (Retry / Menu / Quit), the option the user is
    on has a black-on-white box behind it. All buttons in one menu are the same
    width, so the box keeps its size and place as the user moves. The results
    screen no longer uses `[ ]` brackets. The custom-file path field is a text
    field, not a button, so it has no box.
- **Tests:** 90 logic tests, all passing: 14 `test_R1_1_*`, 2 `test_R1_2_*`,
  3 `test_R1_3_*`, 25 `test_R2_1_*`, 17 `test_R3_1_*`, 4 `test_R4_1_*`,
  10 `test_R4_2_*`, 15 `test_R5_1_*`.
- **Committed:** the agent committed `spec.md` (`0d828ea`), which the round
  prompt approved. The user committed the Round 5 code, tests, and decisions
  (`1700d9e`..`af68558`). At handoff time, the Round 5 `history.md` entry, the
  new CLAUDE.md rule (rule 16), and this file were still uncommitted. Run
  `git status` to see what has changed since.
- **Not hand-tested:** the agent did not run Round 5 in a real terminal. Nobody
  has checked that (a) the box is really white, not gray, in Git Bash/mintty
  through `winpty`, and (b) the box moves correctly on all three menus.
  `main.py` imports cleanly, and an ASCII render of the button layouts looked
  right. The Round 4 zoom and resize behavior is also still not hand-tested.

## Files

| File                                   | Purpose                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `logic.py`                             | Pure logic, with no curses import. Settings (timers, word count, percentile scale, custom-file limits, R4 layout constants and zoom tips, **(R5)** `BUTTON_GAP = 3`), the word lists, `generate_text()`, `_hard_text()`, `TypingTest`, `calculate_wpm()`, `percent_beaten()`, `wrap_positions()`, the R2 custom-file functions, `zoom_tip()`, `centered_positions()`, and **(R5)** `Button` (a namedtuple: `row, col, text, selected`), `button_labels()`, `move_selection()`, `vertical_menu_buttons()`, and `button_row()`. |
| `main.py`                              | The curses UI only. Color pairs `GREEN, RED, GREEN_BOX, RED_BOX`, **(R5)** `HIGHLIGHT` (black on white), `init_colors()`, **(R5)** `highlight_attr()` and `draw_buttons()`, `vertical_menu()`, `main_menu()`, `choose_difficulty()`, `ask_custom_text()`, `handle_resize()`, `countdown()`, `draw_test()`, `run_test()`, `show_results()`, and `app()`. `option_row()` (the old bracket row) was removed.                                                                                                                     |
| `tests/test_logic.py`                  | `unittest` tests for `logic.py`, named `test_R<round>_<n>_...`. Round 5 added `ButtonHighlightTests`.                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `samples/sample.txt`                   | A valid custom-test file, for trying R2.1 by hand.                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `docs/decisions/`                           | Y-statement records `0001`-`0008` (`0007` and `0008` are new this round).                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `spec.md`                              | The feature spec, updated this round with "Selectable buttons".                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `problem.md`                           | The problem statement and per-round requirements, tagged `R1.1` ... `R5.1`.                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `history.md`                           | A log of every session.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `arch-round-1.md` .. `handoff-round-4.md` | Older handoffs, now out of date.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |

## Program flow

```
app()
 └─ main_menu()  ── Esc ──> quit                       [white-box buttons]
     ├─ "standard" → choose_difficulty()               [white-box buttons]
     │      ├─ Esc → back to main_menu
     │      └─ easy / medium / hard ─────────────┐
     └─ "custom" → ask_custom_text()             │     [text field, no box]
          ├─ Esc → back to main_menu             │
          └─ valid file → text ──────────────────┤
                                                 ▼
        retry loop: countdown() → run_test(text) → show_results(..., difficulty)
             Retry → same mode again                   [white-box buttons]
             Menu  → back to main_menu
             Quit / Esc anywhere → exit
```

How a button is drawn (R5.1):

```
vertical_menu() / show_results()
   selected = logic.move_selection(selected, ±1, count)        # arrow keys
   buttons  = logic.vertical_menu_buttons(labels, selected, cols, rows)
           or logic.button_row(options, selected, cols, row)
   main.draw_buttons(stdscr, buttons)   # selected one → highlight_attr()
```

## How to run (Git Bash on Windows, in this order)

```bash
cd "/c/Users/kiril/OneDrive - DePaul University/Sophmore 26-27/Fall/CSC 299/csc299-main/typing-test-cli-app"
pip install windows-curses              # once only (Windows only)
python -m unittest discover tests -v    # run the tests: expect "Ran 90 tests ... OK"
winpty python main.py                   # play (winpty is needed in Git Bash)
```

On macOS or Linux, skip the pip install and `winpty` and use `python3`.

To check a button layout without curses:

```bash
python -c "import logic; print(logic.button_row(['Retry', 'Menu', 'Quit'], 1, 80, 12))"
```

## Round 5 decisions and why

The user chose these when asked:

| Decision                                                                                    | Why                                                                    |
| ------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **All three menus** get the white box (main, difficulty, results); the path field does not. | "All selectable buttons"; a text field is not a button.                |
| **Always white** (explicit black-on-white color pair), not reverse video.                   | Reverse video only looks white on a dark theme. See `docs/decisions/0007`.  |
| **No `[ ]` brackets** on the results screen.                                                | The box is enough, and the row no longer shifts. See `docs/decisions/0008`. |
| **Same width for every button in a menu.**                                                  | The box keeps its size and position as you move. See `docs/decisions/0008`. |
| **The agent committed `spec.md` only.**                                                     | The round prompt approved it.                                          |

The agent chose these itself. The user saw the list at the end of Round 5 but
has not confirmed them one by one:

- The white is **color 15** (bright white), because color 7 (`COLOR_WHITE`) is
  often light gray. It falls back to color 7 when `curses.COLORS <= 15`.
- A terminal **without colors** gets reverse video (`A_REVERSE`) instead.
- Labels are **left-aligned** inside the box (one leading space, padded with
  spaces up to the longest label + 2), so "1." and "2." line up.
- The results buttons are **3 columns apart** (`BUTTON_GAP`).
- Hover movement moved to **`logic.move_selection()`** (clamped, no wrap-around),
  so it is tested. Key behavior is unchanged.
- The **vertical menus stay on the same rows** as before: the first option one
  row above the middle (`rows // 2 - 1`), the title at `rows // 2 - 3`.
- `option_row()` was removed from `main.py`.
- spec.md now also lists the existing **"back to main menu"** results option.
- **Two decision records** instead of one, one per decision.

## Unresolved / open questions

- all resolved!

## Warnings for the next session

- **Standing rules are in CLAUDE.md**, including the new rule 16 (every button
  uses the R5.1 layout and `draw_buttons()`)
- **Requirement IDs:** new Round 6 bullets in problem.md should be tagged
  `R6.1`, `R6.2`, ... If they aren't tagged, ask before naming tests.
- **"Bigger font" can't be done in curses.** If a later requirement asks for a
  font, size, or style change, explain this limit and ask first, as in Round 4.
- **A new menu or button:** don't draw options with `centered()` and
  `A_REVERSE`. Pass the labels to `logic.vertical_menu_buttons()` or
  `logic.button_row()` and draw them with `main.draw_buttons()`, or the white
  box will be missing. Add `test_R<round>_*` tests for any new layout function.
- **Changing `button_labels()` padding or `BUTTON_GAP`:** the R5.1 tests check
  width = longest label + 2, one leading space, and a gap of exactly
  `BUTTON_GAP`. `test_R5_1_vertical_buttons_on_consecutive_rows_below_middle`
  expects rows 11, 12, 13 on a 24-row screen, so moving the menus breaks it
  without a real bug.
- **`A_REVERSE` is still used once**, for the fake cursor in the path field
  (`ask_custom_text()`). That one is not a button; leave it.
- **`init_colors()` calls `start_color()` without checking `has_colors()`**
  (this was already the case before Round 5). Only `highlight_attr()` checks it.
- **The test text is drawn at `centered_positions()`**, not `wrap_positions()`
  directly. Wrapping changes go in `wrap_positions()`, placement changes in
  `centered_positions()`; `test_R4_2_same_layout_as_wrap_just_shifted` checks
  that the two agree.
- **The `HardTextTests` use a fixed seed** (`random.Random(11)`). Changing
  `HARD_WORDS`, the `HARD_*_CHANCE` values, or the order of `rng` calls in
  `_hard_text()` can fail
  `test_R3_1_hard_contains_commas_sentence_ends_and_numbers` without a real bug.
- **Keep the calling conventions:** `generate_text(word_count, rng, difficulty=...)`
  (Round 1 tests pass the first two positionally), `run_test(stdscr, text)`
  needs the text built first, and `show_results(..., difficulty=None)` hides
  the difficulty line for custom tests.
- Git prints "LF will be replaced by CRLF" warnings on Windows. These are
  harmless.
