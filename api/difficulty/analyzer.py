"""
Difficulty analyzer for Sudoku puzzles.
"""

from ..board.board import Board
from ..solver.solver import SudokuSolver
from .levels import DifficultyLevel, TECHNIQUE_DIFFICULTY


class DifficultyAnalyzer:
    """Analyzes the difficulty of a Sudoku puzzle."""

    def analyze(self, board: Board) -> DifficultyLevel:
        """
        Analyze puzzle difficulty.

        Args:
            board: The puzzle to analyze

        Returns:
            The difficulty level
        """
        solver = SudokuSolver()
        solver.solve(board, collect_steps=True)

        hardest_technique = solver.get_hardest_technique()
        total_steps = len(solver.get_steps())

        max_diff = TECHNIQUE_DIFFICULTY.get(hardest_technique, 0)

        if max_diff <= 1 and total_steps <= 30:
            return DifficultyLevel.EASY
        elif max_diff <= 2 and total_steps <= 80:
            return DifficultyLevel.MEDIUM
        elif max_diff <= 3 and total_steps <= 150:
            return DifficultyLevel.HARD
        else:
            return DifficultyLevel.EXPERT

    def get_details(self, board: Board) -> dict:
        """
        Get detailed difficulty analysis.

        Args:
            board: The puzzle to analyze

        Returns:
            Dictionary with difficulty details
        """
        solver = SudokuSolver()
        solver.solve(board, collect_steps=True)

        steps = solver.get_steps()
        hardest = solver.get_hardest_technique()

        technique_counts = {}
        for step in steps:
            technique_counts[step.technique] = technique_counts.get(step.technique, 0) + 1

        max_diff = TECHNIQUE_DIFFICULTY.get(hardest, 0)

        level = DifficultyLevel.EASY
        if max_diff > 1 or len(steps) > 30:
            level = DifficultyLevel.MEDIUM
        if max_diff > 2 or len(steps) > 80:
            level = DifficultyLevel.HARD
        if max_diff > 3 or len(steps) > 150:
            level = DifficultyLevel.EXPERT

        return {
            "level": str(level),
            "total_steps": len(steps),
            "hardest_technique": hardest,
            "technique_counts": technique_counts,
        }
