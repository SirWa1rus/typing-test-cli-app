"""Tests for logic.py. Each test name starts with its requirement ID from
problem.md: test_R<round>_<n>_... (e.g. test_R2_1_... is Round 2, bullet 1).

Run from the project folder with:

    python -m unittest discover tests -v
"""

import os
import random
import tempfile
import unittest

import logic


class GenerateTextTests(unittest.TestCase):
    def test_R1_1_word_count(self):
        text = logic.generate_text(10, random.Random(1))
        self.assertEqual(len(text.split(" ")), 10)

    def test_R1_1_uses_only_easy_words(self):
        text = logic.generate_text(50, random.Random(2))
        for word in text.split(" "):
            self.assertIn(word, logic.EASY_WORDS)

    def test_R1_1_same_seed_same_text(self):
        a = logic.generate_text(20, random.Random(42))
        b = logic.generate_text(20, random.Random(42))
        self.assertEqual(a, b)


class TypingTestTests(unittest.TestCase):
    def test_R1_1_starts_untyped(self):
        t = logic.TypingTest("hi there")
        self.assertEqual(t.cursor, 0)
        self.assertEqual(t.status(0), logic.UNTYPED)
        self.assertFalse(t.is_finished())

    def test_R1_1_correct_and_incorrect(self):
        t = logic.TypingTest("ab c")
        t.type_char("a")
        t.type_char("x")
        t.type_char("_")   # wrong character where a space belongs
        self.assertEqual(t.status(0), logic.CORRECT)
        self.assertEqual(t.status(1), logic.INCORRECT)
        self.assertEqual(t.status(2), logic.INCORRECT)
        self.assertEqual(t.status(3), logic.UNTYPED)
        self.assertEqual(t.correct_count(), 1)

    def test_R1_1_correct_space(self):
        t = logic.TypingTest("a b")
        t.type_char("a")
        t.type_char(" ")
        self.assertEqual(t.status(1), logic.CORRECT)

    def test_R1_1_backspace_fixes_mistake(self):
        t = logic.TypingTest("ab")
        t.type_char("a")
        t.type_char("x")
        t.backspace()
        self.assertEqual(t.status(1), logic.UNTYPED)
        t.type_char("b")
        self.assertEqual(t.correct_count(), 2)

    def test_R1_1_backspace_when_empty_does_nothing(self):
        t = logic.TypingTest("ab")
        t.backspace()
        self.assertEqual(t.cursor, 0)

    def test_R1_1_finished_and_extra_keys_ignored(self):
        t = logic.TypingTest("ab")
        for ch in "abc":
            t.type_char(ch)
        self.assertTrue(t.is_finished())
        self.assertEqual(t.cursor, 2)


class ScoringTests(unittest.TestCase):
    def test_R1_2_wpm_formula(self):
        # 250 correct chars = 50 words, in 60 seconds -> 50 WPM
        self.assertAlmostEqual(logic.calculate_wpm(250, 60), 50.0)
        # 150 chars = 30 words in 45 s (0.75 min) -> 40 WPM
        self.assertAlmostEqual(logic.calculate_wpm(150, 45), 40.0)

    def test_R1_2_wpm_zero_time(self):
        self.assertEqual(logic.calculate_wpm(100, 0), 0.0)

    def test_R1_3_percent_at_average_is_half(self):
        self.assertAlmostEqual(logic.percent_beaten(logic.AVERAGE_WPM), 50.0)

    def test_R1_3_percent_increases_with_speed(self):
        self.assertLess(logic.percent_beaten(20), logic.percent_beaten(60))

    def test_R1_3_percent_stays_in_range(self):
        self.assertGreaterEqual(logic.percent_beaten(0), 0)
        self.assertLessEqual(logic.percent_beaten(300), 100)


class WrapPositionsTests(unittest.TestCase):
    def test_R1_1_one_position_per_character(self):
        text = "the cat sat on the mat"
        self.assertEqual(len(logic.wrap_positions(text, 10)), len(text))

    def test_R1_1_fits_on_one_line(self):
        self.assertEqual(logic.wrap_positions("ab cd", 20),
                         [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)])

    def test_R1_1_breaks_at_space(self):
        # width 6: "ab cd " fits (6 cols), "ef" moves to row 1
        pos = logic.wrap_positions("ab cd ef", 6)
        self.assertEqual(pos[6], (1, 0))   # 'e'
        self.assertEqual(pos[5], (0, 5))   # the space before 'ef'

    def test_R1_1_never_exceeds_width(self):
        text = logic.generate_text(40, random.Random(3))
        for row, col in logic.wrap_positions(text, 15):
            self.assertLess(col, 15)

    def test_R1_1_long_word_is_split(self):
        pos = logic.wrap_positions("abcdefgh", 3)
        self.assertEqual(pos[3], (1, 0))


# --- R2.1: custom typing test from a .txt file ---------------------------------------

VALID_TEXT = "The quick brown fox jumps over the lazy dog, twice!"  # 51 chars


class CleanPathInputTests(unittest.TestCase):
    def test_R2_1_trims_spaces(self):
        self.assertEqual(logic.clean_path_input("  a.txt  "), "a.txt")

    def test_R2_1_strips_double_quotes(self):
        self.assertEqual(logic.clean_path_input('"C:/x y/a.txt"'), "C:/x y/a.txt")

    def test_R2_1_strips_single_quotes(self):
        self.assertEqual(logic.clean_path_input("'a.txt'"), "a.txt")

    def test_R2_1_keeps_unmatched_quote(self):
        self.assertEqual(logic.clean_path_input('"a.txt'), '"a.txt')


class NormalizeCustomTextTests(unittest.TestCase):
    def test_R2_1_newlines_and_tabs_become_spaces(self):
        self.assertEqual(logic.normalize_custom_text("one\ntwo\tthree\r\nfour"),
                         "one two three four")

    def test_R2_1_repeated_spaces_collapse(self):
        self.assertEqual(logic.normalize_custom_text("a    b"), "a b")

    def test_R2_1_trailing_newline_trimmed(self):
        self.assertEqual(logic.normalize_custom_text("  hello world\n"), "hello world")


class ValidateCustomTextTests(unittest.TestCase):
    def test_R2_1_valid_text_has_no_error(self):
        self.assertIsNone(logic.validate_custom_text(VALID_TEXT))

    def test_R2_1_all_keyboard_symbols_allowed(self):
        text = "`~!@#$%^&*()-_=+[]{}\\|;:'\",.<>/? 0123456789 abcXYZ"
        self.assertIsNone(logic.validate_custom_text(text))

    def test_R2_1_non_keyboard_character_rejected(self):
        error = logic.validate_custom_text(VALID_TEXT + " café")
        self.assertIn("standard keyboard", error)
        self.assertIn("'é'", error)

    def test_R2_1_curly_quotes_rejected(self):
        self.assertIsNotNone(logic.validate_custom_text(VALID_TEXT + " \u201chi\u201d"))

    def test_R2_1_minimum_length_boundary(self):
        self.assertIsNone(logic.validate_custom_text("a" * 40))
        self.assertIn("39 characters", logic.validate_custom_text("a" * 39))

    def test_R2_1_maximum_length_boundary(self):
        self.assertIsNone(logic.validate_custom_text("a" * 400))
        self.assertIn("401 characters", logic.validate_custom_text("a" * 401))


class LoadCustomTextTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def write(self, name, content, encoding="utf-8"):
        path = os.path.join(self.tmp.name, name)
        with open(path, "w", encoding=encoding, newline="") as f:
            f.write(content)
        return path

    def test_R2_1_loads_and_normalizes_file(self):
        path = self.write("ok.txt", "The quick brown fox\njumps over the lazy dog,\ttwice!\n")
        self.assertEqual(logic.load_custom_text(path), VALID_TEXT)

    def test_R2_1_accepts_quoted_path(self):
        path = self.write("ok.txt", VALID_TEXT)
        self.assertEqual(logic.load_custom_text(f'"{path}"'), VALID_TEXT)

    def test_R2_1_strips_notepad_bom(self):
        path = self.write("bom.txt", VALID_TEXT, encoding="utf-8-sig")
        self.assertEqual(logic.load_custom_text(path), VALID_TEXT)

    def test_R2_1_uppercase_extension_ok(self):
        path = self.write("OK.TXT", VALID_TEXT)
        self.assertEqual(logic.load_custom_text(path), VALID_TEXT)

    def test_R2_1_empty_path_rejected(self):
        with self.assertRaisesRegex(logic.CustomTextError, "type a path"):
            logic.load_custom_text("   ")

    def test_R2_1_non_txt_rejected(self):
        path = self.write("notes.md", VALID_TEXT)
        with self.assertRaisesRegex(logic.CustomTextError, r"\.txt"):
            logic.load_custom_text(path)

    def test_R2_1_missing_file_rejected(self):
        missing = os.path.join(self.tmp.name, "nope.txt")
        with self.assertRaisesRegex(logic.CustomTextError, "No file found"):
            logic.load_custom_text(missing)

    def test_R2_1_too_short_file_rejected(self):
        path = self.write("short.txt", "too short\n")
        with self.assertRaisesRegex(logic.CustomTextError, "9 characters"):
            logic.load_custom_text(path)

    def test_R2_1_length_counted_after_cleanup(self):
        # 40 visible chars padded with blank lines: valid once cleaned up.
        path = self.write("padded.txt", "\n\n" + "a" * 40 + "\n\n\n")
        self.assertEqual(logic.load_custom_text(path), "a" * 40)

    def test_R2_1_bad_character_file_rejected(self):
        path = self.write("emoji.txt", VALID_TEXT + " \U0001F600")
        with self.assertRaisesRegex(logic.CustomTextError, "standard keyboard"):
            logic.load_custom_text(path)

    def test_R2_1_non_utf8_file_rejected(self):
        path = os.path.join(self.tmp.name, "binary.txt")
        with open(path, "wb") as f:
            f.write(b"\xff\xfe\x00\x81" * 20)
        with self.assertRaisesRegex(logic.CustomTextError, "plain text"):
            logic.load_custom_text(path)

    def test_R2_1_loaded_text_works_as_typing_test(self):
        path = self.write("ok.txt", VALID_TEXT)
        t = logic.TypingTest(logic.load_custom_text(path))
        for ch in VALID_TEXT:
            t.type_char(ch)
        self.assertTrue(t.is_finished())
        self.assertEqual(t.correct_count(), len(VALID_TEXT))


if __name__ == "__main__":
    unittest.main()
