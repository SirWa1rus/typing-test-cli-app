# 0013. Mark the hovered button with [ ] brackets instead of a white box

- Status: accepted
- Date: 2026-11-22
- Round: 6 (requirement R6.2, which changes R5.1)
- Supersedes: 0007 (white box as an explicit color pair). Amends: 0008
  (equal-width buttons: still equal width, now with bracket space instead of
  box padding).

## Y-statement

In the context of **showing which selectable button the user is on (main menu,
difficulty menu, results screen), which Round 5 did with a black-on-white box
(R5.1, decision 0007)**,
facing **the user's new requirement R6.2 to "change white boxes to be brackets",
and the Round 5 lesson that a button marker must not make the row shift as the
user moves (decision 0008)**,
we decided **to remove the white box completely and mark the hovered option
with square brackets and a space inside, "[ Retry ]", on all three menus; the
other options get spaces where the brackets would be, every label is padded to
the longest option + 4, and the closing bracket sits right after the option's
text; `logic.button_labels(options, selected)` now builds the brackets into
each button's text, and `main.draw_buttons()` just prints it**,
and neglected **tight brackets "[Retry]" (the pre-Round 5 look), arrow markers
"> Retry <", brackets plus a bold highlight, brackets on the results screen
only, and adding the brackets in main.py while drawing**,
to achieve **a marker that looks the same on every terminal (no colors needed,
so none of the white-versus-gray or Windows color issues), buttons whose text
never moves (only the brackets move), and bracket placement that is checked by
unit tests**,
accepting **that the marker stands out less than a filled white box, that each
button is two columns wider than in Round 5, that a short option's closing
bracket leaves trailing spaces inside the button's width, that
`button_labels()` changed its signature (it now needs the selected index),
and that color pair 5 is left unused.**

The bracket look ("[ Retry ]"), all three menus, removing the box completely,
and the ID R6.2 were the user's choices. Putting the brackets in logic.py,
the closing bracket right after the text, and keeping R5.1's layout tests
(rewriting only the four white-box ones as R6.2 tests) were the agent's.

## Alternatives considered

| Option | Why not chosen |
| --- | --- |
| Keep the white box | R6.2 replaces it. |
| "[Retry]" (no inner space) | The user picked "[ Retry ]". |
| "> Retry <" | The user picked square brackets. |
| Brackets + bold | The user chose brackets only. |
| Results screen only | The user chose all three menus. |
| Add brackets in main.py | Breaks CLAUDE.md rule 15 (layout in logic.py, tested). |

## Where it lives

`logic.BRACKET_OPEN`, `logic.BRACKET_CLOSE`, `logic.NO_BRACKET`,
`logic.button_labels()`, `logic.vertical_menu_buttons()`, `logic.button_row()`,
and `main.draw_buttons()`, tested by the `test_R6_2_*` tests (class
`ButtonBracketTests`) and the remaining `test_R5_1_*` layout tests.
