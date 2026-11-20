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
    8.  Every test name starts with the unique ID of the requirement it checks: R<round>.<n>, where <n> is the bullet number in that round's section of problem.md. Python names can't contain dots, so R2.1 is written test_R2_1_... A requirement is tested under the round it was built in.
    9.  Record design decisions that had real alternatives in decisions/ as Y-statements, in files numbered 0001-..., 0002-..., and so on.
    10. Keep logic.py free of curses/UI code so it stays fully unit-testable; main.py is UI only.
