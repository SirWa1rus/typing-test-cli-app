# Chat history

## 2026-11-19: Session 1 (Claude Opus 5.5)

**User:** build the program in spec.md

**Agent:** Read spec.md, arch.md, and history.md (and skipped problem.md). It found gaps and asked four questions:

1. Where should the percentile data come from? **User:** a built-in average (bell curve of typical typists).
2. The spec says incorrect spaces show a green box. Is that a typo? **User:** yes, use a red box.
3. Allow Backspace during the test? **User:** yes.
4. Strict stdlib, or curses + windows-curses? **User:** curses + windows-curses.

**Agent:** Built `logic.py` (pure logic), `main.py` (curses UI), and `tests/test_logic.py` (19 logic tests, all passing). It updated arch.md with the architecture, decisions, and run steps. It asked permission before running any git commands.
