"""
Tests for the hint engine.
"""

import unittest
from api.generator.full_board import FullBoardGenerator
from api.generator.puzzle_generator import PuzzleGenerator
from api.hints.hint_engine import HintEngine
from api.board.board import Board


class TestHints(unittest.TestCase):
    """Test cases for hint engine."""

    def test_get_hint(self):
        """Test getting a hint."""
        generator = PuzzleGenerator()
        puzzle = generator.generate(difficulty="easy")

        hint_engine = HintEngine()
        hint = hint_engine.get_next_hint(puzzle)

        self.assertIsNotNone(hint)
        self.assertIsNotNone(hint.technique)
        self.assertIsNotNone(hint.explanation)

    def test_hint_does_not_modify_board(self):
        """Test that hints don't modify the board."""
        generator = PuzzleGenerator()
        puzzle = generator.generate(difficulty="easy")

        puzzle_copy = puzzle.copy()

        hint_engine = HintEngine()
        hint_engine.get_next_hint(puzzle)

        self.assertEqual(puzzle.to_list(), puzzle_copy.to_list())

    def test_multiple_hints(self):
        """Test getting multiple hints."""
        generator = PuzzleGenerator()
        puzzle = generator.generate(difficulty="medium")

        hint_engine = HintEngine()

        for _ in range(3):
            hint = hint_engine.get_next_hint(puzzle)
            self.assertIsNotNone(hint)

    def test_hint_with_value(self):
        """Test that hint can contain a value to place."""
        generator = PuzzleGenerator()
        puzzle = generator.generate(difficulty="easy")

        hint_engine = HintEngine()
        hint = hint_engine.get_next_hint(puzzle)

        if hint.value:
            row = hint.cell_index // 9
            col = hint.cell_index % 9
            puzzle.set_value(row, col, hint.value, fixed=False)

        self.assertTrue(puzzle.is_valid())

    def test_is_solved(self):
        """Test is_solved check."""
        hint_engine = HintEngine()
        generator = FullBoardGenerator()

        board = generator.generate()
        self.assertTrue(hint_engine.is_solved(board))

    def test_can_make_progress(self):
        """Test can_make_progress check."""
        hint_engine = HintEngine()
        generator = PuzzleGenerator()

        puzzle = generator.generate(difficulty="easy")
        self.assertTrue(hint_engine.can_make_progress(puzzle))


if __name__ == "__main__":
    unittest.main()
