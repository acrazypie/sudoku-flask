"""
Hint engine that provides hints to the user.
"""

from ..board.board import Board
from ..solver.solve_step import SolveStep
from ..solver.candidates import initialize_candidates
from ..solver.techniques.naked_single import NakedSingle
from ..solver.techniques.hidden_single import HiddenSingle
from ..solver.techniques.naked_pair import NakedPair
from ..solver.techniques.hidden_pair import HiddenPair
from ..solver.techniques.pointing_pair import PointingPair


class HintEngine:
    """Provides hints for solving Sudoku puzzles."""

    def __init__(self):
        self._techniques = [
            NakedSingle(),
            HiddenSingle(),
            NakedPair(),
            HiddenPair(),
            PointingPair(),
        ]
        self._initialized = False

    def get_next_hint(self, board: Board) -> SolveStep:
        """
        Get the next hint for the puzzle.

        This method does NOT modify the board.

        Args:
            board: The current puzzle state

        Returns:
            A SolveStep representing the next logical move
        """
        if not self._initialized:
            initialize_candidates(board)
            self._initialized = True

        for technique in self._techniques:
            step = technique.find(board)
            if step:
                return step

        raise ValueError("No more hints available - puzzle requires guessing")

    def reset(self) -> None:
        """Reset the hint engine state."""
        self._initialized = False

    def is_solved(self, board: Board) -> bool:
        """Check if the puzzle is solved."""
        return board.is_complete()

    def can_make_progress(self, board: Board) -> bool:
        """Check if the puzzle can be solved logically."""
        try:
            self.get_next_hint(board)
            return True
        except ValueError:
            return False
