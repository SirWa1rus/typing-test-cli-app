# 0009. Twinkling stars in place of a rocket animation

- Status: accepted
- Date: 2026-11-22
- Round: 6 (requirement R6.1, animated "Get ready" screen)

## Y-statement

In the context of **the R6.1 "Get ready" animation, which started as a shaky
🚀 rocket with a thick fire trail, streaking stars, and a large planet**,
facing **a series of problems when the user ran it in Git Bash through winpty:
a terminal cannot rotate the emoji; the emoji showed as `*`; the fire looked
green (a color-numbering bug, see 0012); and a rocket drawn from colored
boxes did not appear**,
we decided **to drop the rocket, the fire, and the moving stars, and show a
calm night sky: stars that stay in fixed spots and twinkle (each cycles dim
gray `.` -> white `+` -> bold white `*` and back, with its own speed and
starting point so they don't blink together), behind the still Jupiter-style
planet**,
and neglected **the rocket in all its forms (rotated emoji, emoji flying
up-right, emoji with an ASCII fallback, box-art pixel rocket), a fire trail
(characters, then filled boxes), streaking stars, and stars that twinkle by
turning fully on and off at random**,
to achieve **an animation that uses only plain characters and the colors that
already worked on the user's terminal (the planet), so it shows reliably, and
looks like a real sky**,
accepting **that the original rocket idea is gone (problem.md's R6.1 bullet was
rewritten to match), that the twinkle is a fixed repeating pattern rather than
truly random, and that "dim" needs a gray color because `A_DIM` does nothing
on Windows curses.**

Dropping the rocket and making the stars twinkle in place were the user's
choices. The twinkle steps and speeds, gray for dim stars, and hiding the
stars behind the planet were the agent's.

## Alternatives considered

| Option | Why not chosen |
| --- | --- |
| Rocket (emoji, ASCII, or box art) | Did not show correctly for the user; they scrapped it. |
| Fire trail | Scrapped by the user. |
| Streaking (moving) stars | The user wanted them to twinkle instead. |
| Random on/off blinking | Looks like flicker rather than twinkle, and is harder to test. |
| Stars in front of the planet | With still stars, the planet should hide the stars behind it. |

## Where it lives

`logic.TWINKLE`, `logic.TWINKLE_SPEEDS`, `logic.star_field()`, and
`main.STAR_STYLE`, `main.draw_cells()`, tested by the `test_R6_1_stars_*`,
`test_R6_1_every_star_twinkles`, and `test_R6_1_twinkle_*` tests.
