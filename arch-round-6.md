# Handoff: end of Round 6

For a fresh session starting the next round. Read `CLAUDE.md` first: it holds
the standing rules for every session (commits, test names, decision records,
Git Bash, winpty, history.md, layout math in logic.py, buttons (rule 16, now
**brackets**), and, new this round, **rules 17-19: colors by name, ASCII only,
animations**). This file
describes the state of the project at the end of Round 6. It replaces
`arch-round-5.md` and the older handoffs; where they disagree, this file is
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
- **Round 5 (done):** mark the hovered button on every menu (**R5.1**).
  Round 5 did this with a white box; **R6.2 replaced the box with brackets.**
- **Round 6 (done):**
  - **R6.1, animated "Get ready" screen:** during the 5-second countdown before
    every test (standard and custom), the screen shows a night sky:
    - **Twinkling stars** in fixed spots. Each cycles gray `.` -> white `+` ->
      bold white `*` and back, at its own speed and starting point, so they
      don't blink together. They are hidden behind the planet.
    - **A very large Jupiter-style planet**, centered and still, in shades of
      purple and blue: many thin bands whose edges wave up and down a row, and
      a big oval "Great Spot" (bright purple core, dark purple rim) below the
      middle, right of center.
    - **Text** at the top ("Get ready..." on row 1, the countdown number on
      row 2) and the bottom (the zoom tip, then "Esc: quit"). Text that lands
      on the planet gets the planet's color behind it, so it has no black box.
  - **R6.2, brackets instead of the white box (changes R5.1):** on the main
    menu, the difficulty menu, and the results screen, the option the user is
    on is marked `[ Retry ]` (square brackets, a space inside). The other
    options have spaces in the same places, and every button in a menu is the
    same width (longest option + 4), so only the brackets move; the option
    text never shifts. The white box is gone completely (no color, no bold).
    The custom-file path field is a text field and has no brackets.

    ```
         [ 1. Standard typing test ]          [ Retry ]     Menu        Quit
           2. Custom typing test                Retry     [ Menu ]      Quit
    ```
  - problem.md's R6.1 bullet is the user's short version: "stars in the
    background that stay in place and twinkle, and a very large purple and blue
    planet designed to look like Jupiter (R6.1)". **spec.md has the full
    detail.**
- **Tests:** 114 logic tests, all passing: 14 `test_R1_1_*`, 2 `test_R1_2_*`,
  3 `test_R1_3_*`, 25 `test_R2_1_*`, 17 `test_R3_1_*`, 4 `test_R4_1_*`,
  10 `test_R4_2_*`, 11 `test_R5_1_*`, 19 `test_R6_1_*`, 9 `test_R6_2_*`.
  (R6.2 replaced the four R5.1 tests that checked the white-box layout.)
- **Committed:** for R6.1, the agent committed only `spec.md`, five times, as
  the spec changed (`c96371e`, `5a6bc7d`, `597334b`, `4c424d1`, `0ea0320`); the
  round prompt approved that. The user committed problem.md (`19bd1b9`), the
  code and tests (`2d8233c`), and the decision records (`5a5bc42`). For R6.2,
  added after the handoff was first written, the user asked the agent to
  commit everything except `history.md` in small steps: problem.md
  (`1745022`), spec.md (`dc33494`), logic.py + tests (`66e6075`), main.py
  (`e3dae05`), decisions (`119eb09`), CLAUDE.md (`1d4421a`), and this file.
  **`history.md` is left uncommitted for the user.** Run `git status` to see
  what has changed since.
- **Not hand-tested:** the user ran several earlier versions of the animation
  (that is how the bugs below were found), but has **not yet confirmed the
  final version** (twinkling stars + Jupiter) in a real terminal, and **has
  not seen the R6.2 brackets** yet. The agent checked the bracket text with a
  printed preview and a fake window only.

## How R6.1 got here (so the next session doesn't repeat it)

The original R6.1 asked for a shaky 🚀 rocket "rotated to point up", flying
straight up with a thick white/orange/yellow/red fire trail, streaking stars,
and a slowly moving planet. Each piece was built, run by the user, and changed:

| Version | What happened in the user's terminal | Outcome |
| --- | --- | --- |
| Emoji rocket flying up-right (a terminal can't rotate a character), fire made of characters, streaking stars | Black boxes behind characters on the planet | Fixed: planet-colored backgrounds; fire as filled boxes, no red; planet made still |
| Same, with box fire | **Fire looked green**; **rocket showed as `*`** | Green: color-numbering bug, fixed (rule 17, decision 0012). Rocket redrawn as box pixel art; planet made Jupiter-style |
| Box-art rocket | The rocket **did not appear** | Back to the emoji; fire scrapped |
| Emoji rocket, no fire | (user scrapped it) | Rocket and moving stars scrapped; stars twinkle instead |

**Lessons:** emoji don't display in Git Bash + winpty (rule 18); raw color
numbers mean different colors on Windows (rule 17); `curses.A_DIM` is 0 on
Windows (rule 18). Why the box rocket didn't appear was **never diagnosed**:
the user did not run the emoji/box check script (`emoji_check.py`, kept only in
the agent's scratch folder, not in the project).

## Files

| File | Purpose |
| --- | --- |
| `logic.py` | Pure logic, with no curses import. Settings, word lists, `generate_text()`, `TypingTest`, scoring, `wrap_positions()`, the R2 custom-file functions, the R4 layout (`zoom_tip()`, `centered_positions()`), the buttons (`Button`, **(R6.2)** `BRACKET_OPEN`, `BRACKET_CLOSE`, `NO_BRACKET`, `button_labels(options, selected)`, `move_selection()`, `vertical_menu_buttons()`, `button_row()`), and **(R6)** the animation: `FRAME_SECONDS`, `BOX`, `STAR_SEED`, `STAR_CELLS_PER_STAR`, `TWINKLE`, `TWINKLE_SPEEDS`, `PLANET_SIZE`, `PLANET_BANDS`, `PLANET_BANDS_ACROSS`, `PLANET_WAVE_LENGTH`, `SPOT_CORE`, `SPOT_RIM`, `PLANET_COLORS`, `Cell` (namedtuple `row, col, char, color`), `animation_frame()`, `countdown_text_rows()`, `star_field()`, `planet_spot()`, `planet_cells()`, `planet_background()`. Now also imports `math`. |
| `main.py` | The curses UI only. **(R6.2)** the white box is removed: no `HIGHLIGHT` pair, `highlight_attr()`, or `BRIGHT_WHITE`; `draw_buttons()` prints the button text as is. **(R6.1)** `animation_colors()` (color name -> curses color number), `init_animation_colors()` (pairs from 6 up), `CELL_ATTRS`, `ON_PLANET`, `STAR_STYLE`, `NO_COLOR_PLANET`, `over_planet()`, `draw_cells()`, `centered_over_planet()`, `draw_get_ready_animation()`, and a rewritten `countdown()`. Everything else is as in Round 5. |
| `tests/test_logic.py` | `unittest` tests for `logic.py`. Round 6 added `GetReadyAnimationTests` (R6.1) and `ButtonBracketTests` (R6.2, replacing four white-box tests in `ButtonHighlightTests`), and moved the `if __name__ == "__main__"` block to the end of the file (it used to sit before the R5 tests). |
| `decisions/` | Y-statement records `0001`-`0013` (`0009`-`0013` are new this round; `0007` is now marked superseded by `0013`, and `0008` amended by it). |
| `spec.md` | The feature spec, with the new "Get ready" screen section. |
| `problem.md` | The problem statement and per-round requirements, tagged `R1.1` ... `R6.2`. |
| `history.md` | A log of every session. |
| `samples/sample.txt` | A valid custom-test file, for trying R2.1 by hand. |
| `arch-round-1.md` .. `arch-round-5.md` | Older handoffs, now out of date. |

## Program flow

```
app()
 └─ main_menu()  ── Esc ──> quit                       [ bracket buttons ]
     ├─ "standard" → choose_difficulty()               [ bracket buttons ]
     │      ├─ Esc → back to main_menu
     │      └─ easy / medium / hard ─────────────┐
     └─ "custom" → ask_custom_text()             │     [text field, no box]
          ├─ Esc → back to main_menu             │
          └─ valid file → text ──────────────────┤
                                                 ▼
        retry loop: countdown() → run_test(text) → show_results(..., difficulty)
             Retry → same mode again                   [ bracket buttons ]
             Menu  → back to main_menu
             Quit / Esc anywhere → exit
```

How one countdown frame is drawn (R6.1), every 50 ms:

```
countdown()
   frame      = logic.animation_frame(seconds since start)      # 20 per second
   background = logic.planet_background(cols, rows)             # {(row, col): color}
   draw_get_ready_animation(stdscr, frame)
       draw_cells(logic.star_field(cols, rows, frame))          # stars first...
       draw_cells(logic.planet_cells(cols, rows))               # ...then the planet
   centered_over_planet(...) for each logic.countdown_text_rows() entry
```

How a button is drawn (R5.1 layout, R6.2 brackets):

```
vertical_menu() / show_results()
   selected = logic.move_selection(selected, +1 or -1, count)    # arrow keys
   buttons  = logic.vertical_menu_buttons(labels, selected, cols, rows)
           or logic.button_row(options, selected, cols, row)     # "[ Retry ]" built in
   main.draw_buttons(stdscr, buttons)                            # plain text
```

## How to run (Git Bash on Windows, in this order)

```bash
cd "/c/Users/kiril/OneDrive - DePaul University/Sophmore 26-27/Fall/CSC 299/csc299-main/typing-test-cli-app"
pip install windows-curses              # once only (Windows only)
python -m unittest discover tests -v    # run the tests: expect "Ran 114 tests ... OK"
winpty python main.py                   # play (winpty is needed in Git Bash)
```

Start any test to see the animation during the 5-second countdown. On macOS
or Linux, skip the pip install and `winpty` and use `python3`.

To check the bracket buttons without curses:

```bash
python -c "import logic; print([b.text for b in logic.button_row(['Retry', 'Menu', 'Quit'], 1, 80, 12)])"
```

To check a frame without curses (prints the stars, with `#` for the planet):

```bash
python -c "
import logic
g = [[' '] * 80 for _ in range(24)]
for c in logic.planet_cells(80, 24): g[c.row][c.col] = '#'
for c in logic.star_field(80, 24, 0): g[c.row][c.col] = c.char
print('\n'.join(''.join(r) for r in g))"
```

## Round 6 decisions and why

The user chose these when asked or when giving feedback:

| Decision | Why |
| --- | --- |
| **Requirement ID R6.1** for the whole bullet. | Like R4.1 and R5.1. |
| **R6.2** for the bracket bullet, tagged in problem.md. | Round 6, bullet 2. |
| **`[ Retry ]` brackets with a space inside**, on **all three menus**, with the white box **removed completely**. | The user's new requirement and choices. See `decisions/0013`. |
| **The agent commits the R6.2 work in small steps, except `history.md`.** | The user asked. |
| **Twinkling stars that stay in place; no rocket, no fire, no moving stars.** | After the rocket and fire didn't work in Git Bash. See `decisions/0009`. |
| **Jupiter look in purple and blue** (not Jupiter's real tan/brown colors). | Keeps R6.1's "purple and blue planet". |
| **The planet is centered and stays still.** | It is far away. |
| **No black boxes behind characters on the planet.** | They looked bad. See `decisions/0011`. |
| **Remove the tests for removed features** (including a guard test checking the rocket and fire stayed removed). | The user asked. |
| **The agent committed `spec.md` only.** | The round prompt approved it. |

The agent chose these itself. The user saw them at the end of each change but
has not confirmed them one by one:

- **Twinkle:** steps `(".", dim)`, `(".", dim)`, `("+", normal)`,
  `("*", bright)`, `("+", normal)`, `(".", dim)`, at 3-6 frames per step (one
  twinkle takes about 0.9-1.8 s). The pattern is fixed per frame, not random.
- **Dim stars are gray** (`COLOR_BLACK + 8`), because `A_DIM` does nothing on
  Windows. Normal stars are white, bright ones bold white.
- **Stars are hidden behind the planet**, not drawn on top of it
  (`decisions/0011`).
- About **one star per 40 screen cells**, the same pattern every countdown
  (`STAR_SEED = 299`).
- **20 frames per second**, with every frame computed from the frame number
  alone (`decisions/0010`).
- **The countdown text moved** from the middle of the screen to rows 1-2 and
  the last two rows; "Get ready..." is now bold.
- **Planet:** radius 45% of the screen's smaller side, about 10 bands, band
  edges waving one row, spot below and right of center with its own shades.
  256-color shades: purples 93 / 141 / 54 / 170, blues 27 / 75 / 18, falling
  back to magenta / bright magenta / blue / bright blue.
- **Colors by curses name, + 8 for bright** (`decisions/0012`, now CLAUDE.md
  rule 17), to fix the green fire.
- Without colors, the planet is drawn with `:` characters.
- **Four decision records** (0009-0012), and 0009 was rewritten and renamed as
  the design changed (it was untracked at the time).
- **(R6.2)** The brackets are built into the button text in logic.py
  (`button_labels(options, selected)`), not added while drawing.
- **(R6.2)** The closing bracket sits right after the option's text; shorter
  options are padded with spaces after it (`"[ Menu ] "`).
- **(R6.2)** Only the four R5.1 tests that checked the white-box layout were
  replaced (by nine `test_R6_2_*` tests); the other eleven R5.1 tests still
  describe the layout and were kept.
- **(R6.2)** Decision `0007` was marked superseded and `0008` amended by `0013`.
- **(R6.2)** Color pair 5 (the old white box) is left unused, so the animation
  pairs still start at 6.

## Unresolved / open questions

- **Final animation not confirmed** in the user's terminal (see "Not hand-tested").
- **Dim text does nothing on Windows.** The hint lines that use `curses.A_DIM`
  ("Esc: quit", the zoom tip, the menu hints, the difficulty line on the
  results screen) have never looked dim on the user's machine. Not fixed; the
  user hasn't decided whether to.
- **Two known test gaps** (from a mutation test the agent ran on a scratch
  copy, where 8 of 10 deliberate `logic.py` bugs were caught):
  nothing checks that `*` is labeled the *bright* twinkle step, or how fast
  the stars twinkle. The user decided not to add tests for now.
- **Why the box-art rocket didn't appear** was never found out (scrapped anyway).

## Warnings for the next session

- **Standing rules are in CLAUDE.md**, including rule 16, now about brackets,
  and new rules 17 (colors by name),
  18 (ASCII only, no `A_DIM`), and 19 (animations, and asking the user to look).
- **The tests never import main.py.** A broken, or even unparseable, `main.py`
  still passes all 114 tests (the agent checked this). Bugs in colors,
  drawing order, or timing are only found by running `winpty python main.py`.
  In Round 6, every bug the user hit was a UI bug that the tests passed.
- **Expect design changes after the user runs it.** R6.1 changed five times
  after the user saw it running. Build in small steps, ask the user to run
  each step, and don't build a big feature fully before they've seen it.
- **Text over the planet:** use `centered_over_planet(..., background)`, not
  `centered()`, for anything drawn on the countdown screen, or it will show a
  black box on the planet.
- **Color pairs:** 1-4 are the typing colors, 5 is unused (it was the R5.1
  white box), and 6 upward are made in a loop by
  `init_animation_colors()` (6-23 today). Add new pairs after the loop,
  or add the color to `animation_colors()`. `animation_colors()` also makes an
  unused solid-white box pair for `"white"`; that's harmless.
- **Buttons (R6.2):** `button_labels()` now needs the selected index, and a
  button's text includes its brackets or the spaces for them. The tests check
  width = longest option + 4, `"[ "` at the start of the selected label only,
  the closing bracket right after the text, and that the option text stays in
  the same column as the hover moves. Changing `BRACKET_OPEN`,
  `BRACKET_CLOSE`, `NO_BRACKET`, or `BUTTON_GAP` can fail them without a real
  bug. `test_R5_1_vertical_buttons_on_consecutive_rows_below_middle` still
  expects rows 11, 12, 13 on a 24-row screen.
- **The planet tests use an 80x24 screen and set thresholds:** at least 6 color
  changes down the middle column, wavy edges on more than 5 rows, an area over
  20% of the screen, and the spot below and right of center. Changing
  `PLANET_SIZE`, `PLANET_BANDS`, `PLANET_BANDS_ACROSS`, the wave, or
  `planet_spot()` can fail them without a real bug.
- **The star tests depend on `STAR_SEED = 299`** and on the planet's shape
  (stars under the planet are dropped). `test_R6_1_enough_stars_and_on_screen`
  expects more than 15 visible stars on 80x24.
- **Weak tests:** `test_R6_1_twinkle_goes_dim_normal_bright` and
  `test_R6_1_text_at_top_and_bottom` mostly restate constants, and
  `test_R6_1_planet_stays_still` can't really fail (the planet function takes
  no frame number).
- **Still true from Round 5:** new menus must use the button functions
  (rule 16), or they will have no brackets; `A_REVERSE` is still used once, for the fake cursor in the path
  field; `init_colors()` calls `start_color()` without checking `has_colors()`;
  the test text is drawn at `centered_positions()`; the `HardTextTests` use a
  fixed seed (`random.Random(11)`); keep the calling conventions
  `generate_text(word_count, rng, difficulty=...)`, `run_test(stdscr, text)`,
  `show_results(..., difficulty=None)`.
- **Requirement IDs:** new Round 7 bullets should be tagged `R7.1`, `R7.2`, ...
  If they aren't tagged, ask before naming tests.
- **"Bigger font" can't be done in curses.** If a later requirement asks for a
  font, size, or style change, explain this limit and ask first, as in Round 4.
- Git prints "LF will be replaced by CRLF" warnings on Windows. These are harmless.
