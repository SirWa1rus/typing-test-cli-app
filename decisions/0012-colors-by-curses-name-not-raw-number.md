# 0012. Pick basic colors by curses name (+ 8 for bright), never by raw number

- Status: accepted
- Date: 2026-11-22
- Round: 6 (requirement R6.1, animated "Get ready" screen)

## Y-statement

In the context of **coloring the R6.1 animation: at the time a fire trail (white, yellow,
orange), and the Jupiter-style planet (many shades of purple and blue)**,
facing **a bug the user saw when running it: the fire looked green, because the
code asked for color number 11 ("bright yellow" in the usual terminal order),
but the Windows curses library (PDCurses) numbers colors in the Windows console
order, where 11 is bright cyan; also, the in-between shades (orange, the
purples, the blues) only exist on 256-color terminals**,
we decided **to choose every basic color by curses' own constant
(`COLOR_YELLOW`, `COLOR_RED`, ...), make a "bright" color as that constant
+ 8 (true in both orders, when the terminal has 16 or more colors), use
256-color numbers (208 orange, 93/141/54/170 purples, 27/75/18 blues) only
when `curses.COLORS` is larger than the number, and otherwise fall back to the
nearest basic color; all of this lives in one function, `main.animation_colors()`**,
and neglected **hard-coding raw numbers like 11 (the bug), detecting the platform
and keeping two color tables, and using only the 8 basic colors**,
to achieve **colors that are the same on Windows and on other systems (the
fire was later removed at the user's request, but the stars' white and gray
and the planet still rely on this), and a planet with several distinct purples and blues on 256-color
terminals**,
accepting **that on a 16-color terminal several planet shades look the same, that 256-color numbers are assumed to follow the
standard xterm palette, and that colors still can't be unit-tested (rule 6),
only simulated (the agent checked the Windows order with a fake curses).**

This was the agent's decision, made to fix the green fire the user reported.

## Alternatives considered

| Option | Why not chosen |
| --- | --- |
| Raw numbers (e.g. 11 for bright yellow) | Different colors on Windows: the green-fire bug. |
| Separate Windows and other-system tables | Twice the code; the constants already handle the order. |
| Only the 8 basic colors | The Jupiter bands would have just two shades. |

## Where it lives

`main.animation_colors()`, `main.init_animation_colors()`. The R5.1 white box
uses color 15, which is bright white in both orders, so it was not affected.
