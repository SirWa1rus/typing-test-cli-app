# 0006. Center the test text as one block at most 60 columns wide

- Status: accepted
- Date: 2026-11-21
- Round: 4 (requirement R4.2, centered typing test text)

## Y-statement

In the context of **centering the typing test text between the screen edges
(R4.2, `|-++-|`)**,
facing **text that used to be wrapped to the full screen width (so on a wide
screen "centering" would change nothing), and a cursor that moves from the end
of one line to the start of the next as you type**,
we decided **to wrap the text to at most 60 columns (less on narrow screens,
keeping 2 free columns at each edge), keep the lines' left edges lined up, and
center that whole block left-to-right and top-to-bottom, never above the
title and timer**,
and neglected **centering each line by itself, and keeping full-width lines
with only margins added**,
to achieve **text that visibly sits in the middle of any screen size, a short
line length that is easy to read, and the start of every line in the same
column, so the eye knows where the next line begins**,
accepting **that the right edge of the block is ragged, so the block is only
centered to within one column, and that on very wide screens a lot of space is
left empty.**

The centered block and vertical centering were the user's choices. The
60-column cap, the 2-column side margin, and centering by the widest line
(rather than by the 60-column cap) were the agent's.

## Alternatives considered

| Option | Why not chosen |
| --- | --- |
| Each line centered by itself | Line starts would jump around, so after each line break the typist has to hunt for where the next line begins. |
| Full-width lines with margins | Already almost what Round 1 did; on a wide terminal the text would not look centered, and very long lines are harder to read. |

## Where it lives

`logic.centered_positions()`, `logic.TEXT_MAX_WIDTH`, `logic.SIDE_MARGIN`,
`logic.TEXT_TOP`, and `main.draw_test()`, tested by the `test_R4_2_*` tests.
