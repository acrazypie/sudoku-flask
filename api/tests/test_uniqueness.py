"""
Tests for uniqueness checking.
"""

import unittest
from api.generator.full_board import FullBoardGenerator
from api.generator.puzzle_generator import PuzzleGenerator
from api.generator.uniqueness import UniquenessChecker, count_solutions
from api.board.board import Board
from api.board.constants import EMPTY_CELL


class TestUniqueness(unittest.TestCase):
    """Test cases for uniqueness checking."""

    def test_unique_solution(self):
        """Test that generated puzzles have unique solutions."""
        generator = PuzzleGenerator()
        checker = UniquenessChecker()

        for _ in range(3):
            puzzle = generator.generate(difficulty="hard")
            self.assertTrue(checker.has_unique_solution(puzzle))

    def test_full_board_unique(self):
        """Test that full board has unique solution."""
        generator = FullBoardGenerator()
        board = generator.generate()

        checker = UniquenessChecker()
        self.assertTrue(checker.has_unique_solution(board))

    def test_count_solutions(self):
        """Test solution counting."""
        generator = FullBoardGenerator()
        board = generator.generate()

        count = count_solutions(board)
        self.assertEqual(count, 1)

    def test_puzzle_with_multiple_solutions(self):
        """Test detection of multiple solutions."""
        board = Board()

        board.set_value(0, 0, 1, fixed=True)
        board.set_value(0, 1, 2, fixed=True)

        checker = UniquenessChecker()
        self.assertFalse(checker.has_unique_solution(board))


if __name__ == "__main__":
    unittest.main()
