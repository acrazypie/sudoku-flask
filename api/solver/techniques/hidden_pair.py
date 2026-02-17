"""
Hidden Pair solving technique.

A hidden pair occurs when two cells in the same group contain 
exactly two candidates that don't appear in any other cells 
in that group, allowing all other candidates to be removed 
from those two cells.
"""

from ...board.board import Board
from ..solve_step import SolveStep
from .base import BaseTechnique
from ...board.constants import ROW_INDICES, COL_INDICES, BOX_INDICES


class HiddenPair(BaseTechnique):
    """Find hidden pairs in rows, columns, and boxes."""

    @property
    def name(self) -> str:
        return "Hidden Pair"

    @property
    def difficulty(self) -> int:
        return 4

    def find(self, board: Board) -> SolveStep | None:
        """Find a hidden pair."""
        for row in range(9):
            step = self._check_group(board, ROW_INDICES[row], "row")
            if step:
                return step

        for col in range(9):
            step = self._check_group(board, COL_INDICES[col], "column")
            if step:
                return step

        for box in range(9):
            step = self._check_group(board, BOX_INDICES[box], "box")
            if step:
                return step

        return None

    def _check_group(self, board: Board, indices: list, group_type: str) -> SolveStep | None:
        """Check a group for hidden pairs."""
        from ...board.constants import ALL_VALUES

        value_positions = {v: [] for v in range(1, 10)}

        for idx in indices:
            cell = board.get_cell_by_index(idx)
            if cell.is_empty:
                for val in cell.candidates:
                    value_positions[val].append(idx)

        candidates_in_group = [
            (val1, val2)
            for val1 in range(1, 10)
            for val2 in range(val1 + 1, 10)
            if len(value_positions[val1]) >= 1
            and len(value_positions[val2]) >= 1
        ]

        for val1, val2 in candidates_in_group:
            cells1 = set(value_positions[val1])
            cells2 = set(value_positions[val2])

            shared_cells = cells1 & cells2

            if len(shared_cells) == 2:
                cell_list = list(shared_cells)

                other_values_in_cells = set()
                for idx in shared_cells:
                    cell = board.get_cell_by_index(idx)
                    other_values_in_cells.update(cell.candidates)

                other_values_in_cells.discard(val1)
                other_values_in_cells.discard(val2)

                if len(other_values_in_cells) > 0:
                    row1, col1 = cell_list[0] // 9, cell_list[0] % 9
                    row2, col2 = cell_list[1] // 9, cell_list[1] % 9

                    return SolveStep(
                        technique=self.name,
                        cell_index=cell_list[0],
                        candidates_removed=other_values_in_cells,
                        affected_cells=cell_list,
                        explanation=f"Found hidden pair {val1} and {val2} in cells "
                                    f"({row1 + 1}, {col1 + 1}) and ({row2 + 1}, {col2 + 1}). "
                                    f"Removed candidates {sorted(other_values_in_cells)} "
                                    f"from these cells.",
                    )

        return None
