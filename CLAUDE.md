# Rules for project:

    1.  The user does all git commits. Never commit, undo, or amend a commit; list the changed files instead.
    2.  Develop in python
    3.  Provide steps for running the program in git bash on windows (and in what order they should be run)
    4.  Some important files:

            -   history.md: a history of all chat messages between the user and the agent
            -   spec.md: program description + list of features

    5.  Handoff files are named arch-round-<#>.md. Write one only when the user asks. At the start of a round, read the newest one (it replaces older ones such as arch-round-1.md as the current handoff).
    6.  Build only tests for the project's logic
    7.  Interview the user for any missing information from the spec.md file during program development.
    8.  Every test name starts with the unique ID of the requirement it checks, as tagged in problem.md: R<round>.<n> (e.g. R2.1 = Round 2, bullet 1). Python names can't contain dots, so R2.1 is written test_R2_1_...
    9.  Record design decisions that had real alternatives in decisions/ as Y-statements, in files numbered 0001-..., 0002-..., and so on.
    10. Keep logic.py free of curses/UI code so it stays fully unit-testable; main.py is UI only.
    11. Read-only git commands (git status, git log, git diff) are fine without asking. Never stage files (git add) either; that is part of committing.
    12. Use Git Bash syntax, not PowerShell. The project path contains spaces (OneDrive - DePaul University/...), so always quote it.
    13. On Windows the curses UI needs `pip install windows-curses` (once) and must be started as `winpty python main.py` in Git Bash; without winpty it fails with a "Redirection is not supported" style error.
    14. At the end of each session, append a short dated entry to history.md (the user's requests, the questions asked and answers given, and what changed).
    15. Put layout math (where text goes on screen: wrapping, centering, sizes) in logic.py as pure functions that take the screen size, and test them; main.py only reads the screen size and draws at the positions logic.py returns.
