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

        Algorithm:
        1. Generate a complete valid solution using backtracking
        2. Remove clues while maintaining uniqueness
        3. Returns puzzle string with '.' for empty cells

        Args:
            difficulty: One of 'easy', 'medium', 'expert', 'master', 'extreme'
            unique: If True, ensures puzzle has exactly one solution

        Returns:
            Puzzle string with digits and '.' for empty cells
        """
        if difficulty not in self.DIFFICULTY:
            difficulty = "easy"

        # Step 1: Generate a complete valid solution
        solution = self._generate_full_solution()
        if not solution:
            # Fallback to pre-generated
            return self.PRE_GENERATED.get(difficulty, self.PRE_GENERATED["easy"])

        # Step 2: Remove clues based on difficulty
        target_blanks = self.DIFFICULTY[difficulty]
        puzzle = self._remove_clues(solution, target_blanks, unique)

        return puzzle

    def _generate_full_solution(self) -> Optional[str]:
        """
        Generate a complete valid Sudoku solution using backtracking.
        Returns a filled 81-character string or None if generation fails.
        """
        grid = list(self.BLANK_BOARD)

        def is_valid(idx: int, digit: str) -> bool:
            """Check if placing digit at index is valid"""
            # Get the square name for this index
            square = self.SQUARES[idx]

            # Check peers
            for peer in self.SQUARE_PEERS_MAP[square]:
                peer_idx = self.SQUARES.index(peer)
                if grid[peer_idx] == digit:
                    return False
            return True

        def backtrack(idx: int) -> bool:
            """Recursively fill the grid"""
            if idx == self.NR_SQUARES:
                return True

            # Get a list of digits in random order
            digits = list(self.DIGITS)
            random.shuffle(digits)

            for digit in digits:
                if is_valid(idx, digit):
                    grid[idx] = digit
                    if backtrack(idx + 1):
                        return True
                    grid[idx] = self.BLANK_CHAR

            return False

        if backtrack(0):
            return "".join(grid)
        return None

    def _remove_clues(
        self, solution: str, target_blanks: int, unique: bool = True
    ) -> str:
        """
        Remove clues from a complete solution to create a puzzle.

        Args:
            solution: Complete valid solution string
            target_blanks: Target number of empty cells
            unique: If True, ensures the puzzle has exactly one solution

        Returns:
            Puzzle string with clues removed
        """
        puzzle = list(solution)
        removed_count = 0
        max_attempts = self.NR_SQUARES * 2
        attempts = 0

        # Get list of all cell indices and shuffle them
        indices = list(range(self.NR_SQUARES))
        random.shuffle(indices)

        for idx in indices:
            if removed_count >= target_blanks or attempts > max_attempts:
                break

            attempts += 1

            # Skip if already blank
            if puzzle[idx] == self.BLANK_CHAR:
                removed_count += 1
                continue

            # Try removing this clue
            clue = puzzle[idx]
            puzzle[idx] = self.BLANK_CHAR

            # Check if puzzle still has unique solution (if required)
            if unique:
                solution_count = self._count_solutions("".join(puzzle), limit=2)
                if solution_count != 1:
                    # Put the clue back
                    puzzle[idx] = clue
                    continue

            removed_count += 1

        return "".join(puzzle)

    def _count_solutions(self, board: str, limit: int = 2) -> int:
        """
        Count the number of solutions for a puzzle (with early termination).

        Args:
            board: Puzzle string
            limit: Stop counting after reaching this limit

        Returns:
            Number of solutions found (capped at limit)
        """
        self.validate_board(board)

        count = [0]  # Use list to allow modification in nested function

        def search(candidates: Dict[str, str]) -> bool:
            """Search for solutions, return True to continue searching"""
            if count[0] > limit:
                return False

            if not candidates:
                return False

            # Check if solved
            all_solved = all(len(candidates[sq]) == 1 for sq in self.SQUARES)
            if all_solved:
                count[0] += 1
                return count[0] <= limit

            # Find square with minimum candidates > 1
            min_candidates_square = None
            min_nr_candidates = 10

            for square in self.SQUARES:
                nr_candidates = len(candidates[square])
                if 1 < nr_candidates < min_nr_candidates:
                    min_nr_candidates = nr_candidates
                    min_candidates_square = square

            if not min_candidates_square:
                count[0] += 1
                return count[0] <= limit

            # Try each candidate
            for val in candidates[min_candidates_square]:
                if not search(
                    self._assign(
                        json.loads(json.dumps(candidates)), min_candidates_square, val
                    )
                ):
                    pass  # Continue searching other branches

            return count[0] <= limit

        candidates = self._get_candidates_map(board)
        if candidates:
            search(candidates)

        return count[0]

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
