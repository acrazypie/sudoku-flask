"""
Flask Sudoku Web Application
Entry point for the Flask application

Run with: python app.py
"""

from app import create_app

# Create and run the Flask application
app = create_app()

if __name__ == "__main__":
    # Run development server
    app.run(debug=True, host="127.0.0.1", port=5000)
