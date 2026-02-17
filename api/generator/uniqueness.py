"""
Uniqueness checker for Sudoku puzzles.
"""

from ..board.board import Board
from ..board.constants import EMPTY_CELL


class UniquenessChecker:
    """Checks if a puzzle has a unique solution."""

    def has_unique_solution(self, board: Board, max_solutions: int = 2) -> bool:
        """
        Check if the puzzle has a unique solution.

        Args:
            board: The puzzle board to check
            max_solutions: Maximum solutions to find (default 2)

        Returns:
            True if puzzle has exactly one solution
        """
        solution_count = [0]

        def solve(board: Board) -> bool:
            empty_cells = board.get_empty_cells()
            if not empty_cells:
                solution_count[0] += 1
                return solution_count[0] >= max_solutions

            cell_index = empty_cells[0]
            row = cell_index // 9
            col = cell_index % 9

            candidates = self._get_valid_candidates(board, row, col)

            for value in candidates:
                board.set_value(row, col, value, fixed=False)
                if solve(board):
                    board.set_value(row, col, EMPTY_CELL, fixed=False)
                    return True
                board.set_value(row, col, EMPTY_CELL, fixed=False)

            return False

        solve(board)
        return solution_count[0] == 1

    def _get_valid_candidates(self, board: Board, row: int, col: int) -> set:
        """Get valid candidate values for a cell."""
        from ..board.constants import ALL_VALUES

        used = set()
        used.update(board.get_row_values(row))
        used.update(board.get_col_values(col))
        box_row, box_col = board.get_box_for_cell(row, col)
        used.update(board.get_box_values(box_row, box_col))
        return ALL_VALUES - used


def count_solutions(board: Board) -> int:
    """
    Count the number of solutions for a puzzle.

    Args:
        board: The puzzle board

    Returns:
        Number of solutions found (capped at 3)
    """
    solution_count = [0]

    def solve(board: Board) -> bool:
        empty_cells = board.get_empty_cells()
        if not empty_cells:
            solution_count[0] += 1
            return solution_count[0] >= 3

        cell_index = empty_cells[0]
        row = cell_index // 9
        col = cell_index % 9

        candidates = get_valid_candidates(board, row, col)

        for value in candidates:
            board.set_value(row, col, value, fixed=False)
            if solve(board):
                board.set_value(row, col, EMPTY_CELL, fixed=False)
                return True
            board.set_value(row, col, EMPTY_CELL, fixed=False)

        return False

    solve(board)
    return solution_count[0]


def get_valid_candidates(board: Board, row: int, col: int) -> set:
    """Get valid candidate values for a cell."""
    from ..board.constants import ALL_VALUES

    used = set()
    used.update(board.get_row_values(row))
    used.update(board.get_col_values(col))
    box_row, box_col = board.get_box_for_cell(row, col)
    used.update(board.get_box_values(box_row, box_col))
    return ALL_VALUES - used
