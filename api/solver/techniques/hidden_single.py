"""
Hidden Single solving technique.

A hidden single occurs when a candidate value appears only once 
in a row, column, or box.
"""

from ...board.board import Board
from ..solve_step import SolveStep
from .base import BaseTechnique
from ...board.constants import ROW_INDICES, COL_INDICES, BOX_INDICES


class HiddenSingle(BaseTechnique):
    """Find hidden singles in rows, columns, and boxes."""

    @property
    def name(self) -> str:
        return "Hidden Single"

    @property
    def difficulty(self) -> int:
        return 2

    def find(self, board: Board) -> SolveStep | None:
        """Find a hidden single."""
        for row in range(9):
            step = self._check_group(board, ROW_INDICES[row], f"row {row + 1}")
            if step:
                return step

        for col in range(9):
            step = self._check_group(board, COL_INDICES[col], f"column {col + 1}")
            if step:
                return step

        for box in range(9):
            step = self._check_group(board, BOX_INDICES[box], f"box {box + 1}")
            if step:
                return step

        return None

    def _check_group(self, board: Board, indices: list, group_name: str) -> SolveStep | None:
        """Check a group (row, col, box) for hidden singles."""
        for value in range(1, 10):
            cells_with_value = [
                idx for idx in indices
                if board.get_cell_by_index(idx).is_empty
                and value in board.get_cell_by_index(idx).candidates
            ]

            if len(cells_with_value) == 1:
                idx = cells_with_value[0]
                row = idx // 9
                col = idx % 9
                box_row, box_col = idx // 27, (idx % 9) // 3

                location = ""
                if "row" in group_name:
                    location = f"row {row + 1}, column {col + 1}"
                elif "column" in group_name:
                    location = f"row {row + 1}, column {col + 1}"
                else:
                    location = f"row {row + 1}, column {col + 1}"

                return SolveStep(
                    technique=self.name,
                    cell_index=idx,
                    value=value,
                    explanation=f"Value {value} can only go in one cell in {group_name}: "
                                f"cell at {location}",
                )

        return None
