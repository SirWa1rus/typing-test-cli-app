# Architecture / Handoff

Read `spec.md` for the feature list and `CLAUDE.md` for project rules.
(Do not read `problem.md`.)

## Status

v1 implemented (2026-11-19): every feature in `spec.md` is built, and the logic tests pass.

## Files

| File | Purpose |
|---|---|
| `logic.py` | Pure logic, with no curses import. It holds the settings constants, the easy word list, `generate_text()`, the `TypingTest` class (typed chars, per-char status, backspace, finished), `calculate_wpm()`, `percent_beaten()`, and `wrap_positions()` (maps each char to a (row, col) for display). |
| `main.py` | The curses UI. It runs the countdown screen, then the test screen, then the results screen (Retry/Quit menu). The loop is `app()`. |
| `tests/test_logic.py` | `unittest` tests for `logic.py` only. Per the project rules, we test logic only, not UI. |

## Flow

`app()` loops: `countdown()` (5 s), then `run_test()` (45 s, or until the text is fully typed), then `show_results()`, which returns `"retry"` or `"quit"`. Esc quits from any screen.

## Decisions made with the user (2026-11-19)

- **Percentile** uses a built-in bell curve (`statistics.NormalDist`), mean 40 WPM, SD 12 (`AVERAGE_WPM`, `WPM_SPREAD`). These are assumed population numbers, not measured data, and nothing is saved to disk.
- **Spaces:** a correct space shows a green box and an incorrect space shows a red box. The spec said green for both; the user confirmed red was intended for incorrect.
- **Backspace** is allowed during the test.
- **Library:** `curses`. On Windows this needs the `windows-curses` pip package. In Git Bash it must be run through `winpty`.

## Other implementation choices

- WPM is (correct chars / 5) / minutes elapsed. If the user finishes early, the actual elapsed time is used.
- The timer starts when the text appears, not on the first keystroke.
- The test text is 60 random easy words (`WORDS_PER_TEST`).
- The next character to type is underlined and bolded.
- `ESCDELAY=25` makes Esc respond instantly on Unix curses.
- `safe_addstr()` swallows `curses.error`, so a small terminal doesn't crash the app.

## How to run (Git Bash on Windows)

```bash
cd typing-test-cli-app
pip install windows-curses          # once only (Windows only)
python -m unittest discover tests -v   # run the logic tests
winpty python main.py               # play
```

## Possible next steps

- Difficulty levels (the spec only defines "easy").
- Save a score history, and show a personal best.
- Show accuracy % on the results screen.
