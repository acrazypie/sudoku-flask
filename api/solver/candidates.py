"""
Candidate management utilities for the solver.
"""

from ..board.board import Board
from ..board.constants import ALL_VALUES


def initialize_candidates(board: Board) -> None:
    """Initialize candidate sets for all empty cells."""
    for row in range(9):
        for col in range(9):
            cell = board.get_cell(row, col)
            if cell.is_empty:
                candidates = calculate_candidates(board, row, col)
                cell.candidates = candidates


def calculate_candidates(board: Board, row: int, col: int) -> set:
    """Calculate valid candidates for a cell."""
    used = set()
    used.update(board.get_row_values(row))
    used.update(board.get_col_values(col))
    box_row, box_col = board.get_box_for_cell(row, col)
    used.update(board.get_box_values(box_row, box_col))
    return ALL_VALUES - used


def update_candidates_for_cell(board: Board, row: int, col: int) -> None:
    """Update candidates for a cell after a value is placed."""
    cell = board.get_cell(row, col)
    if cell.is_solved:
        return

    candidates = calculate_candidates(board, row, col)
    cell.candidates = candidates


def update_all_candidates(board: Board) -> None:
    """Update candidates for all empty cells."""
    for row in range(9):
        for col in range(9):
            if board.get_cell(row, col).is_empty:
                update_candidates_for_cell(board, row, col)
