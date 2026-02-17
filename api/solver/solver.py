"""
Main Sudoku solver that orchestrates all solving techniques.
"""

from typing import List
from ..board.board import Board
from .solve_step import SolveStep
from .candidates import initialize_candidates, update_all_candidates
from .techniques.naked_single import NakedSingle
from .techniques.hidden_single import HiddenSingle
from .techniques.naked_pair import NakedPair
from .techniques.hidden_pair import HiddenPair
from .techniques.pointing_pair import PointingPair


class SudokuSolver:
    """Main solver that applies logical solving techniques."""

    def __init__(self):
        self._techniques = [
            NakedSingle(),
            HiddenSingle(),
            NakedPair(),
            HiddenPair(),
            PointingPair(),
        ]
        self._steps: List[SolveStep] = []

    def solve(self, board: Board, collect_steps: bool = True) -> bool:
        """
        Solve a Sudoku puzzle using logical techniques.

        Args:
            board: The puzzle to solve
            collect_steps: Whether to collect solving steps

        Returns:
            True if puzzle was solved, False otherwise
        """
        self._steps = []
        initialize_candidates(board)

        max_iterations = 500
        iteration = 0

        while not board.is_complete() and iteration < max_iterations:
            iteration += 1
            step_applied = False

            for technique in self._techniques:
                step = technique.find(board)
                if step:
                    technique.apply(board, step)
                    update_all_candidates(board)

                    if collect_steps:
                        self._steps.append(step)

                    step_applied = True
                    break

            if not step_applied:
                break

        return board.is_complete()

    def get_steps(self) -> List[SolveStep]:
        """Get the list of solving steps."""
        return self._steps.copy()

    def get_hardest_technique(self) -> str:
        """Get the name of the hardest technique used."""
        if not self._steps:
            return "None"

        technique_difficulty = {
            "Naked Single": 1,
            "Hidden Single": 2,
            "Naked Pair": 3,
            "Hidden Pair": 4,
            "Pointing Pair": 4,
        }

        max_difficulty = 0
        hardest = "None"

        for step in self._steps:
            diff = technique_difficulty.get(step.technique, 0)
            if diff > max_difficulty:
                max_difficulty = diff
                hardest = step.technique

        return hardest
