"""
API routes for Sudoku game
Handles puzzle generation, solving, and validation
"""

from flask import Blueprint, jsonify, request
from sudoku_solver import SudokuSolver

api_bp = Blueprint("api", __name__, url_prefix="/api")
sudoku = SudokuSolver()


@api_bp.route("/generate", methods=["POST"])
def generate_puzzle():
    """Generate a new Sudoku puzzle based on difficulty"""
    data = request.get_json()
    difficulty = data.get("difficulty", "easy")

    try:
        puzzle = sudoku.generate(difficulty)
        return jsonify({"success": True, "puzzle": puzzle})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@api_bp.route("/solve", methods=["POST"])
def solve_puzzle():
    """Solve a given Sudoku puzzle"""
    data = request.get_json()
    board = data.get("board", "")

    try:
        solution = sudoku.solve(board)
        return jsonify({"success": True, "solution": solution})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@api_bp.route("/validate", methods=["POST"])
def validate_move():
    """Validate if a move is correct"""
    data = request.get_json()
    board = data.get("board", "")
    index = data.get("index", -1)
    value = data.get("value", "")
    solution = data.get("solution", "")

    try:
        if 0 <= index < 81 and solution and index < len(solution):
            is_correct = solution[index] == value
            return jsonify({"success": True, "correct": is_correct})
        return jsonify({"success": False, "error": "Invalid index or solution"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@api_bp.route("/get-hint", methods=["POST"])
def get_hint():
    """Get a hint for the current board"""
    data = request.get_json()
    solution = data.get("solution", "")
    current_board = data.get("board", "")

    try:
        if not solution or not current_board:
            return (
                jsonify({"success": False, "error": "Missing board or solution"}),
                400,
            )

        # Find first empty cell
        for i, cell in enumerate(current_board):
            if cell == ".":
                return jsonify({"success": True, "index": i, "value": solution[i]})

        return jsonify({"success": False, "error": "No empty cells"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
