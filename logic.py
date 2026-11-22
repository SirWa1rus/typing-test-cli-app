"""Pure logic for the typing test: no screen/keyboard code lives here.

Keeping this separate from main.py (the curses UI) means every function here
can be tested with plain unit tests, without opening a terminal window.
"""

import os
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

# Limits for a custom .txt test (counted after the text is cleaned up).
MIN_CUSTOM_CHARS = 40
MAX_CUSTOM_CHARS = 400

# Typing test screen layout (R4).
TEXT_MAX_WIDTH = 60     # longest line of test text, in columns
SIDE_MARGIN = 2         # empty columns kept at the left and right screen edges
TEXT_TOP = 3            # first screen row the text may use (rows 0-2: title and timer)

# A terminal program can't change the terminal's font, so we tell the user how
# to zoom instead (works in Git Bash/mintty and Windows Terminal) (R4.1).
ZOOM_TIP = "Tip: hold Ctrl and scroll the mouse wheel (or press Ctrl+= / Ctrl+-) to make the text bigger"
ZOOM_TIP_SHORT = "Ctrl+scroll: bigger text"

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

# Longer, less common words for a "medium" test (all lowercase, no punctuation).
MEDIUM_WORDS = [
    "garden", "however", "simple", "travel", "number", "always", "letter", "answer", "change", "follow",
    "around", "family", "mother", "father", "school", "friend", "animal", "picture", "country", "between",
    "during", "before", "minute", "window", "market", "summer", "winter", "spring", "autumn", "yellow",
    "purple", "orange", "silver", "bright", "quiet", "gentle", "strong", "weather", "forest", "island",
    "river", "ocean", "valley", "bridge", "castle", "doctor", "farmer", "artist", "driver", "player",
    "kitchen", "bottle", "basket", "pocket", "button", "candle", "carpet", "ticket", "jacket", "blanket",
    "morning", "evening", "history", "general", "certain", "several", "perhaps", "almost", "already", "enough",
    "because", "believe", "develop", "explain", "imagine", "improve", "include", "measure", "prepare", "receive",
    "system", "problem", "program", "service", "subject", "student", "teacher", "company", "control", "nothing",
]

# Long words for a "hard" test. Hard text also adds capitals, punctuation, and numbers.
HARD_WORDS = [
    "knowledge", "different", "beautiful", "important", "especially",
    "government", "experience", "particular", "understand", "community",
    "development", "environment", "information", "technology", "international",
    "relationship", "opportunity", "performance", "political", "population",
    "professional", "significant", "traditional", "university", "yesterday",
    "absolutely", "according", "actually", "agreement", "apartment",
    "attention", "available", "background", "boundary", "calculate",
    "challenge", "character", "chocolate", "collection", "comfortable",
    "committee", "completely", "condition", "conference", "consider",
    "continue", "contract", "creative", "critical", "currently",
    "dangerous", "decision", "definitely", "democracy", "describe",
    "discovery", "discussion", "education", "electricity", "emergency",
    "encourage", "equipment", "establish", "evidence", "exercise",
    "exchange", "existence", "expensive", "familiar", "favorite",
    "frequently", "generation", "happiness", "hospital", "identity",
    "immediately", "increase", "independent", "individual", "industry",
    "interesting", "investment", "language", "literature", "magazine",
    "maintain", "marriage", "material", "medicine", "mountain",
    "necessary", "neighbor", "obviously", "operation", "ordinary",
    "organize", "original", "otherwise", "pleasant", "possible",
]

# Difficulty levels for the standard test, in the order the menu shows them.
EASY = "easy"
MEDIUM = "medium"
HARD = "hard"
DIFFICULTIES = (EASY, MEDIUM, HARD)

# How often hard text adds extras (each is a chance per word, from 0 to 1).
HARD_NUMBER_CHANCE = 0.10     # a word is replaced by a number from 0 to 999
HARD_SENTENCE_CHANCE = 0.15   # a word ends a sentence with . ? or !
HARD_COMMA_CHANCE = 0.15      # a word is followed by a comma

# Character states returned by TypingTest.status()
UNTYPED = "untyped"
CORRECT = "correct"
INCORRECT = "incorrect"


# --- Test text ----------------------------------------------------------------

def generate_text(word_count=WORDS_PER_TEST, rng=None, difficulty=EASY):
    """Return `word_count` random words for `difficulty`, joined by single spaces.

    easy and medium are plain lowercase words; hard is turned into sentences
    (see _hard_text). `rng` lets tests pass a seeded random.Random so the
    output is predictable. An unknown difficulty raises ValueError.
    """
    rng = rng or random.Random()
    if difficulty == EASY:
        return " ".join(rng.choice(EASY_WORDS) for _ in range(word_count))
    if difficulty == MEDIUM:
        return " ".join(rng.choice(MEDIUM_WORDS) for _ in range(word_count))
    if difficulty == HARD:
        return _hard_text(word_count, rng)
    raise ValueError(f"Unknown difficulty: {difficulty!r}")


def _hard_text(word_count, rng):
    """Random HARD_WORDS made to look like sentences.

    Each sentence starts with a capital letter and ends with . ? or !, some
    words get a comma after them, and some words are swapped for numbers.
    The last word always ends the final sentence.
    """
    tokens = []
    new_sentence = True
    for i in range(word_count):
        if rng.random() < HARD_NUMBER_CHANCE:
            token = str(rng.randint(0, 999))
        else:
            token = rng.choice(HARD_WORDS)
            if new_sentence:
                token = token.capitalize()
        is_last = i == word_count - 1
        new_sentence = is_last or rng.random() < HARD_SENTENCE_CHANCE
        if new_sentence:
            token += rng.choice(".?!")
        elif rng.random() < HARD_COMMA_CHANCE:
            token += ","
        tokens.append(token)
    return " ".join(tokens)


# --- Custom test text (from a .txt file) ------------------------------------------

class CustomTextError(Exception):
    """Raised when a custom .txt file can't be used. str(error) is shown to the user."""


def clean_path_input(raw):
    """Tidy a path the user typed: trim spaces and one pair of surrounding quotes.

    Windows "Copy as path" wraps paths in double quotes, so we accept that.
    """
    path = raw.strip()
    if len(path) >= 2 and path[0] == path[-1] and path[0] in "\"'":
        path = path[1:-1].strip()
    return path


def normalize_custom_text(raw):
    """Turn line breaks and tabs into spaces, collapse repeated spaces, trim the ends."""
    return " ".join(raw.split())


def is_keyboard_char(ch):
    """True for characters on a standard US keyboard: printable ASCII (space to ~)."""
    return " " <= ch <= "~"


def validate_custom_text(text):
    """Return an error message if `text` can't be a test, or None if it's fine.

    `text` should already be normalized.
    """
    bad = sorted({ch for ch in text if not is_keyboard_char(ch)})
    if bad:
        shown = " ".join(repr(ch) for ch in bad[:5])
        return f"File has characters not on a standard keyboard: {shown}"
    if not MIN_CUSTOM_CHARS <= len(text) <= MAX_CUSTOM_CHARS:
        return (f"File has {len(text)} characters; it needs "
                f"{MIN_CUSTOM_CHARS}-{MAX_CUSTOM_CHARS}.")
    return None


def load_custom_text(raw_path):
    """Read, clean, and check a custom .txt file. Returns the test text.

    Raises CustomTextError with a user-friendly message if anything is wrong.
    A relative path is looked up from the folder the program was run in.
    """
    path = clean_path_input(raw_path)
    if not path:
        raise CustomTextError("Please type a path to a .txt file.")
    if not path.lower().endswith(".txt"):
        raise CustomTextError("The file must end in .txt")
    if not os.path.isfile(path):
        raise CustomTextError(f"No file found at: {path}")
    try:
        # utf-8-sig also strips the invisible "BOM" marker Notepad may add.
        with open(path, encoding="utf-8-sig") as f:
            raw = f.read()
    except UnicodeDecodeError:
        raise CustomTextError("The file isn't plain text (couldn't read it as UTF-8).")
    except OSError as e:
        raise CustomTextError(f"Couldn't open the file: {e.strerror}")
    text = normalize_custom_text(raw)
    error = validate_custom_text(text)
    if error:
        raise CustomTextError(error)
    return text


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


# --- Screen layout (R4) --------------------------------------------------------

def zoom_tip(width):
    """The zoom tip that fits in `width` columns: the full one, a short one, or ""."""
    for tip in (ZOOM_TIP, ZOOM_TIP_SHORT):
        if len(tip) <= width:
            return tip
    return ""


def centered_positions(text, screen_cols, screen_rows):
    """Where to draw each character of `text` so the text sits in the middle.

    The text is wrapped into lines at most TEXT_MAX_WIDTH wide (less on a
    narrow screen, keeping SIDE_MARGIN free on each side). The lines keep a
    straight left edge, and that whole block is centered left-to-right and
    top-to-bottom, but never starts above row TEXT_TOP (the title and timer).

    Returns one (screen_row, screen_col) pair per character of `text`.
    """
    width = min(TEXT_MAX_WIDTH, screen_cols - 2 * SIDE_MARGIN)
    positions = wrap_positions(text, width)
    if not positions:
        return []
    block_width = max(col for _, col in positions) + 1
    block_height = positions[-1][0] + 1
    left = max(0, (screen_cols - block_width) // 2)
    top = max(TEXT_TOP, (screen_rows - block_height) // 2)
    return [(top + row, left + col) for row, col in positions]
