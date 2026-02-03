"""
API routes for Sudoku game
Handles puzzle generation, solving, validation, and scoring
"""

from flask import Blueprint, jsonify, request, session
from sudoku_solver import SudokuSolver

api_bp = Blueprint("api", __name__, url_prefix="/api")
sudoku = SudokuSolver()


@api_bp.route("/generate", methods=["POST"])
def generate_puzzle():
    """Generate a new Sudoku puzzle based on difficulty"""
    data = request.get_json() or {}
    difficulty = data.get("difficulty", "easy")

    try:
        puzzle = sudoku.generate(difficulty)

        # Solve the puzzle to get the solution
        solution = sudoku.solve(puzzle)

        # Store in session
        session["puzzle"] = puzzle
        session["solution"] = solution
        session["difficulty"] = difficulty

        return jsonify({"success": True, "puzzle": puzzle, "difficulty": difficulty})
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


@api_bp.route("/score", methods=["POST"])
def save_score():
    """
    Save game score to session.

    Expected JSON:
    {
        "difficulty": "easy|medium|expert|master|extreme",
        "time": <seconds>,
        "mistakes": <number>,
        "score": <calculated score>
    }
    """
    data = request.get_json() or {}

    try:
        # Get or create scores list in session
        if "scores" not in session:
            session["scores"] = []

        score_entry = {
            "difficulty": data.get("difficulty", "unknown"),
            "time": data.get("time", 0),
            "mistakes": data.get("mistakes", 0),
            "score": data.get("score", 0),
            "timestamp": data.get("timestamp", ""),
        }

        # Add to scores list
        session["scores"].append(score_entry)
        session.modified = True

        # Calculate statistics
        scores_list = [s["score"] for s in session["scores"]]
        stats = {
            "current_score": score_entry["score"],
            "total_games": len(session["scores"]),
            "highest_score": max(scores_list) if scores_list else 0,
            "average_score": sum(scores_list) / len(scores_list) if scores_list else 0,
            "all_scores": session["scores"],
        }

        return jsonify({"success": True, "stats": stats})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
