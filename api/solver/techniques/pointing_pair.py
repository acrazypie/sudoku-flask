"""
Pointing Pair solving technique.

A pointing pair occurs when two cells in the same box contain 
the same candidate, and that candidate doesn't appear in any 
other cell in the same row or column outside the box. 
This allows the candidate to be eliminated from that row/column.
"""

from ...board.board import Board
from ..solve_step import SolveStep
from .base import BaseTechnique
from ...board.constants import BOX_INDICES, ROW_INDICES, COL_INDICES


class PointingPair(BaseTechnique):
    """Find pointing pairs in boxes."""

    @property
    def name(self) -> str:
        return "Pointing Pair"

    @property
    def difficulty(self) -> int:
        return 4

    def find(self, board: Board) -> SolveStep | None:
        """Find a pointing pair."""
        for box in range(9):
            step = self._check_box(board, box)
            if step:
                return step

        return None

    def _check_box(self, board: Board, box: int) -> SolveStep | None:
        """Check a box for pointing pairs."""
        indices = BOX_INDICES[box]
        box_row = box // 3
        box_col = box % 3

        cells_in_box = [
            (idx, board.get_cell_by_index(idx).candidates.copy())
            for idx in indices
            if board.get_cell_by_index(idx).is_empty
        ]

        if len(cells_in_box) < 2:
            return None

        for value in range(1, 10):
            cells_with_value = [
                idx for idx, cands in cells_in_box if value in cands
            ]

            if len(cells_with_value) < 2:
                continue

            rows = set(idx // 9 for idx in cells_with_value)
            cols = set(idx % 9 for idx in cells_with_value)

            if len(rows) == 1:
                row = rows.pop()
                affected = []

                for col in range(9):
                    if (row * 9 + col) not in indices:
                        cell = board.get_cell_by_index(row * 9 + col)
                        if cell.is_empty and value in cell.candidates:
                            cell.remove_candidate(value)
                            affected.append(row * 9 + col)

                if affected:
                    return SolveStep(
                        technique=self.name,
                        cell_index=cells_with_value[0],
                        candidates_removed={value},
                        affected_cells=affected,
                        explanation=f"Pointing pair in box {box + 1}: value {value} "
                                    f"appears only in row {row + 1}. "
                                    f"Removed {value} from {len(affected)} cells in that row "
                                    f"outside the box.",
                    )

            if len(cols) == 1:
                col = cols.pop()
                affected = []

                for row in range(9):
                    if (row * 9 + col) not in indices:
                        cell = board.get_cell_by_index(row * 9 + col)
                        if cell.is_empty and value in cell.candidates:
                            cell.remove_candidate(value)
                            affected.append(row * 9 + col)

                if affected:
                    return SolveStep(
                        technique=self.name,
                        cell_index=cells_with_value[0],
                        candidates_removed={value},
                        affected_cells=affected,
                        explanation=f"Pointing pair in box {box + 1}: value {value} "
                                    f"appears only in column {col + 1}. "
                                    f"Removed {value} from {len(affected)} cells in that column "
                                    f"outside the box.",
                    )

        return None
