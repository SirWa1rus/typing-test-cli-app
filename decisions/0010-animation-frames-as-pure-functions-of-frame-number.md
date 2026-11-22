# 0010. Each animation frame is a pure function of the frame number

- Status: accepted
- Date: 2026-11-22
- Round: 6 (requirement R6.1, animated "Get ready" screen)

## Y-statement

In the context of **drawing the R6.1 animation (twinkling stars, a still
planet) about 20 times a second during the
countdown**,
facing **CLAUDE.md rules 10 and 15 (no curses in logic.py, layout math in
logic.py and tested), and that random twinkling and changing frames are hard to
test if they depend on hidden state or the clock**,
we decided **to compute every frame from just the screen size and a frame
number (`animation_frame(elapsed)`, 20 per second), with
`star_field()` and `planet_cells()` in logic.py returning
`Cell(row, col, char, color_name)` lists; the stars get fixed spots, speeds,
and twinkle starting points from a fixed seed, and their look in a frame is
worked out from the frame number,
and `main.py` only maps color names to curses colors and draws the cells back
to front**,
and neglected **an animation object that updates its own state every tick,
calling `random` directly in main.py, and drawing the animation inside main.py
with no layout functions**,
to achieve **an animation whose every frame can be checked by unit tests
(direction, colors, clipping to the screen, the planet staying
centered), that stays smooth if a frame is skipped, and that redraws correctly
right after the terminal is resized**,
accepting **that each frame rebuilds every cell from scratch (a few hundred
cells, cheap at 20 frames per second), that the star pattern is the same
every countdown, and that the real colors (especially the purple and blue
shades, which need a 256-color terminal) can only be checked by eye.**

This was the agent's decision.

## Alternatives considered

| Option | Why not chosen |
| --- | --- |
| Stateful animation object | Needs a sequence of updates to test; skipping or resizing breaks it. |
| `random` called in main.py | Not testable (rule 6: logic tests only). |
| Drawing math in main.py | Breaks rules 10 and 15. |

## Where it lives

`logic.Cell`, `logic.animation_frame()`,
`logic.star_field()`, `logic.planet_cells()`,
`logic.countdown_text_rows()`, and `main.init_animation_colors()`,
`main.draw_cells()`, `main.draw_get_ready_animation()`, `main.countdown()`,
tested by the `test_R6_1_*` tests.
