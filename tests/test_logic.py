"""Tests for logic.py. Run from the project folder with:

    python -m unittest discover tests -v
"""

import random
import unittest

import logic


class GenerateTextTests(unittest.TestCase):
    def test_word_count(self):
        text = logic.generate_text(10, random.Random(1))
        self.assertEqual(len(text.split(" ")), 10)

    def test_uses_only_easy_words(self):
        text = logic.generate_text(50, random.Random(2))
        for word in text.split(" "):
            self.assertIn(word, logic.EASY_WORDS)

    def test_same_seed_same_text(self):
        a = logic.generate_text(20, random.Random(42))
        b = logic.generate_text(20, random.Random(42))
        self.assertEqual(a, b)


class TypingTestTests(unittest.TestCase):
    def test_starts_untyped(self):
        t = logic.TypingTest("hi there")
        self.assertEqual(t.cursor, 0)
        self.assertEqual(t.status(0), logic.UNTYPED)
        self.assertFalse(t.is_finished())

    def test_correct_and_incorrect(self):
        t = logic.TypingTest("ab c")
        t.type_char("a")
        t.type_char("x")
        t.type_char("_")   # wrong character where a space belongs
        self.assertEqual(t.status(0), logic.CORRECT)
        self.assertEqual(t.status(1), logic.INCORRECT)
        self.assertEqual(t.status(2), logic.INCORRECT)
        self.assertEqual(t.status(3), logic.UNTYPED)
        self.assertEqual(t.correct_count(), 1)

    def test_correct_space(self):
        t = logic.TypingTest("a b")
        t.type_char("a")
        t.type_char(" ")
        self.assertEqual(t.status(1), logic.CORRECT)

    def test_backspace_fixes_mistake(self):
        t = logic.TypingTest("ab")
        t.type_char("a")
        t.type_char("x")
        t.backspace()
        self.assertEqual(t.status(1), logic.UNTYPED)
        t.type_char("b")
        self.assertEqual(t.correct_count(), 2)

    def test_backspace_when_empty_does_nothing(self):
        t = logic.TypingTest("ab")
        t.backspace()
        self.assertEqual(t.cursor, 0)

    def test_finished_and_extra_keys_ignored(self):
        t = logic.TypingTest("ab")
        for ch in "abc":
            t.type_char(ch)
        self.assertTrue(t.is_finished())
        self.assertEqual(t.cursor, 2)


class ScoringTests(unittest.TestCase):
    def test_wpm_formula(self):
        # 250 correct chars = 50 words, in 60 seconds -> 50 WPM
        self.assertAlmostEqual(logic.calculate_wpm(250, 60), 50.0)
        # 150 chars = 30 words in 45 s (0.75 min) -> 40 WPM
        self.assertAlmostEqual(logic.calculate_wpm(150, 45), 40.0)

    def test_wpm_zero_time(self):
        self.assertEqual(logic.calculate_wpm(100, 0), 0.0)

    def test_percent_at_average_is_half(self):
        self.assertAlmostEqual(logic.percent_beaten(logic.AVERAGE_WPM), 50.0)

    def test_percent_increases_with_speed(self):
        self.assertLess(logic.percent_beaten(20), logic.percent_beaten(60))

    def test_percent_stays_in_range(self):
        self.assertGreaterEqual(logic.percent_beaten(0), 0)
        self.assertLessEqual(logic.percent_beaten(300), 100)


class WrapPositionsTests(unittest.TestCase):
    def test_one_position_per_character(self):
        text = "the cat sat on the mat"
        self.assertEqual(len(logic.wrap_positions(text, 10)), len(text))

    def test_fits_on_one_line(self):
        self.assertEqual(logic.wrap_positions("ab cd", 20),
                         [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)])

    def test_breaks_at_space(self):
        # width 6: "ab cd " fits (6 cols), "ef" moves to row 1
        pos = logic.wrap_positions("ab cd ef", 6)
        self.assertEqual(pos[6], (1, 0))   # 'e'
        self.assertEqual(pos[5], (0, 5))   # the space before 'ef'

    def test_never_exceeds_width(self):
        text = logic.generate_text(40, random.Random(3))
        for row, col in logic.wrap_positions(text, 15):
            self.assertLess(col, 15)

    def test_long_word_is_split(self):
        pos = logic.wrap_positions("abcdefgh", 3)
        self.assertEqual(pos[3], (1, 0))


if __name__ == "__main__":
    unittest.main()
