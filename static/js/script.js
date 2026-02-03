// script.js
// -------------------------------------------
// Game logic for Sudoku UI using Flask API backend
// -------------------------------------------

// --- VARS ---
let selectedCell = null;
let currentBoard = "";
let solution = "";
let mistakes = 0;
let timer = null;
let seconds = 0;
let hintsLeft = 2;
let undoStack = [];
let selectedDifficulty = "easy";

// --- ELEMENTS ---
const boardContainer = document.getElementById("board");
const startBtn = document.getElementById("start-button");
const overBtn = document.getElementById("over-button");
const homeBtn = document.getElementById("home-button");
const diffBtns = document.querySelectorAll(".diff-select button");
const errCounter = document.getElementById("err-counter");
const hintBtn = document.getElementById("hint");
const undoBtn = document.getElementById("undo");
const timerMin = document.getElementById("timer-min");
const timerSec = document.getElementById("timer-sec");
const numPad = document.getElementById("numPad");
const numHint = document.getElementById("num-hint");

// -------------------------------------------
// Scoring Constants
// -------------------------------------------
const DIFFICULTY_MULTIPLIER = {
    easy: 1.0,
    medium: 1.5,
    expert: 2.0,
    master: 3.0,
    extreme: 5.0,
};

const BASE_SCORE = 1000;
const BONUS_PER_SECOND = 0.5; // Points for fast solving
const PENALTY_PER_MISTAKE = 50; // Points deducted per mistake

// -------------------------------------------
// Difficulty selection
// -------------------------------------------
diffBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
        diffBtns.forEach((b) => b.classList.remove("Dselected"));
        btn.classList.add("Dselected");
        selectedDifficulty = btn.id;
        localStorage.setItem("diff", selectedDifficulty);
    });
});

const savedDiff = localStorage.getItem("diff");
if (savedDiff) {
    diffBtns.forEach((b) => {
        b.classList.toggle("Dselected", b.id === savedDiff);
    });
    selectedDifficulty = savedDiff;
}

// -------------------------------------------
// Timer
// -------------------------------------------
function startTimer() {
    seconds = 0;
    clearInterval(timer);
    timer = setInterval(() => {
        seconds++;
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        timerMin.textContent = String(mins).padStart(2, "0");
        timerSec.textContent = String(secs).padStart(2, "0");
    }, 1000);
}

function stopTimer() {
    clearInterval(timer);
}

// -------------------------------------------
// Scoring
// -------------------------------------------
function calculateScore(difficulty, timeTaken, mistakesMade) {
    // Calculate score based on:
    // - Base score: 1000
    // - Difficulty multiplier: 1.0x (easy) to 5.0x (extreme)
    // - Time bonus: Extra points for solving fast
    // - Mistake penalty: -50 points per mistake

    const multiplier = DIFFICULTY_MULTIPLIER[difficulty] || 1.0;
    const baseWithMultiplier = BASE_SCORE * multiplier;
    const timeBonus = Math.max(0, (600 - timeTaken) * BONUS_PER_SECOND);
    const mistakePenalty = mistakesMade * PENALTY_PER_MISTAKE;

    const finalScore = Math.max(
        0,
        baseWithMultiplier + timeBonus - mistakePenalty,
    );
    return Math.round(finalScore);
}

// -------------------------------------------
// Generate board
// -------------------------------------------
function generateBoard(boardString) {
    boardContainer.innerHTML = "";
    const chars = boardString.split("");

    chars.forEach((char, i) => {
        const cell = document.createElement("div");
        cell.classList.add("cell");
        cell.dataset.index = i;

        if (char !== ".") {
            cell.textContent = char;
            cell.classList.add("prefilled");

            cell.addEventListener("click", () => {
                selectCell(cell);
                highlightSameNumbers(char);
            });

            cell.addEventListener("mouseenter", () => {
                clearHighlights();
                highlightSameNumbers(char);
            });
            cell.addEventListener("mouseleave", () => {
                clearHighlights();
                if (selectedCell) {
                    highlightRowColBox(selectedCell);
                    if (selectedCell.textContent)
                        highlightSameNumbers(selectedCell.textContent);
                    selectedCell.classList.add("selected");
                }
            });
        } else {
            cell.addEventListener("click", () => selectCell(cell));
        }

        cell.addEventListener("mouseenter", () => {
            if (!cell.classList.contains("selected")) {
                clearHighlights();
                highlightRowColBox(cell);
                if (cell.textContent) highlightSameNumbers(cell.textContent);
            }
        });
        cell.addEventListener("mouseleave", () => {
            if (!cell.classList.contains("selected")) clearHighlights();
            if (selectedCell) {
                highlightRowColBox(selectedCell);
                if (selectedCell.textContent)
                    highlightSameNumbers(selectedCell.textContent);
                selectedCell.classList.add("selected");
            }
        });

        boardContainer.appendChild(cell);
    });
}

// -------------------------------------------
// Start Game (with Flask API and loading screen)
// -------------------------------------------
startBtn.addEventListener("click", async () => {
    // Store difficulty in sessionStorage so loading page can access it
    sessionStorage.setItem("difficulty", selectedDifficulty);

    // Show loading screen - generation will happen on that page
    window.location.href = "/loading";
});

// -------------------------------------------
// Cell selection
// -------------------------------------------
function selectCell(cell) {
    clearHighlights();
    cell.classList.add("selected");
    selectedCell = cell;
    highlightRowColBox(cell);
    if (cell.textContent) highlightSameNumbers(cell.textContent);
}

// --- Highlight helpers ---
function highlightRowColBox(cell) {
    const idx = parseInt(cell.dataset.index);
    const row = Math.floor(idx / 9);
    const col = idx % 9;

    const cells = boardContainer.querySelectorAll(".cell");
    cells.forEach((c, i) => {
        const r = Math.floor(i / 9);
        const cCol = i % 9;

        const boxRow = Math.floor(r / 3);
        const boxCol = Math.floor(cCol / 3);
        const selBoxRow = Math.floor(row / 3);
        const selBoxCol = Math.floor(col / 3);

        if (
            r === row ||
            cCol === col ||
            (boxRow === selBoxRow && boxCol === selBoxCol)
        ) {
            c.classList.add("related");
        }
    });
}

function highlightSameNumbers(num) {
    const cells = boardContainer.querySelectorAll(".cell");
    cells.forEach((c) => {
        if (c.textContent === num) {
            c.classList.add("same-number");
        }
    });
}

function clearHighlights() {
    boardContainer
        .querySelectorAll(".selected, .related, .same-number")
        .forEach((el) =>
            el.classList.remove("selected", "related", "same-number"),
        );
}

// -------------------------------------------
// Number pad input
// -------------------------------------------
numPad.addEventListener("click", (e) => {
    const button = e.target.closest("button");
    if (!button) return;

    const number = button.dataset.num;

    clearHighlights();
    highlightSameNumbers(number);

    if (selectedCell) {
        selectedCell.classList.add("selected");
        highlightRowColBox(selectedCell);
        if (selectedCell.textContent)
            highlightSameNumbers(selectedCell.textContent);
    }

    if (!selectedCell) return;

    const index = Array.from(boardContainer.children).indexOf(selectedCell);

    if (solution[index] === number) {
        selectedCell.textContent = number;
        selectedCell.classList.remove("selected");
        selectedCell.classList.add("locked");
        undoStack.push({ cell: selectedCell, value: number });
        clearHighlights();
        selectedCell = null;
        checkWin();
    } else {
        mistakes++;
        errCounter.textContent = mistakes;
        selectedCell.classList.add("error");
        setTimeout(() => selectedCell.classList.remove("error"), 300);
        if (mistakes >= 3) gameOver();
    }
});

// -------------------------------------------
// Undo
// -------------------------------------------
undoBtn.addEventListener("click", () => {
    const last = undoStack.pop();
    if (!last) return;
    last.cell.textContent = "";
    last.cell.classList.remove("locked");
});

// -------------------------------------------
// Hint
// -------------------------------------------
hintBtn.addEventListener("click", () => {
    if (hintsLeft <= 0) return;
    const emptyCells = Array.from(boardContainer.children).filter(
        (c) => !c.textContent,
    );
    if (emptyCells.length === 0) return;
    const randomCell =
        emptyCells[Math.floor(Math.random() * emptyCells.length)];
    const index = Array.from(boardContainer.children).indexOf(randomCell);

    randomCell.textContent = solution[index];
    randomCell.classList.add("hinted");
    hintsLeft--;
    numHint.textContent = hintsLeft;
});

// -------------------------------------------
// Check Win / Game Over
// -------------------------------------------
function checkWin() {
    const filled = Array.from(boardContainer.children).every(
        (c) => c.textContent !== "",
    );
    if (filled) {
        stopTimer();

        const difficulty = sessionStorage.getItem("difficulty") || "easy";
        const score = calculateScore(difficulty, seconds, mistakes);

        sessionStorage.setItem("finalScore", score);
        sessionStorage.setItem("gameTime", seconds);
        sessionStorage.setItem("gameMistakes", mistakes);
        sessionStorage.setItem("gameDifficulty", difficulty);

        sendScoreToBackend(difficulty, seconds, mistakes, score);

        window.location.href = "/result";
    }
}

function gameOver() {
    stopTimer();
    document.cookie = "game_state=lost; path=/; max-age=300";
    window.location.href = "/over";
}

// -------------------------------------------
// Send score to backend
// -------------------------------------------
async function sendScoreToBackend(difficulty, timeTaken, mistakesMade, score) {
    try {
        const response = await fetch("/api/save-score", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                difficulty: difficulty,
                time: timeTaken,
                mistakes: mistakesMade,
                score: score,
                timestamp: new Date().toISOString(),
            }),
        });

        if (!response.ok) {
            console.warn("Failed to save score to backend");
        }

        const data = await response.json();
        console.log("Score saved:", data);
    } catch (error) {
        console.error("Error sending score to backend:", error);
    }
}

// -------------------------------------------
// Retry / Home
// -------------------------------------------
overBtn.addEventListener("click", () => {
    document.cookie = "game_state=; path=/; max-age=0";
    window.location.href = "/";
});

homeBtn.addEventListener("click", () => {
    document.cookie = "game_state=; path=/; max-age=0";
    window.location.href = "/";
});

// -------------------------------------------
// Initialize game page (when loaded)
// -------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
    if (boardContainer && sessionStorage.getItem("puzzle")) {
        currentBoard = sessionStorage.getItem("puzzle");
        solution = sessionStorage.getItem("solution");

        mistakes = 0;
        hintsLeft = 2;
        undoStack = [];
        errCounter.textContent = mistakes;
        numHint.textContent = hintsLeft;

        generateBoard(currentBoard);
        startTimer();
    }
});
