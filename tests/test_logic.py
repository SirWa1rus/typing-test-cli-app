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


# --- R3.1: medium and hard difficulty for the standard typing test --------------------

SENTENCE_ENDS = ".?!"


def bare_word(token):
    """A token with its punctuation removed and lowercased: 'Whether,' -> 'whether'."""
    return token.rstrip(",.?!").lower()


class DifficultyTests(unittest.TestCase):
    def test_R3_1_three_difficulties_in_order(self):
        self.assertEqual(logic.DIFFICULTIES, (logic.EASY, logic.MEDIUM, logic.HARD))

    def test_R3_1_default_is_easy(self):
        # Round 1 callers pass no difficulty and must still get easy text.
        self.assertEqual(logic.generate_text(30, random.Random(5)),
                         logic.generate_text(30, random.Random(5), logic.EASY))

    def test_R3_1_unknown_difficulty_rejected(self):
        with self.assertRaises(ValueError):
            logic.generate_text(10, random.Random(1), "impossible")

    def test_R3_1_word_count_every_difficulty(self):
        for difficulty in logic.DIFFICULTIES:
            with self.subTest(difficulty=difficulty):
                text = logic.generate_text(25, random.Random(7), difficulty)
                self.assertEqual(len(text.split(" ")), 25)

    def test_R3_1_only_keyboard_characters_every_difficulty(self):
        for difficulty in logic.DIFFICULTIES:
            with self.subTest(difficulty=difficulty):
                text = logic.generate_text(60, random.Random(8), difficulty)
                self.assertTrue(all(logic.is_keyboard_char(ch) for ch in text))

    def test_R3_1_same_seed_same_text_every_difficulty(self):
        for difficulty in logic.DIFFICULTIES:
            with self.subTest(difficulty=difficulty):
                a = logic.generate_text(20, random.Random(9), difficulty)
                b = logic.generate_text(20, random.Random(9), difficulty)
                self.assertEqual(a, b)

    def test_R3_1_word_lists_get_longer_with_difficulty(self):
        def average(words):
            return sum(map(len, words)) / len(words)
        self.assertLess(average(logic.EASY_WORDS), average(logic.MEDIUM_WORDS))
        self.assertLess(average(logic.MEDIUM_WORDS), average(logic.HARD_WORDS))

    def test_R3_1_word_lists_have_no_duplicates_or_overlap(self):
        easy, medium, hard = map(set, (logic.EASY_WORDS, logic.MEDIUM_WORDS, logic.HARD_WORDS))
        self.assertEqual(len(medium), len(logic.MEDIUM_WORDS))
        self.assertEqual(len(hard), len(logic.HARD_WORDS))
        self.assertFalse(easy & medium)
        self.assertFalse(medium & hard)
        self.assertFalse(easy & hard)


class MediumTextTests(unittest.TestCase):
    def setUp(self):
        self.words = logic.generate_text(60, random.Random(10), logic.MEDIUM).split(" ")

    def test_R3_1_medium_uses_only_medium_words(self):
        for word in self.words:
            self.assertIn(word, logic.MEDIUM_WORDS)

    def test_R3_1_medium_is_plain_lowercase(self):
        for word in self.words:
            self.assertTrue(word.isalpha() and word.islower(), word)


class HardTextTests(unittest.TestCase):
    def setUp(self):
        self.text = logic.generate_text(60, random.Random(11), logic.HARD)
        self.tokens = self.text.split(" ")

    def test_R3_1_hard_tokens_are_hard_words_or_numbers(self):
        for token in self.tokens:
            word = bare_word(token)
            self.assertTrue(word.isdigit() or word in logic.HARD_WORDS, token)

    def test_R3_1_hard_starts_with_capital(self):
        self.assertTrue(self.text[0].isupper())

    def test_R3_1_hard_ends_with_sentence_punctuation(self):
        self.assertIn(self.text[-1], SENTENCE_ENDS)

    def test_R3_1_hard_capital_after_each_sentence_end(self):
        for before, after in zip(self.tokens, self.tokens[1:]):
            if before[-1] in SENTENCE_ENDS and not after[0].isdigit():
                self.assertTrue(after[0].isupper(), f"{before} {after}")

    def test_R3_1_hard_mid_sentence_words_are_lowercase(self):
        for before, after in zip(self.tokens, self.tokens[1:]):
            if before[-1] not in SENTENCE_ENDS:
                self.assertFalse(after[0].isupper(), f"{before} {after}")

    def test_R3_1_hard_contains_commas_sentence_ends_and_numbers(self):
        self.assertIn(",", self.text)
        self.assertTrue(any(ch in self.text[:-1] for ch in SENTENCE_ENDS))
        self.assertTrue(any(ch.isdigit() for ch in self.text))

    def test_R3_1_hard_text_works_as_typing_test(self):
        t = logic.TypingTest(self.text)
        for ch in self.text:
            t.type_char(ch)
        self.assertTrue(t.is_finished())
        self.assertEqual(t.correct_count(), len(self.text))


class ZoomTipTests(unittest.TestCase):
    def test_R4_1_full_tip_explains_ctrl_zoom_on_wide_screen(self):
        tip = logic.zoom_tip(200)
        self.assertEqual(tip, logic.ZOOM_TIP)
        self.assertIn("Ctrl", tip)
        self.assertIn("bigger", tip)

    def test_R4_1_short_tip_on_narrow_screen(self):
        tip = logic.zoom_tip(len(logic.ZOOM_TIP) - 1)
        self.assertEqual(tip, logic.ZOOM_TIP_SHORT)
        self.assertIn("Ctrl", tip)

    def test_R4_1_no_tip_when_nothing_fits(self):
        self.assertEqual(logic.zoom_tip(len(logic.ZOOM_TIP_SHORT) - 1), "")
        self.assertEqual(logic.zoom_tip(0), "")

    def test_R4_1_tip_never_wider_than_screen(self):
        for width in range(0, 120):
            self.assertLessEqual(len(logic.zoom_tip(width)), width)


TEXT = logic.generate_text(60, random.Random(4))


def rows_of(positions):
    """Group (row, col) positions by row: {row: [cols...]}."""
    rows = {}
    for r, c in positions:
        rows.setdefault(r, []).append(c)
    return rows


class CenteredPositionsTests(unittest.TestCase):
    def test_R4_2_one_position_per_character(self):
        self.assertEqual(len(logic.centered_positions(TEXT, 100, 30)), len(TEXT))

    def test_R4_2_same_layout_as_wrap_just_shifted(self):
        pos = logic.centered_positions(TEXT, 100, 30)
        wrapped = logic.wrap_positions(TEXT, logic.TEXT_MAX_WIDTH)
        dr, dc = pos[0][0] - wrapped[0][0], pos[0][1] - wrapped[0][1]
        self.assertEqual(pos, [(r + dr, c + dc) for r, c in wrapped])

    def test_R4_2_every_line_starts_at_same_column(self):
        starts = {min(cols) for cols in rows_of(logic.centered_positions(TEXT, 100, 30)).values()}
        self.assertEqual(len(starts), 1)

    def test_R4_2_horizontally_centered(self):
        for cols in (40, 61, 80, 100, 101, 200):
            pos = logic.centered_positions(TEXT, cols, 30)
            left = min(c for _, c in pos)
            right = cols - 1 - max(c for _, c in pos)
            self.assertLessEqual(abs(left - right), 1, f"screen width {cols}")

    def test_R4_2_lines_capped_at_max_width_on_wide_screen(self):
        widths = [max(c) - min(c) + 1 for c in rows_of(logic.centered_positions(TEXT, 300, 30)).values()]
        self.assertLessEqual(max(widths), logic.TEXT_MAX_WIDTH)

    def test_R4_2_fits_inside_narrow_screen_with_margins(self):
        cols = 30
        pos = logic.centered_positions(TEXT, cols, 60)
        self.assertGreaterEqual(min(c for _, c in pos), logic.SIDE_MARGIN)
        self.assertLessEqual(max(c for _, c in pos), cols - 1 - logic.SIDE_MARGIN)

    def test_R4_2_vertically_centered(self):
        screen_rows = 40
        pos = logic.centered_positions(TEXT, 100, screen_rows)
        top = min(r for r, _ in pos)
        bottom_gap = screen_rows - 1 - max(r for r, _ in pos)
        self.assertLessEqual(abs(top - bottom_gap), 1)

    def test_R4_2_never_above_title_and_timer(self):
        pos = logic.centered_positions(TEXT, 100, 5)  # very short screen
        self.assertEqual(min(r for r, _ in pos), logic.TEXT_TOP)

    def test_R4_2_short_text_centered_by_its_own_width(self):
        text = "short words"
        pos = logic.centered_positions(text, 81, 30)
        self.assertEqual(pos[0][1], (81 - len(text)) // 2)
        self.assertEqual({r for r, _ in pos}, {(30 - 1) // 2})

    def test_R4_2_empty_text_gives_no_positions(self):
        self.assertEqual(logic.centered_positions("", 80, 24), [])


class ButtonHighlightTests(unittest.TestCase):
    """R5.1: a white box behind the selectable button the user is on.

    The drawing (the white color) is in main.py; these tests check the layout
    math in logic.py: which button is marked as selected, and where each
    button and its box go.
    """

    MENU = ["Standard typing test", "Custom typing test"]
    ROW = ["Retry", "Menu", "Quit"]

    def test_R5_1_labels_padded_to_same_width(self):
        labels = logic.button_labels(self.MENU)
        widths = {len(label) for label in labels}
        self.assertEqual(widths, {len("Standard typing test") + 2})

    def test_R5_1_label_has_one_space_before_text(self):
        for label, option in zip(logic.button_labels(self.ROW), self.ROW):
            self.assertTrue(label.startswith(" " + option))

    def test_R5_1_vertical_exactly_the_hovered_button_selected(self):
        for hovered in range(len(self.MENU)):
            buttons = logic.vertical_menu_buttons(self.MENU, hovered, 80, 24)
            self.assertEqual([b.selected for b in buttons],
                             [i == hovered for i in range(len(self.MENU))])

    def test_R5_1_vertical_box_keeps_size_and_column(self):
        buttons = logic.vertical_menu_buttons(self.MENU, 0, 80, 24)
        self.assertEqual(len({b.col for b in buttons}), 1)
        self.assertEqual(len({len(b.text) for b in buttons}), 1)

    def test_R5_1_vertical_buttons_on_consecutive_rows_below_middle(self):
        options = ["Easy", "Medium", "Hard"]
        buttons = logic.vertical_menu_buttons(options, 0, 80, 24)
        self.assertEqual([b.row for b in buttons], [11, 12, 13])

    def test_R5_1_vertical_buttons_centered(self):
        b = logic.vertical_menu_buttons(self.MENU, 0, 80, 24)[0]
        left_space = b.col
        right_space = 80 - (b.col + len(b.text))
        self.assertLessEqual(abs(left_space - right_space), 1)

    def test_R5_1_vertical_text_shows_the_option(self):
        buttons = logic.vertical_menu_buttons(self.MENU, 0, 80, 24)
        for b, option in zip(buttons, self.MENU):
            self.assertIn(option, b.text)

    def test_R5_1_row_exactly_the_hovered_button_selected(self):
        for hovered in range(len(self.ROW)):
            buttons = logic.button_row(self.ROW, hovered, 80, 12)
            self.assertEqual([b.selected for b in buttons],
                             [i == hovered for i in range(len(self.ROW))])

    def test_R5_1_row_has_no_brackets(self):
        for b in logic.button_row(self.ROW, 1, 80, 12):
            self.assertNotIn("[", b.text)
            self.assertNotIn("]", b.text)

    def test_R5_1_row_buttons_same_width_left_to_right_with_gap(self):
        buttons = logic.button_row(self.ROW, 0, 80, 12)
        self.assertEqual(len({len(b.text) for b in buttons}), 1)
        for left, right in zip(buttons, buttons[1:]):
            self.assertEqual(right.col - (left.col + len(left.text)), logic.BUTTON_GAP)
        self.assertEqual({b.row for b in buttons}, {12})

    def test_R5_1_row_layout_does_not_move_when_hover_moves(self):
        cols = [[b.col for b in logic.button_row(self.ROW, s, 80, 12)] for s in range(3)]
        self.assertEqual(cols[0], cols[1])
        self.assertEqual(cols[1], cols[2])

    def test_R5_1_row_centered(self):
        buttons = logic.button_row(self.ROW, 0, 80, 12)
        left_space = buttons[0].col
        right_space = 80 - (buttons[-1].col + len(buttons[-1].text))
        self.assertLessEqual(abs(left_space - right_space), 1)

    def test_R5_1_narrow_screen_never_negative_column(self):
        for b in logic.vertical_menu_buttons(self.MENU, 0, 5, 24):
            self.assertGreaterEqual(b.col, 0)
        for b in logic.button_row(self.ROW, 0, 5, 12):
            self.assertGreaterEqual(b.col, 0)

    def test_R5_1_move_selection_steps_by_one(self):
        self.assertEqual(logic.move_selection(0, 1, 3), 1)
        self.assertEqual(logic.move_selection(2, -1, 3), 1)

    def test_R5_1_move_selection_stops_at_ends(self):
        self.assertEqual(logic.move_selection(0, -1, 3), 0)
        self.assertEqual(logic.move_selection(2, 1, 3), 2)


class GetReadyAnimationTests(unittest.TestCase):
    """R6.1: the animated "Get ready" screen (twinkling stars, Jupiter-style planet)."""

    COLS, ROWS = 80, 24
    FRAMES = range(100)  # every frame of a 5-second countdown at 20 frames/second
    PLANET_SHADES = {"purple", "light_purple", "dark_purple", "bright_purple",
                     "blue", "light_blue", "dark_blue"}

    def on_screen(self, cells, cols=COLS, rows=ROWS):
        return all(0 <= c.row < rows and 0 <= c.col < cols for c in cells)

    def stars(self, frame):
        return logic.star_field(self.COLS, self.ROWS, frame)

    # --- frames ---

    def test_R6_1_frames_count_up_twenty_per_second(self):
        self.assertEqual(logic.animation_frame(0), 0)
        self.assertEqual(logic.animation_frame(0.049), 0)
        self.assertEqual(logic.animation_frame(1.0), 20)

    # --- twinkling stars ---

    def test_R6_1_stars_stay_in_place(self):
        spots = lambda f: [(c.row, c.col) for c in self.stars(f)]
        for frame in self.FRAMES:
            self.assertEqual(spots(frame), spots(0))

    def test_R6_1_every_star_twinkles(self):
        cycle = len(logic.TWINKLE) * max(logic.TWINKLE_SPEEDS)
        looks = {}
        for frame in range(cycle):
            for c in self.stars(frame):
                looks.setdefault((c.row, c.col), set()).add(c.char)
        self.assertTrue(looks)
        for spot, chars in looks.items():
            self.assertEqual(chars, {".", "+", "*"}, spot)  # dim, normal, and bright

    def test_R6_1_stars_do_not_all_blink_together(self):
        for frame in (0, 17, 50):
            self.assertGreater(len({c.char for c in self.stars(frame)}), 1)

    def test_R6_1_stars_use_twinkle_looks_only(self):
        allowed = set(logic.TWINKLE)
        for frame in range(30):
            for c in self.stars(frame):
                self.assertIn((c.char, c.color), allowed)

    def test_R6_1_twinkle_goes_dim_normal_bright(self):
        brightness = [b for _, b in logic.TWINKLE]
        self.assertEqual(set(brightness), {"star_dim", "star", "star_bright"})

    def test_R6_1_stars_are_behind_the_planet(self):
        planet = logic.planet_background(self.COLS, self.ROWS)
        for frame in (0, 33):
            for c in self.stars(frame):
                self.assertNotIn((c.row, c.col), planet)

    def test_R6_1_enough_stars_and_on_screen(self):
        stars = self.stars(0)
        self.assertGreater(len(stars), 15)
        self.assertTrue(self.on_screen(stars))
        self.assertTrue(self.on_screen(logic.star_field(10, 4, 0), 10, 4))

    def test_R6_1_stars_repeatable(self):
        self.assertEqual(self.stars(5), self.stars(5))

    # --- planet (Jupiter-style, purple and blue) ---

    def planet(self):
        return logic.planet_cells(self.COLS, self.ROWS)

    def test_R6_1_planet_is_very_large(self):
        self.assertGreater(len(self.planet()), 0.2 * self.COLS * self.ROWS)

    def test_R6_1_planet_only_purples_and_blues(self):
        colors = {c.color for c in self.planet()}
        self.assertLessEqual(colors, self.PLANET_SHADES)
        self.assertTrue(any("purple" in c for c in colors))
        self.assertTrue(any("blue" in c for c in colors))

    def test_R6_1_planet_has_many_bands_like_jupiter(self):
        mid_col = self.COLS // 2
        column = [c.color for c in sorted(self.planet(), key=lambda c: c.row) if c.col == mid_col]
        changes = sum(1 for a, b in zip(column, column[1:]) if a != b)
        self.assertGreaterEqual(changes, 6)

    def test_R6_1_planet_bands_are_wavy(self):
        spot = {logic.SPOT_CORE, logic.SPOT_RIM}
        wavy_rows = 0
        for row in range(self.ROWS):
            colors = {c.color for c in self.planet() if c.row == row and c.color not in spot}
            wavy_rows += len(colors) > 1
        self.assertGreater(wavy_rows, 5)  # band edges cross many rows, so they wave

    def test_R6_1_planet_has_a_great_spot(self):
        spot_row, spot_col, row_radius, col_radius = logic.planet_spot(self.COLS, self.ROWS)
        colors = {(c.row, c.col): c.color for c in self.planet()}
        self.assertEqual(colors[(spot_row, spot_col)], logic.SPOT_CORE)
        self.assertGreater(spot_row, self.ROWS // 2)           # below the middle
        self.assertGreater(spot_col, self.COLS // 2)           # right of center
        self.assertGreater(col_radius, row_radius)             # a wide oval
        self.assertNotIn(logic.SPOT_CORE, logic.PLANET_BANDS)  # it stands out from the bands
        self.assertNotIn(logic.SPOT_RIM, logic.PLANET_BANDS)

    def test_R6_1_planet_centered(self):
        cells = self.planet()
        mid_row = (min(c.row for c in cells) + max(c.row for c in cells)) / 2
        mid_col = (min(c.col for c in cells) + max(c.col for c in cells)) / 2
        self.assertLessEqual(abs(mid_row - self.ROWS // 2), 1)
        self.assertLessEqual(abs(mid_col - self.COLS // 2), 2)

    def test_R6_1_planet_stays_still(self):
        self.assertEqual(self.planet(), self.planet())  # no frame input: it cannot move

    def test_R6_1_planet_clipped_to_screen(self):
        self.assertTrue(self.on_screen(self.planet()))
        self.assertTrue(self.on_screen(logic.planet_cells(10, 4), 10, 4))

    # --- no black boxes behind text on the planet ---

    def test_R6_1_background_matches_planet_and_is_empty_off_planet(self):
        background = logic.planet_background(self.COLS, self.ROWS)
        for c in self.planet():
            self.assertEqual(background[(c.row, c.col)], c.color)
        self.assertNotIn((0, 0), background)  # top-left corner is open space

    # --- text ---

    def test_R6_1_text_at_top_and_bottom(self):
        rows = logic.countdown_text_rows(self.ROWS)
        self.assertEqual((rows["title"], rows["number"]), (1, 2))
        self.assertEqual((rows["tip"], rows["hint"]), (self.ROWS - 2, self.ROWS - 1))


if __name__ == "__main__":
    unittest.main()
