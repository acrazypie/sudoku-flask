"""
Tests for the Sudoku solver.
"""

import unittest
import random
from api.generator.full_board import FullBoardGenerator
from api.generator.puzzle_generator import PuzzleGenerator
from api.solver.solver import SudokuSolver
from api.validation.rules import validate_complete


class TestSolver(unittest.TestCase):
    """Test cases for Sudoku solver."""

    def setUp(self):
        """Set up test fixtures with fixed seed for reproducibility."""
        random.seed(42)

    def test_solve_complete_board(self):
        """Test that solver handles already-complete board."""
        generator = FullBoardGenerator()
        board = generator.generate()

        solver = SudokuSolver()
        solved = solver.solve(board.copy())

        self.assertTrue(solved)
        self.assertTrue(validate_complete(board))

    def test_solve_easy_puzzle(self):
        """Test solving easy puzzle."""
        generator = PuzzleGenerator()
        puzzle = generator.generate(difficulty="easy")

        solver = SudokuSolver()
        solved = solver.solve(puzzle.copy())

        self.assertTrue(solved)
        if puzzle.is_complete():
            self.assertTrue(validate_complete(puzzle))

    def test_solve_medium_puzzle(self):
        """Test solving medium puzzle."""
        generator = PuzzleGenerator()
        puzzle = generator.generate(difficulty="medium")

        solver = SudokuSolver()
        solved = solver.solve(puzzle.copy())

        self.assertTrue(solved)

    def test_solve_hard_puzzle(self):
        """Test solving hard puzzle."""
        generator = PuzzleGenerator()
        puzzle = generator.generate(difficulty="hard")

        solver = SudokuSolver()
        solved = solver.solve(puzzle.copy())

        self.assertTrue(solved)

    def test_collect_steps(self):
        """Test that solver collects solving steps."""
        generator = PuzzleGenerator()
        puzzle = generator.generate(difficulty="easy")

        solver = SudokuSolver()
        solver.solve(puzzle.copy(), collect_steps=True)

        steps = solver.get_steps()
        self.assertGreater(len(steps), 0)

    def test_hardest_technique(self):
        """Test hardest technique detection."""
        generator = PuzzleGenerator()
        puzzle = generator.generate(difficulty="medium")

        solver = SudokuSolver()
        solver.solve(puzzle.copy())

        hardest = solver.get_hardest_technique()
        self.assertIsNotNone(hardest)


if __name__ == "__main__":
    unittest.main()
