"""
Naked Pair solving technique.

A naked pair occurs when two cells in the same group have exactly 
the same two candidates, allowing those candidates to be removed 
from all other cells in that group.
"""

from ...board.board import Board
from ..solve_step import SolveStep
from .base import BaseTechnique
from ...board.constants import ROW_INDICES, COL_INDICES, BOX_INDICES


class NakedPair(BaseTechnique):
    """Find naked pairs in rows, columns, and boxes."""

    @property
    def name(self) -> str:
        return "Naked Pair"

    @property
    def difficulty(self) -> int:
        return 3

    def find(self, board: Board) -> SolveStep | None:
        """Find a naked pair."""
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
        """Check a group for naked pairs."""
        empty_cells = [
            (idx, board.get_cell_by_index(idx).candidates)
            for idx in indices
            if board.get_cell_by_index(idx).is_empty
        ]

        for i, (idx1, candidates1) in enumerate(empty_cells):
            if len(candidates1) != 2:
                continue

            for idx2, candidates2 in empty_cells[i + 1:]:
                if len(candidates2) != 2:
                    continue

                if candidates1 == candidates2:
                    removed = candidates1.copy()
                    affected = []

                    for idx in indices:
                        cell = board.get_cell_by_index(idx)
                        if cell.is_empty and idx not in (idx1, idx2):
                            before_count = len(cell.candidates)
                            for cand in removed:
                                cell.remove_candidate(cand)
                            if len(cell.candidates) < before_count:
                                affected.append(idx)

                    if affected:
                        row1, col1 = idx1 // 9, idx1 % 9
                        row2, col2 = idx2 // 9, idx2 % 9

                        return SolveStep(
                            technique=self.name,
                            cell_index=idx1,
                            candidates_removed=removed,
                            affected_cells=affected,
                            explanation=f"Cells at ({row1 + 1}, {col1 + 1}) and "
                                        f"({row2 + 1}, {col2 + 1}) form a naked pair "
                                        f"with candidates {sorted(removed)}. "
                                        f"Removing these from {len(affected)} related cells.",
                        )

        return None
