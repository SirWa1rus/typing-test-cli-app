# 0002. Report custom-file problems with one exception type

- Status: accepted
- Date: 2026-11-20
- Round: 2 (requirement R2, custom typing test)

## Y-statement

In the context of **checking a custom .txt file in `logic.py` and showing the
problem to the user in `main.py`**,
facing **many different ways a file can be bad (empty path, wrong extension,
missing file, not UTF-8, non-keyboard characters, too short or long) and the
rule that `logic.py` must not contain any screen code**,
we decided **to have `load_custom_text()` either return the cleaned text or raise
a single `CustomTextError` whose message is the user-facing explanation**,
and neglected **returning a `(text, error)` pair, and returning error codes that
`main.py` turns into messages**,
to achieve **one `try/except` in the UI that shows `str(error)` in red and asks
again, with every message testable in `tests/test_logic.py` without curses**,
accepting **that the wording of the messages lives in the logic layer, and that
callers who forget the `try/except` would crash instead of silently getting a
bad value.**

## Where it lives

`logic.CustomTextError`, `logic.load_custom_text()`, and `main.ask_custom_text()`.
