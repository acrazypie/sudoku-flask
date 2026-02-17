"""
Base class for all solving techniques.
"""

from abc import ABC, abstractmethod
from ...board.board import Board
from ..solve_step import SolveStep


class BaseTechnique(ABC):
    """Abstract base class for Sudoku solving techniques."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the technique."""
        pass

    @property
    @abstractmethod
    def difficulty(self) -> int:
        """Difficulty level of this technique (higher = harder)."""
        pass

    @abstractmethod
    def find(self, board: Board) -> SolveStep | None:
        """
        Find and apply this technique on the board.

        Args:
            board: The current Sudoku board state

        Returns:
            A SolveStep if technique was applied, None otherwise
        """
        pass

    def apply(self, board: Board, step: SolveStep) -> None:
        """
        Apply a solving step to the board.

        Args:
            board: The board to modify
            step: The step to apply
        """
        if step.value is not None:
            row = step.cell_index // 9
            col = step.cell_index % 9
            board.set_value(row, col, step.value, fixed=False)

        if step.candidates_removed:
            for idx in step.affected_cells:
                cell = board.get_cell_by_index(idx)
                for candidate in step.candidates_removed:
                    cell.remove_candidate(candidate)

    def get_candidates_for_value(
        self, board: Board, value: int, indices: list
    ) -> list:
        """Get indices of cells that have a specific value as candidate."""
        return [
            idx for idx in indices
            if board.get_cell_by_index(idx).is_empty
            and value in board.get_cell_by_index(idx).candidates
        ]
