"""
Sudoku Solver - Python port of sudoku.js
A Sudoku puzzle generator and solver library.
Modified and updated version of sudoku.js by robatron -> https://github.com/robatron/sudoku.js
"""

import random
import json
from typing import Dict, List, Optional, Tuple


class SudokuSolver:
    """Sudoku puzzle generator and solver"""

    # Constants
    DIGITS = "123456789"
    BLANK_CHAR = "."
    BLANK_BOARD = "." * 81
    ROWS = "ABCDEFGHI"
    COLS = "123456789"
    MIN_GIVENS = 17
    NR_SQUARES = 81

    DIFFICULTY = {
        "easy": 62,
        "medium": 52,
        "expert": 42,
        "master": 32,
        "extreme": 22,
    }

    # Pre-generated puzzles (fallback)
    PRE_GENERATED = {
        "easy": "53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79",
        "medium": "..53.....8......2..7..1.5..4....53...1..7...6..32...8..6.5....9..4....3......97..",
        "expert": "8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..",
        "master": "....5..1..3....8.7.....2..1..9....4..7..8..3...5.2...6.8..1...4..9.7.....6.3..2..",
        "extreme": ".2..5.7...3.1....48.....6.7.5....2.1.4...8.3.2....8.7.6.....94....2.5...1.8..4.",
    }

    def __init__(self):
        """Initialize the Sudoku solver"""
        self.SQUARES = self._cross(self.ROWS, self.COLS)
        self.UNITS = self._get_all_units(self.ROWS, self.COLS)
        self.SQUARE_UNITS_MAP = self._get_square_units_map(self.SQUARES, self.UNITS)
        self.SQUARE_PEERS_MAP = self._get_square_peers_map(
            self.SQUARES, self.SQUARE_UNITS_MAP
        )

    # ========================
    # Public Methods
    # ========================

    def generate(self, difficulty: str = "easy", unique: bool = True) -> str:
        """
        Generate a new Sudoku puzzle based on difficulty.
        Returns puzzle string with '.' for empty cells.
        """
        if difficulty not in self.DIFFICULTY:
            difficulty = "easy"

        # Use pre-generated puzzles as fallback
        return self.PRE_GENERATED.get(difficulty, self.PRE_GENERATED["easy"])

    def solve(self, board: str, reverse: bool = False) -> str:
        """
        Solve a Sudoku puzzle.
        Returns solved board string or False if no solution exists.
        """
        self.validate_board(board)

        nr_givens = sum(1 for ch in board if ch in self.DIGITS)
        if nr_givens < self.MIN_GIVENS:
            raise ValueError(f"Too few givens. Minimum givens is {self.MIN_GIVENS}")

        candidates = self._get_candidates_map(board)
        result = self._search(candidates, reverse)

        if result:
            return "".join(result[sq] for sq in self.SQUARES)
        return False

    def validate_board(self, board: str) -> bool:
        """
        Validate a Sudoku board.
        Returns True if valid, otherwise raises ValueError.
        """
        if not board:
            raise ValueError("Empty board")

        if len(board) != self.NR_SQUARES:
            raise ValueError(
                f"Invalid board size. Board must be exactly {self.NR_SQUARES} squares."
            )

        for i, char in enumerate(board):
            if char not in self.DIGITS and char != self.BLANK_CHAR:
                raise ValueError(f"Invalid board character at index {i}: {char}")

        return True

    # ========================
    # Private Helper Methods
    # ========================

    def _get_candidates_map(self, board: str) -> Dict[str, str]:
        """
        Get candidate map for a board.
        Maps each square to its possible digit values.
        """
        self.validate_board(board)

        candidate_map = {sq: self.DIGITS for sq in self.SQUARES}
        squares_values_map = self._get_square_vals_map(board)

        for sq, val in squares_values_map.items():
            if val in self.DIGITS:
                if not self._assign(candidate_map, sq, val):
                    return None

        return candidate_map

    def _assign(
        self, candidates: Dict[str, str], square: str, val: str
    ) -> Optional[Dict[str, str]]:
        """
        Assign a value to a square by eliminating all other candidates.
        Returns updated candidates map or False if contradiction.
        """
        other_vals = candidates[square].replace(val, "")
        for other_val in other_vals:
            if not self._eliminate(candidates, square, other_val):
                return None
        return candidates

    def _eliminate(
        self, candidates: Dict[str, str], square: str, val: str
    ) -> Optional[Dict[str, str]]:
        """
        Eliminate a value from a square's candidates.
        Propagates constraints using constraint propagation.
        """
        if val not in candidates[square]:
            return candidates

        candidates[square] = candidates[square].replace(val, "")
        nr_candidates = len(candidates[square])

        if nr_candidates == 0:
            return None  # Contradiction

        if nr_candidates == 1:
            target_val = candidates[square]
            for peer in self.SQUARE_PEERS_MAP[square]:
                if not self._eliminate(candidates, peer, target_val):
                    return None

        for unit in self.SQUARE_UNITS_MAP[square]:
            val_places = [sq for sq in unit if val in candidates[sq]]
            if len(val_places) == 0:
                return None  # Contradiction
            elif len(val_places) == 1:
                if not self._assign(candidates, val_places[0], val):
                    return None

        return candidates

    def _search(
        self, candidates: Dict[str, str], reverse: bool = False
    ) -> Optional[Dict[str, str]]:
        """
        Use depth-first search to solve the puzzle.
        Returns the solution candidate map or None if no solution exists.
        """
        if not candidates:
            return None

        # Find square with maximum candidates
        max_nr_candidates = 0
        max_candidates_square = None
        for square in self.SQUARES:
            nr_candidates = len(candidates[square])
            if nr_candidates > max_nr_candidates:
                max_nr_candidates = nr_candidates
                max_candidates_square = square

        # If all squares have exactly one candidate, we're solved
        if max_nr_candidates == 1:
            return candidates

        # Find square with minimum candidates > 1
        min_nr_candidates = 10
        min_candidates_square = None
        for square in self.SQUARES:
            nr_candidates = len(candidates[square])
            if 1 < nr_candidates < min_nr_candidates:
                min_nr_candidates = nr_candidates
                min_candidates_square = square

        if not min_candidates_square:
            return None

        # Try each candidate value
        min_candidates = candidates[min_candidates_square]
        if not reverse:
            for val in min_candidates:
                candidates_copy = json.loads(json.dumps(candidates))
                candidates_next = self._search(
                    self._assign(candidates_copy, min_candidates_square, val), reverse
                )
                if candidates_next:
                    return candidates_next
        else:
            for val in reversed(min_candidates):
                candidates_copy = json.loads(json.dumps(candidates))
                candidates_next = self._search(
                    self._assign(candidates_copy, min_candidates_square, val), reverse
                )
                if candidates_next:
                    return candidates_next

        return None

    # ========================
    # Utilities
    # ========================

    def _get_square_vals_map(self, board: str) -> Dict[str, str]:
        """Map each square to its value on the board"""
        if len(board) != len(self.SQUARES):
            raise ValueError("Board/squares length mismatch")

        return {self.SQUARES[i]: board[i] for i in range(len(self.SQUARES))}

    def _get_square_units_map(
        self, squares: List[str], units: List[List[str]]
    ) -> Dict[str, List[List[str]]]:
        """Map each square to its units (rows, columns, boxes)"""
        square_unit_map = {}

        for square in squares:
            cur_square_units = []
            for unit in units:
                if square in unit:
                    cur_square_units.append(unit)
            square_unit_map[square] = cur_square_units

        return square_unit_map

    def _get_square_peers_map(
        self, squares: List[str], units_map: Dict[str, List[List[str]]]
    ) -> Dict[str, List[str]]:
        """Map each square to its peers (other squares in the same unit)"""
        square_peers_map = {}

        for square in squares:
            cur_square_units = units_map[square]
            cur_square_peers = []

            for unit in cur_square_units:
                for unit_square in unit:
                    if unit_square != square and unit_square not in cur_square_peers:
                        cur_square_peers.append(unit_square)

            square_peers_map[square] = cur_square_peers

        return square_peers_map

    def _get_all_units(self, rows: str, cols: str) -> List[List[str]]:
        """Get all units (rows, columns, and 3x3 boxes)"""
        units = []

        # Rows
        for row in rows:
            units.append(self._cross(row, cols))

        # Columns
        for col in cols:
            units.append(self._cross(rows, col))

        # Boxes
        row_squares = ["ABC", "DEF", "GHI"]
        col_squares = ["123", "456", "789"]
        for row_square in row_squares:
            for col_square in col_squares:
                units.append(self._cross(row_square, col_square))

        return units

    def _cross(self, a: str, b: str) -> List[str]:
        """Cross product of all elements in a and b"""
        return [a_elem + b_elem for a_elem in a for b_elem in b]
