# 0007. Draw the hover box as an explicit black-on-white color pair

- Status: superseded by 0013 (Round 6, R6.2: brackets replaced the white box)
- Date: 2026-11-22
- Round: 5 (requirement R5.1, white box behind the hovered button)

## Y-statement

In the context of **showing which selectable button the user is on with a white
box (R5.1)**,
facing **the existing menus' reverse video (`A_REVERSE`), which only swaps the
terminal's own colors, so it is white on a dark theme but dark on a light theme,
and the fact that curses' `COLOR_WHITE` (color 7) is light gray in many
terminals**,
we decided **to add a `HIGHLIGHT` color pair of black text on bright white
(color 15, or color 7 when the terminal has fewer than 16 colors) and use it for
the selected button on all three menus, falling back to reverse video only when
the terminal has no colors**,
and neglected **keeping reverse video, and using `COLOR_WHITE` (color 7) as the
background**,
to achieve **a box that is white on any terminal theme, as the requirement says,
with the same look on the main menu, difficulty menu, and results screen**,
accepting **one more color pair to set up, that on a light-themed terminal the
white box stands out less against the white background, and that a terminal
with no colors still shows reverse video instead of white.**

The always-white box was the user's choice. Using color 15 instead of color 7,
and the no-color fallback, were the agent's.

## Alternatives considered

| Option | Why not chosen |
| --- | --- |
| Keep `A_REVERSE` | Only white on dark themes; the requirement asks for white. |
| `COLOR_WHITE` (7) background | Often shown as light gray, not white. |

## Where it lives

`main.HIGHLIGHT`, `main.init_colors()`, `main.highlight_attr()`, and
`main.draw_buttons()`. The colors can't be unit-tested (CLAUDE.md rule 6:
logic tests only); the `test_R5_1_*` tests check which button is selected.
