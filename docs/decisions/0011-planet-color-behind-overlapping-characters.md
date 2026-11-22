# 0011. Text over the planet gets the planet's color; stars hide behind it

- Status: accepted
- Date: 2026-11-22
- Round: 6 (requirement R6.1, animated "Get ready" screen)

## Y-statement

In the context of **the R6.1 animation, where the countdown text can land on
the large Jupiter-style planet, and stars are scattered across the sky**,
facing **the fact that a curses cell has exactly one background color, so a
character drawn with the terminal's default background shows as a black box
on the planet (which the user asked to remove)**,
we decided **to compute a `{(row, col): planet color}` map in
`logic.planet_background()`, draw every text character that lands on the
planet with a "white on that planet color" color pair, and leave out any star
that would sit on the planet (the stars are far away, behind it), while the
planet itself is solid filled boxes (a space whose text and background colors
match)**,
and neglected **drawing stars in front of the planet with the planet's color
behind them (used earlier this round, when the stars streaked past a rocket),
drawing the planet only as text characters with no background color, and
leaving the black boxes**,
to achieve **text that sits on the planet with no black box, and a sky where the
planet hides the stars behind it, as a real one would**,
accepting **one more color pair per planet shade, that text over the planet is
always white (not the terminal's own text color), that the planet's map is
rebuilt each frame (cheap, a few hundred cells), and that there are fewer
stars on screen than the star count, because some are hidden.**

Removing the black boxes was the user's choice. The planet-colored text
background and hiding the stars behind the planet were the agent's.

## Alternatives considered

| Option | Why not chosen |
| --- | --- |
| Stars in front, with the planet's color behind them | Fit moving stars; still stars look right behind the planet. |
| Planet as characters only | Not a solid planet; still has gaps of terminal background. |
| Leave the black boxes | The user asked for them to go. |

## Where it lives

`logic.planet_background()`, `logic.star_field()`, `main.ON_PLANET`,
`main.over_planet()`, `main.centered_over_planet()`, tested by
`test_R6_1_background_*` and `test_R6_1_stars_are_behind_the_planet`.
