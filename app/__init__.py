"""
Flask Sudoku Web Application
A web-based Sudoku game with backend logic in Python
"""

import os
from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv
from .models import db, User
from .routes import main_bp, api_bp, auth_bp

# Load environment variables from .env file
load_dotenv()


def create_app(config=None):
    """Application factory function"""
    # Get the root directory (where css/, js/, etc. are located)
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "templates"),
        static_folder=os.path.join(root_dir, "static"),
        static_url_path="/static",
    )

    # Configuration
    app.config["JSON_SORT_KEYS"] = False
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", "dev-secret-key-change-in-production"
    )

    # Database configuration
    db_path = os.path.join(root_dir, "sudoku.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)

    # Create tables
    with app.app_context():
        db.create_all()

    return app
