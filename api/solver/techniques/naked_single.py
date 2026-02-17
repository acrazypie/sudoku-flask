"""
Naked Single solving technique.

A naked single occurs when a cell has only one possible candidate.
"""

from ...board.board import Board
from ..solve_step import SolveStep
from .base import BaseTechnique


class NakedSingle(BaseTechnique):
    """Find cells with only one possible candidate."""

    @property
    def name(self) -> str:
        return "Naked Single"

    @property
    def difficulty(self) -> int:
        return 1

    def find(self, board: Board) -> SolveStep | None:
        """Find a cell with only one candidate."""
        for row in range(9):
            for col in range(9):
                cell = board.get_cell(row, col)
                if cell.is_empty and len(cell.candidates) == 1:
                    value = next(iter(cell.candidates))
                    index = row * 9 + col

                    return SolveStep(
                        technique=self.name,
                        cell_index=index,
                        value=value,
                        explanation=f"Cell at row {row + 1}, column {col + 1} "
                                    f"has only one possible value: {value}",
                    )
        return None
