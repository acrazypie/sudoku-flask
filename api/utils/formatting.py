"""
Formatting utilities for Sudoku boards and output.
"""

from ..board.board import Board


def format_board(board: Board) -> str:
    """
    Format a board as a human-readable string.

    Args:
        board: The board to format

    Returns:
        Formatted string representation
    """
    lines = []
    for row in range(9):
        row_str = ""
        for col in range(9):
            val = board.get_value(row, col)
            if val == 0:
                row_str += ". "
            else:
                row_str += f"{val} "

            if col in (2, 5):
                row_str += "| "

        lines.append(row_str.rstrip())

        if row in (2, 5):
            lines.append("-" * 21)

    return "\n".join(lines)


def format_candidates(board: Board) -> str:
    """
    Format candidate information for all cells.

    Args:
        board: The board to format

    Returns:
        Formatted string with candidates
    """
    lines = []
    for row in range(9):
        row_str = ""
        for col in range(9):
            cell = board.get_cell(row, col)
            if cell.is_solved:
                row_str += f"   {cell.value}   "
            else:
                cands = "".join(str(v) for v in sorted(cell.candidates))
                row_str += f"[{cands:9}]"
            if col < 8:
                row_str += " "
        lines.append(row_str)
    return "\n".join(lines)


def format_step(step) -> str:
    """Format a SolveStep for display."""
    row = step.cell_index // 9
    col = step.cell_index % 9

    location = f"Row {row + 1}, Col {col + 1}"

    if step.value:
        return f"Place {step.value} at {location}: {step.explanation}"
    elif step.candidates_removed:
        return f"Remove candidates {sorted(step.candidates_removed)}: {step.explanation}"

    return step.explanation
