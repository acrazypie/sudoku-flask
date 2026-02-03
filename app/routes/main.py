"""
Main page routes for Sudoku game
Handles rendering HTML templates
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models import User, db, Score

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Serve the start screen"""
    return render_template("start.html")


@main_bp.route("/game")
def game():
    """Serve the game screen"""
    return render_template("game.html")


@main_bp.route("/over")
def over():
    """Serve the game over screen - only accessible if game was lost"""
    game_state = request.cookies.get("game_state")
    if game_state != "lost":
        return redirect(url_for("main.index"))
    return render_template("over.html")


@main_bp.route("/loading")
def loading():
    """Serve the loading screen while generating puzzle"""
    return render_template("loading.html")


@main_bp.route("/result")
def result():
    """Serve the result screen after winning"""
    return render_template("result.html")


@main_bp.route("/profile")
@login_required
def profile():
    """Serve the user profile page"""
    return render_template("profile.html", user=current_user)


@main_bp.route("/api/profile/update-nickname", methods=["POST"])
@login_required
def update_nickname():
    """Update user nickname"""
    data = request.get_json()
    nickname = data.get("nickname", "").strip()

    if not nickname or len(nickname) < 1 or len(nickname) > 50:
        return (
            jsonify({"success": False, "error": "Nickname must be 1-50 characters"}),
            400,
        )

    try:
        current_user.nickname = nickname
        db.session.commit()
        return jsonify({"success": True, "message": "Nickname updated successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500


@main_bp.route("/api/save-score", methods=["POST"])
def save_score():
    """
    Save game score (works with or without authentication).
    For authenticated users, saves to database.
    For guests, saves only to session.

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
        difficulty = data.get("difficulty", "unknown")
        time_seconds = int(data.get("time", 0))
        mistakes = int(data.get("mistakes", 0))
        score = int(data.get("score", 0))

        result = {
            "success": True,
            "score": score,
            "difficulty": difficulty,
            "time": time_seconds,
            "mistakes": mistakes,
        }

        # If user is authenticated, save to database
        if current_user.is_authenticated:
            try:
                score_record = Score(
                    user_id=current_user.id,
                    difficulty=difficulty,
                    score=score,
                    time_seconds=time_seconds,
                    mistakes=mistakes,
                )
                db.session.add(score_record)
                db.session.commit()
                result["saved_to_db"] = True
            except Exception as db_error:
                db.session.rollback()
                result["saved_to_db"] = False
                result["db_error"] = str(db_error)

        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@main_bp.route("/api/get-scores", methods=["GET"])
def get_scores():
    """
    Get user scores.
    If authenticated, returns scores from database with statistics.
    Otherwise returns empty list.
    """
    try:
        if not current_user.is_authenticated:
            return jsonify(
                {
                    "success": True,
                    "scores": [],
                    "statistics": {
                        "total_games": 0,
                        "highest_score": 0,
                        "average_score": 0,
                    },
                }
            )

        # Get scores from database
        scores = (
            Score.query.filter_by(user_id=current_user.id)
            .order_by(Score.completed_at.desc())
            .all()
        )
        scores_data = [s.to_dict() for s in scores]

        # Calculate statistics
        if scores_data:
            score_values = [s["score"] for s in scores_data]
            statistics = {
                "total_games": len(scores_data),
                "highest_score": max(score_values),
                "average_score": round(sum(score_values) / len(score_values), 2),
                "by_difficulty": {},
            }

            # Group by difficulty
            for score in scores_data:
                diff = score["difficulty"]
                if diff not in statistics["by_difficulty"]:
                    statistics["by_difficulty"][diff] = {
                        "count": 0,
                        "highest": 0,
                        "average": 0,
                    }
                statistics["by_difficulty"][diff]["count"] += 1
                statistics["by_difficulty"][diff]["highest"] = max(
                    statistics["by_difficulty"][diff]["highest"], score["score"]
                )
        else:
            statistics = {
                "total_games": 0,
                "highest_score": 0,
                "average_score": 0,
                "by_difficulty": {},
            }

        return jsonify(
            {"success": True, "scores": scores_data, "statistics": statistics}
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
