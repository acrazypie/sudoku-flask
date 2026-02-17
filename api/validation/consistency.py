"""
Consistency checker for Sudoku boards.
"""

from ..board.board import Board
from ..board.constants import EMPTY_CELL


def check_consistency(board: Board) -> tuple[bool, list]:
    """
    Check if a board is consistent.

    Returns:
        (is_consistent, list of issues)
    """
    issues = []

    for row in range(9):
        duplicates = _find_duplicates_in_row(board, row)
        if duplicates:
            issues.append(f"Row {row + 1} has duplicates: {duplicates}")

    for col in range(9):
        duplicates = _find_duplicates_in_col(board, col)
        if duplicates:
            issues.append(f"Column {col + 1} has duplicates: {duplicates}")

    for box in range(9):
        duplicates = _find_duplicates_in_box(board, box)
        if duplicates:
            issues.append(f"Box {box + 1} has duplicates: {duplicates}")

    return len(issues) == 0, issues


def _find_duplicates_in_row(board: Board, row: int) -> list:
    """Find duplicate values in a row."""
    values = []
    for col in range(9):
        val = board.get_value(row, col)
        if val != EMPTY_CELL:
            if val in values:
                return [val]
            values.append(val)
    return []


def _find_duplicates_in_col(board: Board, col: int) -> list:
    """Find duplicate values in a column."""
    values = []
    for row in range(9):
        val = board.get_value(row, col)
        if val != EMPTY_CELL:
            if val in values:
                return [val]
            values.append(val)
    return []


def _find_duplicates_in_box(board: Board, box: int) -> list:
    """Find duplicate values in a box."""
    from ..board.constants import BOX_INDICES

    values = []
    for idx in BOX_INDICES[box]:
        val = board.get_cell_by_index(idx).value
        if val != EMPTY_CELL:
            if val in values:
                return [val]
            values.append(val)
    return []


def is_solvable(board: Board) -> bool:
    """
    Check if a puzzle has at least one solution.

    Uses a simple backtracking solver.
    """
    from ..generator.uniqueness import count_solutions
    from ..board.constants import EMPTY_CELL

    test_board = board.copy()

    for idx in range(81):
        if test_board.get_cell_by_index(idx).is_empty:
            test_board.set_value(idx // 9, idx % 9, 0, fixed=False)

    count = count_solutions(test_board)
    return count >= 1
