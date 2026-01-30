# 🎮 Sudoku Game - Flask Web Application

A professional web-based Sudoku game with Python backend logic running on Flask.

**[🌐 Play Now](http://localhost:5000)** | **[🔗 GitHub](https://github.com/acrazypie/sudoku-game)**

## ✨ Features

- 🎯 **5 Difficulty Levels**: Easy, Medium, Expert, Master, Extreme
- 🌍 **Multi-language**: English, Italiano, Français, Deutsch, Español, 日本語
- 🌙 **Dark Mode**: Light and dark themes with cohesive colors
- 📱 **Mobile Responsive**: Perfectly optimized for all devices
- ⏱️ **Built-in Timer**: Track your game duration
- 💡 **Hints System**: 2 hints per puzzle when you're stuck
- ↩️ **Undo**: Revert your last move
- 🎨 **Intuitive UI**: Integrated numpad and automatic highlighting
- ✅ **Real-time Validation**: Immediate feedback on moves
- 🐍 **Python Backend**: All Sudoku logic powered by Python

## 🚀 How to Play

1. Select your difficulty level
2. Click "Start" to begin a new game
3. Click on an empty cell to select it
4. Choose a number from the numpad
5. The game automatically validates your move
6. Complete the grid to win!

## 🛠️ Tech Stack

**Backend:**
- Python 3.8+
- Flask 3.0.0
- sudoku_solver.py (Python port of sudoku.js)

**Frontend:**
- HTML5 with Jinja2 templates
- CSS3 with responsive grid layout
- JavaScript ES6+ with async/await
- Bootstrap Icons

**Architecture:**
- Flask Blueprints for modular routes
- Application Factory pattern
- RESTful API endpoints
- Template inheritance

## 📁 Project Structure

```
sudoku-flask/
├── app/                          # Flask application package
│   ├── __init__.py              # Application factory
│   ├── routes/                  # Route blueprints
│   │   ├── __init__.py
│   │   ├── main.py              # Page routes (/)
│   │   └── api.py               # API endpoints (/api/*)
│   └── templates/               # Jinja2 templates
│       ├── base.html            # Base template (header/footer)
│       └── index.html           # Game content (extends base)
├── static/                      # Static assets
│   ├── css/
│   │   └── style.css            # Game styling
│   ├── js/
│   │   ├── script.js            # Game UI logic (calls Flask API)
│   │   ├── lang.js              # Language support
│   │   ├── theme.js             # Theme switching
│   │   └── sudoku.js            # Original solver (legacy)
│   ├── lang/                    # Translations
│   │   ├── en.json
│   │   ├── it.json
│   │   ├── fr.json
│   │   ├── de.json
│   │   ├── es.json
│   │   └── ja.json
│   ├── icons/                   # Game icons
│   └── fonts/                   # Font files
├── app.py                       # Flask entry point
├── sudoku_solver.py             # Python Sudoku logic
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

## 📊 Difficulty Levels

| Level    | Givens | Description            |
| -------- | ------ | ---------------------- |
| Easy     | 62     | Perfect for beginners   |
| Medium   | 52     | A moderate challenge   |
| Expert   | 42     | For experienced players |
| Master   | 32     | Very challenging       |
| Extreme  | 22     | Maximum difficulty     |

## 🌐 Supported Languages

- 🇬🇧 English
- 🇮🇹 Italiano
- 🇫🇷 Français
- 🇩🇪 Deutsch
- 🇪🇸 Español
- 🇯🇵 日本語

Language is automatically detected from browser preferences. Change it anytime from the header menu.

## 🎨 Themes

- **Light Mode**: Bright theme with pastel colors for daytime play
- **Dark Mode**: Relaxing green theme for evening play

Theme preference is saved to localStorage.

## 📱 Responsive Design

Fully responsive across all devices:

- ✅ Desktop (1024px+)
- ✅ Tablet (768px - 1023px)
- ✅ Mobile (< 768px)

## 🔒 Game Features

### Validation

- Automatic verification of entered numbers
- Maximum 3 errors before game over
- Errors highlighted with shake animation

### Smart Hints

- 2 hints per puzzle
- Each hint fills one correct cell

### Highlighting

- Row, column, and box of selected cell highlighted
- Matching numbers highlighted across grid
- Related cells tinted for clarity

## 💾 Saved State

The app automatically saves:

- Preferred language
- Preferred theme (light/dark)
- Selected difficulty level

## 🔌 API Endpoints

### Generate Puzzle
**POST** `/api/generate`
```json
{"difficulty": "easy"}
→ {"success": true, "puzzle": "53..7....6..195..."}
```

### Solve Puzzle
**POST** `/api/solve`
```json
{"board": "53..7....6..195..."}
→ {"success": true, "solution": "534678912672195348..."}
```

### Get Hint
**POST** `/api/get-hint`
```json
{"solution": "534678...", "board": "53..7...."}
→ {"success": true, "index": 5, "value": "6"}
```

### Validate Move
**POST** `/api/validate`
```json
{"index": 0, "value": "5", "solution": "534..."}
→ {"success": true, "correct": true}
```

## ⚙️ Installation & Setup

### Requirements

- Python 3.8+
- Flask 3.0.0

### Installation

```bash
git clone https://github.com/acrazypie/sudoku-game
cd sudoku-flask
pip install -r requirements.txt
```

## 🚀 Running the Application

### Development Server

```bash
python3 app.py
```

Visit: `http://localhost:5000`

### Production Deployment

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## 🧠 Sudoku Solver Algorithm

The Python solver uses advanced techniques:

- **Constraint Propagation**: Eliminates candidates based on Sudoku rules
- **Backtracking**: When propagation isn't sufficient
- **Depth-First Search**: With candidate-count heuristics for efficiency

## 🔧 Development

### Adding Features

1. **New Routes**: Create blueprint in `app/routes/`
2. **New Pages**: Extend `base.html` in templates
3. **New API**: Add endpoints in `app/routes/api.py`
4. **Configuration**: Update `app/__init__.py`

### Testing the Solver

```python
from sudoku_solver import SudokuSolver

sudoku = SudokuSolver()
puzzle = sudoku.generate('easy')
solution = sudoku.solve(puzzle)
print(solution)
```

## 🗺️ Roadmap

- [ ] Dynamic puzzle generation (currently pre-generated)
- [ ] Advanced solving strategies
- [ ] Leaderboards and scoring system
- [ ] Multiplayer support
- [ ] Database integration
- [ ] User accounts and profiles
- [ ] Game statistics tracking

## 🐛 Known Issues

None at the moment! If you find a bug, please report it on [GitHub Issues](https://github.com/acrazypie/sudoku-game/issues).

## 🤝 Contributing

Contributions are welcome! To improve the app:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Sudoku Solver**: Based on [sudoku.js](https://github.com/robatron/sudoku.js) by robatron
- **Icons**: Bootstrap Icons
- **Fonts**: Outfit Font
- **Game Design**: Elisa's Sudoku project

## ☕ Support the Developer

If you enjoy this project and want to support me:

- ⭐ Star this repository
- 🐦 Share with friends
- ☕ [Buy me a coffee](https://ko-fi.com/egenesio)

## 📧 Contact

- 🌐 [Personal Website](https://egenesio.com)
- 💼 [GitHub](https://github.com/acrazypie)
- ☕ [Ko-fi](https://ko-fi.com/egenesio)

---

**Enjoy your Sudoku experience! 🎮**
