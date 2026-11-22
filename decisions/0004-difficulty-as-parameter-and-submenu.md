# 0004. Choose difficulty in a submenu, pass it as a parameter

- Status: accepted
- Date: 2026-11-21
- Round: 3 (requirement R3.1, medium and hard difficulty)

## Y-statement

In the context of **letting the user pick Easy, Medium, or Hard for the standard
typing test (R3.1)**,
facing **a main menu that already offers Standard and Custom, existing Round 1
code and tests that call `generate_text()` with no difficulty, and the rule that
`logic.py` stays free of UI code**,
we decided **to show a second menu (Easy / Medium / Hard) after the user picks
Standard, with Esc going back to the main menu, and to pass the choice to
`logic.generate_text()` as a `difficulty` parameter that defaults to `"easy"`**,
and neglected **listing all four choices (three standard levels plus Custom) on
the main menu, and writing a separate function for each level
(`generate_easy_text()`, `generate_medium_text()`, ...)**,
to achieve **a main menu that stays short, a difficulty menu that only appears
where it applies (custom tests have no difficulty), and Round 1 callers and
tests that keep working unchanged**,
accepting **one extra key press to start a standard test, and that a misspelled
difficulty is only caught when the program runs (it raises `ValueError`).**

The submenu was the user's choice. The parameter with an Easy default was the
agent's.

## Where it lives

`main.choose_difficulty()`, `main.vertical_menu()`, `main.app()`, and
`logic.generate_text()` / `logic.DIFFICULTIES`, tested by
`test_R3_1_default_is_easy`, `test_R3_1_unknown_difficulty_rejected`, and
`test_R3_1_three_difficulties_in_order`.
