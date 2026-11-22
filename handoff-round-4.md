# Handoff: end of Round 4

For a fresh session starting the next round. Read `CLAUDE.md` first: it holds
the standing rules for every session (commits, test names, decision records,
Git Bash, winpty, history.md). This file describes the state of the project at
the end of Round 4. It replaces `handoff-round-3.md` and the older handoffs; where
they disagree, this file is correct.

## Current state (2026-11-21)

- **Round 1 (done):** a timed standard typing test (5 s countdown, 45 s test).
  Each character turns green or red as you type, and the results screen shows a
  WPM score and a "you beat X% of people" figure.
- **Round 2 (done):** a custom typing test from a `.txt` file (**R2.1**).
- **Round 3 (done):** Easy / Medium / Hard difficulty for the standard test
  (**R3.1**).
- **Round 4 (done):**
  - **R4.1, bigger font:** a curses program can't change the terminal's font,
    so the countdown and test screens show a tip on how to zoom the terminal
    (Ctrl+scroll, or Ctrl+= / Ctrl+-). Narrow screens get a shorter tip, and
    screens too narrow for even that get none. The screen redraws after a zoom.
  - **R4.2, centered text:** the test text is a left-aligned block of lines at
    most 60 columns wide, centered left-to-right and top-to-bottom, never
    above the title and timer.
- **Tests:** 75 logic tests, all passing: 14 `test_R1_1_*`, 2 `test_R1_2_*`,
  3 `test_R1_3_*`, 25 `test_R2_1_*`, 17 `test_R3_1_*`, 4 `test_R4_1_*`,
  10 `test_R4_2_*`.
- **Committed:** the agent committed `spec.md` (`ed2940f`), the one exception
  the user allowed. The user committed the Round 4 code, tests, and decisions
  (`b55f88d`..`84edd59`). At handoff time, the Round 4 `history.md` entry, the
  new CLAUDE.md rules 15-16, and this file were still uncommitted. Run
  `git status` to see what has changed since.
- **Not hand-tested:** the agent did not play Round 4 in a real terminal. In
  particular, nobody has checked that (a) Ctrl+scroll zooms in Git Bash/mintty
  through `winpty`, and (b) the screen redraws correctly after a zoom
  (`handle_resize()`). `main.py` imports cleanly, and an ASCII render of
  `centered_positions()` looked centered.

## Files

| File                                   | Purpose                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `logic.py`                             | Pure logic, with no curses import. Settings (timers, word count, percentile scale, custom-file limits, **(R4)** `TEXT_MAX_WIDTH = 60`, `SIDE_MARGIN = 2`, `TEXT_TOP = 3`, `ZOOM_TIP`, `ZOOM_TIP_SHORT`), the word lists, `generate_text(word_count, rng, difficulty=EASY)`, `_hard_text()`, `TypingTest`, `calculate_wpm()`, `percent_beaten()`, `wrap_positions()`, the R2 custom-file functions (`CustomTextError`, `load_custom_text()`, ...), and **(R4)** `zoom_tip(width)` and `centered_positions(text, screen_cols, screen_rows)`. |
| `main.py`                              | The curses UI only. `vertical_menu()`, `main_menu()`, `choose_difficulty()`, `ask_custom_text()`, **(R4)** `handle_resize(key)`, `countdown()` (now shows the tip), `draw_test()` (now draws at `centered_positions()` with the tip on the bottom row), `run_test(stdscr, text)`, `show_results(stdscr, wpm, percent, difficulty=None)`, and `app()`.                                                                                                                                                                                      |
| `tests/test_logic.py`                  | `unittest` tests for `logic.py`, named `test_R<round>_<n>_...`. Round 4 added `ZoomTipTests` and `CenteredPositionsTests`.                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `samples/sample.txt`                   | A valid custom-test file, for trying R2.1 by hand.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `docs/decisions/`                           | Y-statement records `0001`-`0006` (`0005` and `0006` are new this round).                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `spec.md`                              | The feature spec, updated this round with "Typing test screen layout".                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `problem.md`                           | The problem statement and per-round requirements, tagged `R1.1` ... `R4.2`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `history.md`                           | A log of every session.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `arch-round-1.md` .. `handoff-round-3.md` | Older handoffs, now out of date.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |

## Program flow

```
app()
 └─ main_menu()  ── Esc ──> quit
     ├─ "standard" → choose_difficulty()
     │      ├─ Esc → back to main_menu
     │      └─ easy / medium / hard ─────────────┐
     └─ "custom" → ask_custom_text()             │
          ├─ Esc → back to main_menu             │
          └─ valid file → text ──────────────────┤
                                                 ▼
        retry loop: countdown() → run_test(text) → show_results(..., difficulty)
             Retry → same mode again (same custom text, or new words at the same difficulty)
             Menu  → back to main_menu
             Quit / Esc anywhere → exit

countdown() and run_test() call handle_resize() on every key; a resize just
causes a redraw, because every screen re-reads getmaxyx() each frame.
```

## How to run (Git Bash on Windows, in this order)

```bash
cd "/c/Users/kiril/OneDrive - DePaul University/Sophmore 26-27/Fall/CSC 299/csc299-main/typing-test-cli-app"
pip install windows-curses              # once only (Windows only)
python -m unittest discover tests -v    # run the tests: expect "Ran 75 tests ... OK"
winpty python main.py                   # play (winpty is needed in Git Bash)
```

On macOS or Linux, skip the pip install and `winpty` and use `python3`.

To check the centered layout without curses (prints where each character goes):

```bash
python -c "import logic; print(logic.centered_positions('hello there world', 80, 24))"
```

## Round 4 decisions and why

The user chose these when asked:

| Decision                                                                                    | Why                                                                                                                             |
| ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **R4.1 is a zoom tip on screen**, not block letters, spaced-out text, or an OS font call.   | Curses can't change the font. The tip gives real, sharp, bigger text without changing typing or wrapping. See `docs/decisions/0005`. |
| **R4.2 centers one block** (lines keep a straight left edge), not each line separately.     | The start of each line stays in the same column, so the typist doesn't hunt for the next line. See `docs/decisions/0006`.            |
| **Centered vertically too**, but never above the title and timer.                           | The text sits in the middle of the screen.                                                                                      |
| **The agent committed `spec.md` only**, even though CLAUDE.md rule 1 says the user commits. | A one-time exception, because the round prompt asked for it. Now covered by CLAUDE.md rule 15.                                  |

The agent chose these itself. The user saw the list at the end of Round 4 but
has not confirmed them one by one:

- Lines are at most **60 columns** (`TEXT_MAX_WIDTH`), with **2 empty columns**
  kept at each screen edge (`SIDE_MARGIN`).
- The block is centered by its **widest actual line** (not by the 60-column
  limit), so it is centered to within one column.
- On a screen too short to center vertically, the text starts at **row 3**
  (`TEXT_TOP`, moved from `main.py` to `logic.py`).
- The tip shows on **both** the countdown screen (under the number) and the
  test screen (dim, bottom row). The full tip is about 95 characters, so on a
  typical 80-column window the short tip `Ctrl+scroll: bigger text` appears.
- The tip names **Ctrl+scroll** because it should work in both mintty and
  Windows Terminal. This was not tested.
- `handle_resize()` calls `curses.resize_term(0, 0)` **only on Windows**
  (PDCurses needs it; ncurses updates the size by itself). It is used only on
  the countdown and test screens, not the menus or results screen.

## Unresolved / open questions

- all resolved!

## Warnings for the next session

- **Standing rules are in CLAUDE.md**, including the new rule 15 (layout math goes in
  `logic.py`).
- **Requirement IDs:** new Round 5 bullets in problem.md should be tagged
  `R5.1`, `R5.2`, ... If they aren't tagged, ask before naming tests.
- **"Bigger font" can't be done in curses.** If a later requirement asks for
  font, size, or style changes, explain this limit and ask first, as in Round 4.
- **The test text is no longer drawn at `wrap_positions()` directly.**
  `draw_test()` uses `centered_positions()`, which wraps to
  `min(TEXT_MAX_WIDTH, screen_cols - 2 * SIDE_MARGIN)` and then shifts the
  whole block. A change to wrapping should go in `wrap_positions()`; a change
  to placement, in `centered_positions()`. `test_R4_2_same_layout_as_wrap_just_shifted`
  checks that the two agree.
- **Changing `TEXT_MAX_WIDTH`, `SIDE_MARGIN`, or `TEXT_TOP`** is safe for the
  R4 tests (they read the constants), but `test_R4_2_short_text_centered_by_its_own_width`
  and `test_R4_2_vertically_centered` use fixed screen sizes. A very large
  `TEXT_TOP` could break them without a real bug.
- **Changing `ZOOM_TIP` or `ZOOM_TIP_SHORT`:** the R4.1 tests require both to
  contain `"Ctrl"` and the full tip to contain `"bigger"`, and the short tip
  must be shorter than the full one.
- **The `HardTextTests` use a fixed seed** (`random.Random(11)`). Changing
  `HARD_WORDS`, the `HARD_*_CHANCE` values, or the order of `rng` calls in
  `_hard_text()` changes the text and can fail
  `test_R3_1_hard_contains_commas_sentence_ends_and_numbers` without a real bug.
- **Keep the calling conventions:** `generate_text(word_count, rng, difficulty=...)`
  (Round 1 tests pass the first two positionally), `run_test(stdscr, text)`
  needs text built first, and `show_results(..., difficulty=None)` hides the
  difficulty line for custom tests.
- Git prints "LF will be replaced by CRLF" warnings on Windows. These are
  harmless.
