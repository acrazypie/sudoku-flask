"""
Full board generator using randomized backtracking.
"""

import random
from ..board.board import Board
from ..board.constants import GRID_SIZE, ALL_VALUES, ROW_INDICES, COL_INDICES, BOX_INDICES


class FullBoardGenerator:
    """Generates complete valid Sudoku solutions."""

    def generate(self) -> Board:
        """
        Generate a complete valid Sudoku board.

        Returns:
            A fully solved 9x9 Sudoku board
        """
        board = Board()
        self._fill_board(board)
        return board

    def _fill_board(self, board: Board) -> bool:
        """Recursively fill the board using backtracking."""
        empty_cells = board.get_empty_cells()
        if not empty_cells:
            return True

        cell_index = empty_cells[0]
        row = cell_index // 9
        col = cell_index % 9

        candidates = self._get_valid_candidates(board, row, col)
        candidates = list(candidates)
        random.shuffle(candidates)

        for value in candidates:
            board.set_value(row, col, value, fixed=False)
            if self._fill_board(board):
                return True

        board.set_value(row, col, 0, fixed=False)
        return False

    def _get_valid_candidates(self, board: Board, row: int, col: int) -> set:
        """Get valid candidate values for a cell."""
        used = set()
        used.update(board.get_row_values(row))
        used.update(board.get_col_values(col))
        box_row, box_col = board.get_box_for_cell(row, col)
        used.update(board.get_box_values(box_row, box_col))
        return ALL_VALUES - used
