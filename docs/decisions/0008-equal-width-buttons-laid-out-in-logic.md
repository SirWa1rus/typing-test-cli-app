# 0008. Equal-width buttons, laid out by pure functions in logic.py

- Status: accepted, amended by 0013 (Round 6, R6.2: labels are padded for [ ] brackets instead of the white box)
- Date: 2026-11-22
- Round: 5 (requirement R5.1, white box behind the hovered button)

## Y-statement

In the context of **drawing a white box behind the hovered button (R5.1) on
the vertical menus and the results row**,
facing **labels of different lengths (so a box that fits each label changes
size as you move), the old results row that marked the current option with
`[ ]` brackets and shifted text around them, and CLAUDE.md rule 15 (layout math
goes in logic.py and is tested)**,
we decided **to pad every button in a menu to the same width (one space, the
label, then spaces up to the longest label plus two), drop the brackets, and
compute each button's row, column, text, and "selected" flag in
`logic.button_labels()`, `logic.vertical_menu_buttons()`, and
`logic.button_row()`, with hover movement in `logic.move_selection()`**,
and neglected **boxes sized to each label, keeping the brackets as well as the
box, and leaving the layout inside `main.py`**,
to achieve **a box that keeps its size and place as the user moves, buttons
that never shift, and layout and hover rules that are checked by unit tests
without opening a terminal**,
accepting **a little extra white space after short labels inside the box, and
that the screen code now depends on a `Button` tuple from logic.py.**

Equal widths and dropping the brackets were the user's choices. Left-aligning
the label inside the box, the 3-column gap between row buttons, and the
`Button` tuple were the agent's.

## Alternatives considered

| Option | Why not chosen |
| --- | --- |
| Each box fits its label | The box grows and shrinks while moving, which looks jumpy. |
| Keep `[ ]` and the box | Two signals for one thing; the brackets made the row shift. |
| Layout stays in main.py | Breaks rule 15 and can't be unit-tested. |

## Where it lives

`logic.Button`, `logic.BUTTON_GAP`, `logic.button_labels()`,
`logic.vertical_menu_buttons()`, `logic.button_row()`, `logic.move_selection()`,
and `main.draw_buttons()`, tested by the `test_R5_1_*` tests.
