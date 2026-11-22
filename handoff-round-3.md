# Handoff: end of Round 3

For a fresh session starting the next round. Read `CLAUDE.md` first: it holds
the standing rules for every session (commits, test names, decision records,
Git Bash, winpty, history.md). This file describes the state of the project at
the end of Round 3. It replaces `handoff-round-2.md` and `arch-round-1.md`; where
they disagree, this file is correct.

## Current state (2026-11-21)

- **Round 1 (done):** a timed standard typing test (5 s countdown, 45 s test).
  Each character turns green or red as you type, and the results screen shows a
  WPM score and a "you beat X% of people" figure.
- **Round 2 (done):** a custom typing test from a `.txt` file (**R2.1**).
- **Round 3 (done):** Medium and Hard difficulty for the standard test
  (**R3.1**). Choosing Standard now opens an Easy / Medium / Hard menu.
- **Tests:** 61 logic tests, all passing: 14 `test_R1_1_*`, 2 `test_R1_2_*`,
  3 `test_R1_3_*`, 25 `test_R2_1_*`, 17 `test_R3_1_*`.
- **Committed:** the user committed all Round 3 code, tests, spec, and
  decisions (commits `05e509e`..`a19f8da`). At handoff time, the Round 3
  `history.md` entry, the CLAUDE.md rules 11-14, and this file were still
  uncommitted. Run `git status` to see what has changed since.
- **Not hand-tested:** the agent did not play the new difficulty menu or the
  "Difficulty:" line on the results screen in a real terminal. `main.py`
  imports cleanly, but the user should play through it once.

## Files

| File                                 | Purpose                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `logic.py`                           | Pure logic, with no curses import. It holds the settings, the `EASY_WORDS` / **(R3)** `MEDIUM_WORDS` / `HARD_WORDS` lists, the **(R3)** `EASY`, `MEDIUM`, `HARD`, and `DIFFICULTIES` constants, the `HARD_NUMBER_CHANCE` / `HARD_SENTENCE_CHANCE` / `HARD_COMMA_CHANCE` settings, `generate_text(word_count, rng, difficulty=EASY)`, **(R3)** `_hard_text()`, `TypingTest`, `calculate_wpm()`, `percent_beaten()`, `wrap_positions()`, and the R2 custom-file functions (`CustomTextError`, `clean_path_input()`, `normalize_custom_text()`, `is_keyboard_char()`, `validate_custom_text()`, `load_custom_text()`). |
| `main.py`                            | The curses UI only. It holds **(R3)** `vertical_menu(stdscr, title, options, esc_hint)` (a shared numbered menu that returns an index or `None`), `main_menu()`, **(R3)** `choose_difficulty()`, `ask_custom_text()`, `countdown()`, `run_test(stdscr, text)`, `show_results(stdscr, wpm, percent, difficulty=None)`, and `app()`.                                                                                                                                                                                                                                                                                  |
| `tests/test_logic.py`                | `unittest` tests for `logic.py`, named `test_R<round>_<n>_...`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `samples/sample.txt`                 | A valid custom-test file, for trying R2.1 by hand.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `docs/decisions/`                         | Y-statement records `0001`-`0004` (`0003` and `0004` are new this round).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `spec.md`                            | The feature spec, updated this round with the difficulty menu and levels.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `problem.md`                         | The problem statement and per-round requirements, tagged `R1.1`... `R3.1`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `history.md`                         | A log of every session.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `arch-round-1.md`, `handoff-round-2.md` | Older handoffs, now out of date.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |

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
```

## How to run (Git Bash on Windows, in this order)

```bash
cd "/c/Users/kiril/OneDrive - DePaul University/Sophmore 26-27/Fall/CSC 299/csc299-main/typing-test-cli-app"
pip install windows-curses              # once only (Windows only)
python -m unittest discover tests -v    # run the tests: expect "Ran 61 tests ... OK"
winpty python main.py                   # play (winpty is needed in Git Bash)
```

On macOS or Linux, skip the pip install and `winpty` and use `python3`.

To see sample text for each level without starting the game:

```bash
python -c "import logic; print(logic.generate_text(15, difficulty='hard'))"
```

## Round 3 decisions and why

The user chose these when asked:

| Decision                                                                                                                           | Why                                                                               |
| ---------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| **Medium** = longer, less common lowercase words. **Hard** = long words plus capitals, punctuation (`, . ? !`), and numbers.       | Difficulty should come from what you type, not only from word length.             |
| The difficulty is picked in a **submenu after Standard** (Easy / Medium / Hard). Esc goes back to the main menu.                   | Keeps the main menu short. Custom tests have no difficulty. See `docs/decisions/0004`. |
| **The same percentile scale** (average 40 WPM) for every difficulty.                                                               | Scores stay directly comparable. Harder text just tends to give a lower WPM.      |
| **Retry keeps the same difficulty** with new random words, and the results screen shows **"Difficulty: X"** (standard tests only). | You can practice a level repeatedly and see which level the score is for.         |

The agent chose these itself. The user saw the list at the end of Round 3 but
has not confirmed them one by one:

- How Hard text is built: random `HARD_WORDS` turned into sentences. About 10%
  of words become a number from 0 to 999, about 15% end a sentence with
  `.`/`?`/`!`, and about 15% get a comma. Each sentence starts with a capital
  letter, and the text always ends with sentence punctuation. See
  `docs/decisions/0003`. The percentages are `HARD_*_CHANCE` settings in `logic.py`.
- The agent picked the 100 Medium and 100 Hard words. Tests check that the lists
  have no duplicates, don't overlap each other or `EASY_WORDS`, and get longer
  on average from Easy to Medium to Hard.
- Hard uses only `HARD_WORDS`, never Medium words.
- Difficulty is a `difficulty=` setting on `generate_text()` that defaults to
  Easy, so Round 1 calls work unchanged. An unknown difficulty raises
  `ValueError`. See `docs/decisions/0004`.
- One shared `vertical_menu()` draws both menus. The difficulty menu takes
  number keys `1`-`3`, like the main menu.
- Word count (60) and timer (45 s) are the same for every difficulty, as
  spec.md says.

## Unresolved / open questions

- all resolved!

## Warnings for the next session

- **Standing rules are in CLAUDE.md.** Rules 11-14 were added at the end of
  Round 3 (read-only git is fine, never stage, use Git Bash with the path
  quoted, `winpty`, append to history.md).
- **Requirement IDs:** new Round 4 bullets in problem.md should be tagged
  `R4.1`, `R4.2`, ... If they aren't tagged, ask before naming tests.
- **The `HardTextTests` use a fixed seed** (`random.Random(11)`). The "contains
  commas, sentence ends and numbers" test passes because that seed happens to
  produce all three. If you change `HARD_WORDS`, the `HARD_*_CHANCE` values, or
  the order of `rng` calls in `_hard_text()`, the generated text changes. That
  test could then fail without any real bug, so check the seed before assuming
  the code is broken.
- **Changing a word list** can break `test_R3_1_word_lists_have_no_duplicates_or_overlap`
  (no word may appear in two lists) or `test_R3_1_word_lists_get_longer_with_difficulty`.
- **`generate_text()` is called with `difficulty=` as a keyword** in `main.py`.
  Keep `word_count` and `rng` as the first two arguments, because Round 1 tests
  pass them positionally.
- **`show_results()` takes `difficulty=None`.** Custom tests pass `None`, which
  hides the line. A new test mode should pass `None` or a value from
  `logic.DIFFICULTIES`.
- **`run_test()` requires a `text` argument.** Any new mode should build its
  text first, then call `run_test(stdscr, text)`.
- Git prints "LF will be replaced by CRLF" warnings on Windows. These are
  harmless.
