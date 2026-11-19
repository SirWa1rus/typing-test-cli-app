"""Pure logic for the typing test: no screen/keyboard code lives here.

Keeping this separate from main.py (the curses UI) means every function here
can be tested with plain unit tests, without opening a terminal window.
"""

import random
from statistics import NormalDist

# --- Settings -----------------------------------------------------------------

COUNTDOWN_SECONDS = 5   # countdown before the test appears
TEST_SECONDS = 45       # length of the typing test
WORDS_PER_TEST = 60     # how many words the test text contains

# Assumed "typical typist" speeds, used for the "you beat X% of people" number.
# These are rough estimates of the general population, not measured data.
AVERAGE_WPM = 40
WPM_SPREAD = 12         # standard deviation of the bell curve

# A standard "word" in WPM calculations is 5 characters (spaces included).
CHARS_PER_WORD = 5

# Short, common words for an "easy" test.
EASY_WORDS = [
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "it",
    "for", "not", "on", "with", "he", "as", "you", "do", "at", "this",
    "but", "his", "by", "from", "they", "we", "say", "her", "she", "or",
    "an", "will", "my", "one", "all", "would", "there", "their", "what", "so",
    "up", "out", "if", "about", "who", "get", "which", "go", "me", "when",
    "make", "can", "like", "time", "no", "just", "him", "know", "take", "people",
    "into", "year", "your", "good", "some", "could", "them", "see", "other", "than",
    "then", "now", "look", "only", "come", "its", "over", "think", "also", "back",
    "after", "use", "two", "how", "our", "work", "first", "well", "way", "even",
    "new", "want", "any", "these", "give", "day", "most", "us", "is", "was",
    "are", "has", "had", "been", "were", "said", "each", "many", "made", "find",
    "long", "down", "did", "more", "very", "where", "much", "too", "own", "same",
    "tell", "need", "home", "big", "high", "keep", "last", "let", "put", "old",
    "help", "hand", "small", "end", "play", "run", "move", "live", "place", "read",
]

# Character states returned by TypingTest.status()
UNTYPED = "untyped"
CORRECT = "correct"
INCORRECT = "incorrect"


# --- Test text ----------------------------------------------------------------

def generate_text(word_count=WORDS_PER_TEST, rng=None):
    """Return `word_count` random easy words joined by single spaces.

    `rng` lets tests pass a seeded random.Random so the output is predictable.
    """
    rng = rng or random.Random()
    return " ".join(rng.choice(EASY_WORDS) for _ in range(word_count))


# --- Typing state ---------------------------------------------------------------

class TypingTest:
    """Tracks the target text and what the user has typed so far."""

    def __init__(self, target):
        self.target = target
        self.typed = []

    @property
    def cursor(self):
        """Index of the next character the user will type."""
        return len(self.typed)

    def type_char(self, ch):
        """Record one typed character (ignored once the text is complete)."""
        if not self.is_finished():
            self.typed.append(ch)

    def backspace(self):
        """Remove the last typed character, if there is one."""
        if self.typed:
            self.typed.pop()

    def is_finished(self):
        return len(self.typed) >= len(self.target)

    def status(self, index):
        """Return UNTYPED, CORRECT, or INCORRECT for the character at `index`."""
        if index >= len(self.typed):
            return UNTYPED
        return CORRECT if self.typed[index] == self.target[index] else INCORRECT

    def correct_count(self):
        """How many typed characters match the target."""
        return sum(1 for i in range(len(self.typed)) if self.status(i) == CORRECT)


# --- Scoring -------------------------------------------------------------------

def calculate_wpm(correct_chars, seconds):
    """Words per minute, counting only correctly typed characters.

    WPM = (correct characters / 5) / minutes
    """
    if seconds <= 0:
        return 0.0
    return (correct_chars / CHARS_PER_WORD) / (seconds / 60)


def percent_beaten(wpm, average=AVERAGE_WPM, spread=WPM_SPREAD):
    """Percentage (0-100) of typical typists who score lower than `wpm`.

    Uses a bell curve (normal distribution) centered on `average`.
    """
    return NormalDist(mu=average, sigma=spread).cdf(wpm) * 100


# --- Layout --------------------------------------------------------------------

def wrap_positions(text, width):
    """Lay `text` out in lines at most `width` columns wide, breaking at spaces.

    Returns a list with one (row, col) pair per character of `text`, so the UI
    knows exactly where to draw character i. Each space stays at the end of
    the line it follows. A word longer than `width` is split mid-word.
    """
    width = max(1, width)
    positions = []
    row = col = 0
    words = text.split(" ")
    for i, word in enumerate(words):
        token = word + (" " if i < len(words) - 1 else "")
        if col > 0 and col + len(token) > width:
            row, col = row + 1, 0
        for _ in token:
            if col >= width:
                row, col = row + 1, 0
            positions.append((row, col))
            col += 1
    return positions
