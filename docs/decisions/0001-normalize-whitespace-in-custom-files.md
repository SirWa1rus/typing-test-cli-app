# 0001. Normalize whitespace in custom .txt files

- Status: accepted
- Date: 2026-11-20
- Round: 2 (requirement R2, custom typing test)

## Y-statement

In the context of **loading a custom typing test from a user's .txt file (R2)**,
facing **the fact that almost every real .txt file has line breaks (at least a
trailing newline from the editor), possibly tabs or double spaces, while the
test screen only shows one long wrapped line typed with the space bar**,
we decided **to turn every run of whitespace (newlines, tabs, repeated spaces)
into a single space, trim both ends, and count the 40-400 character limit after
this cleanup**,
and neglected **rejecting any file that contains a line break, and keeping line
breaks as characters the user must type with Enter**,
to achieve **files saved by Notepad or VS Code working without the user having to
edit them, with the length rule matching exactly what is typed on screen**,
accepting **that the file's original line and paragraph layout is lost, and that
a file with lots of blank lines may pass the length check even though its raw
size is larger.**

## Alternatives considered

| Option | Why not chosen |
| --- | --- |
| Reject files containing newlines | Would reject nearly every file an editor saves (trailing newline), confusing users. |
| Keep newlines; Enter types them | Needs new display logic for line breaks and a new key rule; Enter is already the "select" key in menus. |
| Count length before cleanup | The rule would not match what's on screen: a 40-char file with blank lines could be "too long" for no visible reason. |

## Where it lives

`logic.normalize_custom_text()` and `logic.load_custom_text()`, tested by the
`test_R2_1_newlines_and_tabs_become_spaces`, `test_R2_1_trailing_newline_trimmed`,
and `test_R2_1_length_counted_after_cleanup` tests.
