"""
Puzzle generator that creates Sudoku puzzles with unique solutions.
"""

import random
from ..board.board import Board
from ..board.constants import EMPTY_CELL
from .full_board import FullBoardGenerator
from .uniqueness import UniquenessChecker, get_valid_candidates


class PuzzleGenerator:
    """Generates Sudoku puzzles with unique solutions."""

    def __init__(self):
        self._board_generator = FullBoardGenerator()
        self._uniqueness_checker = UniquenessChecker()

    def generate(self, difficulty: str = "medium", attempts: int = 100) -> Board:
        """
        Generate a puzzle with the specified difficulty.

        Args:
            difficulty: Target difficulty level
            attempts: Number of attempts to find a valid puzzle

        Returns:
            A puzzle board with unique solution
        """
        target_clues = self._get_target_clues(difficulty)

        for _ in range(attempts):
            solution = self._board_generator.generate()
            puzzle = self._create_puzzle(solution, target_clues)

            if puzzle is not None:
                return puzzle

        return self._generate_fallback(target_clues)

    def _create_puzzle(self, solution: Board, target_clues: int) -> Board:
        """Create a puzzle by removing cells from a solved board."""
        puzzle = solution.copy()
        indices = list(range(81))
        random.shuffle(indices)

        removed = 0
        target_removal = 81 - target_clues

        for idx in indices:
            if removed >= target_removal:
                break

            row = idx // 9
            col = idx % 9
            original_value = puzzle.get_value(row, col)

            if original_value == EMPTY_CELL:
                continue

            puzzle.set_value(row, col, EMPTY_CELL, fixed=False)

            if not self._uniqueness_checker.has_unique_solution(puzzle):
                puzzle.set_value(row, col, original_value, fixed=True)
                continue

            removed += 1

        return puzzle

    def _get_target_clues(self, difficulty: str) -> int:
        """Get target number of clues for difficulty level."""
        difficulty_map = {
            "easy": random.randint(40, 50),
            "medium": random.randint(32, 39),
            "hard": random.randint(28, 31),
            "expert": random.randint(22, 27),
        }
        return difficulty_map.get(difficulty.lower(), 35)

    def _generate_fallback(self, target_clues: int) -> Board:
        """Generate a puzzle with a simple approach as fallback."""
        solution = self._board_generator.generate()
        puzzle = solution.copy()

        indices = list(range(81))
        random.shuffle(indices)

        for idx in indices[:81 - target_clues]:
            row = idx // 9
            col = idx % 9
            puzzle.set_value(row, col, EMPTY_CELL, fixed=False)

        return puzzle
