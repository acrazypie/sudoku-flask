"""
Validation rules for Sudoku.
"""

from ..board.board import Board
from ..board.constants import EMPTY_CELL, ROW_INDICES, COL_INDICES, BOX_INDICES


def validate_complete(board: Board) -> bool:
    """
    Validate a complete solved board.

    Returns True if the board is a valid solution.
    """
    for row in range(9):
        if not _validate_group(board, ROW_INDICES[row]):
            return False

    for col in range(9):
        if not _validate_group(board, COL_INDICES[col]):
            return False

    for box in range(9):
        if not _validate_group(board, BOX_INDICES[box]):
            return False

    return True


def _validate_group(board: Board, indices: list) -> bool:
    """Validate a group (row, column, or box) has all values 1-9."""
    values = set()
    for idx in indices:
        val = board.get_cell_by_index(idx).value
        if val == EMPTY_CELL:
            return False
        if val in values:
            return False
        values.add(val)

    return values == {1, 2, 3, 4, 5, 6, 7, 8, 9}


def validate_partial(board: Board) -> tuple[bool, str]:
    """
    Validate a partial board (during solving).

    Returns (is_valid, error_message).
    """
    for row in range(9):
        if not _validate_group_partial(board, ROW_INDICES[row], f"Row {row + 1}"):
            return False, f"Invalid row {row + 1}"

    for col in range(9):
        if not _validate_group_partial(board, COL_INDICES[col], f"Column {col + 1}"):
            return False, f"Invalid column {col + 1}"

    for box in range(9):
        if not _validate_group_partial(board, BOX_INDICES[box], f"Box {box + 1}"):
            return False, f"Invalid box {box + 1}"

    return True, ""


def _validate_group_partial(board: Board, indices: list, group_name: str) -> bool:
    """Validate a group has no duplicate values."""
    values = set()
    for idx in indices:
        val = board.get_cell_by_index(idx).value
        if val != EMPTY_CELL:
            if val in values:
                return False
            values.add(val)
    return True
