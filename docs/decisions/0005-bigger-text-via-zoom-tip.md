# 0005. Make the text bigger with a zoom tip, not by redrawing it

- Status: accepted
- Date: 2026-11-21
- Round: 4 (requirement R4.1, bigger font in the typing tests)

## Y-statement

In the context of **making the typing test text bigger (R4.1)**,
facing **the fact that a curses program cannot change the terminal's font size
(the terminal, here Git Bash/mintty, owns the font), and that the test text is
about 60 words long**,
we decided **to show a tip on the countdown and test screens telling the user
to zoom the terminal (hold Ctrl and scroll, or Ctrl+= / Ctrl+-), with a short
version on narrow screens, and to redraw the layout when a zoom resizes the
terminal**,
and neglected **drawing each character as large block letters made of `█`
characters, spacing letters and lines out, and asking Windows to change the
console font through an OS call**,
to achieve **real, sharp, bigger text the user controls, with no change to how
typing, coloring, or wrapping work, and a layout that stays centered after
zooming**,
accepting **that the program does not make the text bigger by itself (the user
has to zoom), and that the zoom keys depend on the terminal (the tip uses the
ones that work in mintty and Windows Terminal).**

The tip approach was the user's choice. Showing it on both the countdown and
test screens, the short-tip fallback, and the resize handling were the agent's.

## Alternatives considered

| Option | Why not chosen |
| --- | --- |
| Block letters (3x5 glyphs of `█`) | Really bigger, but only about one short line fits at a time, so the text would have to scroll, and it needs a glyph for every keyboard character. |
| Spaced-out letters and lines | Easier to read, but the letters are not actually bigger. |
| Change the console font through an OS call | Only works in the old Windows console window, not in Git Bash/mintty, which this class uses. |

## Where it lives

`logic.ZOOM_TIP`, `logic.ZOOM_TIP_SHORT`, `logic.zoom_tip()`, and
`main.countdown()`, `main.draw_test()`, `main.handle_resize()`, tested by the
`test_R4_1_*` tests.
