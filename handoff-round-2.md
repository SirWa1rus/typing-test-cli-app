# Handoff: end of Round 2

For a fresh session starting the next round. Read `CLAUDE.md` first: it holds
the standing rules for every session. This file describes the state of the
project at the end of Round 2. `arch-round-1.md` is the older
handoff from Round 1. Where the two disagree, this file is correct.

## Current state (2026-11-20)

- **Round 1 (done):** a timed standard typing test (5 s countdown, 45 s test, easy
  words). It colors each character green or red, gives a WPM score and a "you beat
  X% of people" figure, and shows a results screen.
- **Round 2 (done):** a custom typing test from a `.txt` file (requirement
  **R2.1**).
- **Tests:** 44 logic tests, all passing: 14 `test_R1_1_*` (working typing test),
  2 `test_R1_2_*` (WPM), 3 `test_R1_3_*` (percentile), and 25 `test_R2_1_*`
  (custom .txt test).
- **Not hand-tested:** the curses screens (the main menu, the path prompt, and
  Retry/Menu/Quit) were not tested by hand in a real terminal by the agent. The
  user should play through them once.
- **Uncommitted:** the user does all commits, and at handoff time the Round 2 work
  was still uncommitted. Run `git status` to see what has been committed since.

## Files

| File                  | Purpose                                                                                                                                                                                                                                                                                                                                                                                                       |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `logic.py`            | Pure logic with no curses import, so all of it can be unit tested. It holds the settings constants, `generate_text()`, `TypingTest`, `calculate_wpm()`, `percent_beaten()`, `wrap_positions()`, and **(R2)** `CustomTextError`, `clean_path_input()`, `normalize_custom_text()`, `is_keyboard_char()`, `validate_custom_text()`, `load_custom_text()`, `MIN_CUSTOM_CHARS = 40`, and `MAX_CUSTOM_CHARS = 400`. |
| `main.py`             | The curses UI only. It holds `main_menu()`, `ask_custom_text()`, `countdown()`, `run_test(stdscr, text)`, `show_results()` (which returns `"retry"`, `"menu"`, or `"quit"`), and `app()`.                                                                                                                                                                                                                     |
| `tests/test_logic.py` | `unittest` tests for `logic.py`. Each test name starts with its requirement ID, `R<round>.<n>` written as `test_R2_1_...` (see CLAUDE.md rule 8).                                                                                                                                                                                                                                                             |
| `samples/sample.txt`  | A valid custom-test file (130 characters after cleanup) for trying the feature by hand.                                                                                                                                                                                                                                                                                                                       |
| `docs/decisions/`          | Decision records written as Y-statements, numbered `0001-...`.                                                                                                                                                                                                                                                                                                                                                |
| `spec.md`             | The feature spec, already updated by the user for Round 2.                                                                                                                                                                                                                                                                                                                                                    |
| `problem.md`          | The problem statement and the requirements for each round, each tagged with its unique ID (`R1.1`, `R2.1`, ...).                                                                                                                                                                                                                                                                                              |
| `history.md`          | A log of every session's chat.                                                                                                                                                                                                                                                                                                                                                                                |
| `arch-round-1.md`     | The Round 1 handoff (renamed from `arch.md`), now out of date.                                                                                                                                                                                                                                                                                                                                                |

## Program flow

```
app()
 └─ main_menu()  ── Esc ──> quit
     ├─ "standard" ─────────────────────────────┐
     └─ "custom" → ask_custom_text()            │
          ├─ Esc → back to main_menu            │
          └─ valid file → text ─────────────────┤
                                                ▼
        retry loop: countdown() → run_test(text) → show_results()
             Retry → same mode again (the same custom text, or new random words)
             Menu  → back to main_menu
             Quit / Esc anywhere → exit
```

## How to run (Git Bash on Windows, in this order)

```bash
cd typing-test-cli-app
pip install windows-curses              # once only (Windows only)
python -m unittest discover tests -v    # run the tests: expect "Ran 44 tests ... OK"
winpty python main.py                   # play (winpty is needed in Git Bash)
```

On macOS or Linux, skip the pip install and `winpty` and use `python3`.

To try a custom test by hand: choose **2. Custom typing test** and enter
`samples/sample.txt`. Relative paths are resolved from the folder the program
was started in.

## Round 2 decisions and why

The user chose these when asked:

| Decision                                                                                                                                             | Why                                                                                                                             |
| ---------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Test IDs are unique per requirement: `R<round>.<n>`, as tagged in problem.md (e.g. `R2.1`), written `test_R2_1_...`.                                 | Plain round tags (`R1`, `R2`) were tried first but every Round 1 test shared "R1", so a name couldn't point to one requirement. |
| A custom test is timed like a standard one (5 s countdown, 45 s).                                                                                    | Keeps one consistent test flow and scoring.                                                                                     |
| Line breaks, tabs, and repeated spaces in the file become single spaces, and the ends are trimmed. The 40–400 count is taken **after** this cleanup. | Nearly every editor-saved file ends with a newline. The limit then matches what is shown on screen. See `docs/decisions/0001`.       |
| An invalid file shows a red error and the prompt asks again. Esc goes back to the menu.                                                              | Lets the user fix a typo without starting over.                                                                                 |
| Retry after a custom test reruns the **same** text. A **Menu** option was added to return to the Standard/Custom choice.                             | Lets the user practice the same passage.                                                                                        |
| Paths may be relative or absolute, and one pair of surrounding quotes is removed.                                                                    | Windows "Copy as path" adds quotes.                                                                                             |

The agent chose these itself, and the user has approved all of them:

- "Standard keyboard characters" means **printable ASCII** (space through `~`).
  Accented letters, emoji, and curly "smart quotes" are rejected.
- Files are read as **UTF-8, ignoring a BOM** (the invisible marker Notepad may
  add at the start of a file). A file that isn't valid UTF-8 is rejected as "not
  plain text".
- The `.txt` extension check ignores case.
- The error message for bad characters lists up to 5 of them.
- File problems are reported with one exception type, `CustomTextError`, whose
  message is shown to the user as is. See `docs/decisions/0002`.
- The main menu is vertical and accepts Up/Down, Left/Right, and the keys `1`/`2`.
- **Retry/Menu/Quit** is shown after standard tests too, not only custom ones.
- Long paths scroll in the input field, and a block marks the cursor.
- Tests create temporary files with `tempfile` rather than files in the repo.

## Unresolved / open questions

None at the end of Round 2.

## Warnings for the next session

- **The user does all git commits** (CLAUDE.md rule 1). Never commit, undo,
  amend, or stage anything. Read-only git commands (`git status`, `git log`,
  `git diff`) are fine without asking. List the changed files instead.
- **Requirement IDs are tagged in problem.md** (`R1.1`–`R1.3`, `R2.1`). When the
  user adds a Round 3 section, its bullets should be tagged `R3.1`, `R3.2`, ...
  If they aren't tagged, ask the user before naming tests.
- **Use Git Bash syntax**, not PowerShell. The project path contains spaces
  (`OneDrive - DePaul University/...`), so always quote it.
- **curses on Windows** needs `windows-curses` and must be run through `winpty`
  in Git Bash. Running `python main.py` without `winpty` fails with a
  "Redirection is not supported" style error.
- **Never import curses in `logic.py`.** The tests rely on it being pure. Put new
  rules in `logic.py` and only drawing and key reading in `main.py`.
- **Test only the logic** (CLAUDE.md rule 6). The UI is checked by playing it.
- `__pycache__/` is in `.gitignore`. An old tracked `.pyc` file was removed in
  commit `aa71d1a`, so it shouldn't come back. If it does, it is because a `.pyc`
  file is tracked again.
- Git prints "LF will be replaced by CRLF" warnings on Windows. These warnings
  are harmless.
- `run_test()` now **requires** a `text` argument. Any new test mode should build
  its text first, then call `run_test(stdscr, text)`.
