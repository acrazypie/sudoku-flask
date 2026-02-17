"""
Tests for the Sudoku generator.
"""

import unittest
from api.generator.full_board import FullBoardGenerator
from api.generator.puzzle_generator import PuzzleGenerator
from api.generator.uniqueness import UniquenessChecker
from api.validation.rules import validate_complete


class TestGenerator(unittest.TestCase):
    """Test cases for Sudoku generators."""

    def test_full_board_generation(self):
        """Test that full board generates valid complete board."""
        generator = FullBoardGenerator()
        board = generator.generate()

        self.assertTrue(validate_complete(board))
        self.assertEqual(board.count_filled(), 81)

    def test_puzzle_generation_easy(self):
        """Test easy puzzle generation."""
        generator = PuzzleGenerator()
        puzzle = generator.generate(difficulty="easy")

        self.assertTrue(puzzle.is_valid())
        self.assertGreater(puzzle.count_filled(), 35)

    def test_puzzle_generation_medium(self):
        """Test medium puzzle generation."""
        generator = PuzzleGenerator()
        puzzle = generator.generate(difficulty="medium")

        self.assertTrue(puzzle.is_valid())
        self.assertGreater(puzzle.count_filled(), 25)

    def test_puzzle_generation_hard(self):
        """Test hard puzzle generation."""
        generator = PuzzleGenerator()
        puzzle = generator.generate(difficulty="hard")

        self.assertTrue(puzzle.is_valid())
        self.assertGreater(puzzle.count_filled(), 20)

    def test_uniqueness_checker(self):
        """Test uniqueness checking."""
        generator = FullBoardGenerator()
        board = generator.generate()

        checker = UniquenessChecker()
        self.assertTrue(checker.has_unique_solution(board))

    def test_multiple_puzzles(self):
        """Test generating multiple puzzles."""
        generator = PuzzleGenerator()

        for _ in range(5):
            puzzle = generator.generate(difficulty="medium")
            self.assertTrue(puzzle.is_valid())


if __name__ == "__main__":
    unittest.main()
