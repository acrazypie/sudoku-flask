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
let boardContainer, startBtn, overBtn, homeBtn, diffBtns, errCounter, hintBtn, undoBtn, timerMin, timerSec, numPad, numHint;

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
const BONUS_PER_SECOND = 0.5;
const PENALTY_PER_MISTAKE = 50;

// -------------------------------------------
// Timer
// -------------------------------------------
function startTimer() {
    if (!timerMin || !timerSec) return;
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
    const multiplier = DIFFICULTY_MULTIPLIER[difficulty] || 1.0;
    const baseWithMultiplier = BASE_SCORE * multiplier;
    const timeBonus = Math.max(0, (600 - timeTaken) * BONUS_PER_SECOND);
    const mistakePenalty = mistakesMade * PENALTY_PER_MISTAKE;
    return Math.max(0, Math.round(baseWithMultiplier + timeBonus - mistakePenalty));
}

// -------------------------------------------
// Generate board
// -------------------------------------------
function generateBoard(boardString) {
    if (!boardContainer) return;
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
                    if (selectedCell.textContent) highlightSameNumbers(selectedCell.textContent);
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
                if (selectedCell.textContent) highlightSameNumbers(selectedCell.textContent);
                selectedCell.classList.add("selected");
            }
        });

        boardContainer.appendChild(cell);
    });
}

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
        if (r === row || cCol === col || (boxRow === selBoxRow && boxCol === selBoxCol)) {
            c.classList.add("related");
        }
    });
}

function highlightSameNumbers(num) {
    const cells = boardContainer.querySelectorAll(".cell");
    cells.forEach((c) => {
        if (c.textContent === num) c.classList.add("same-number");
    });
}

function clearHighlights() {
    if (!boardContainer) return;
    boardContainer.querySelectorAll(".selected, .related, .same-number").forEach((el) =>
        el.classList.remove("selected", "related", "same-number")
    );
}

// -------------------------------------------
// Check Win / Game Over
// -------------------------------------------
function checkWin() {
    if (!boardContainer) return;
    const filled = Array.from(boardContainer.children).every((c) => c.textContent !== "");
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

async function sendScoreToBackend(difficulty, timeTaken, mistakesMade, score) {
    try {
        const response = await fetch("/api/save-score", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ difficulty, time: timeTaken, mistakes: mistakesMade, score, timestamp: new Date().toISOString() }),
        });
        if (!response.ok) console.warn("Failed to save score");
        console.log("Score saved:", await response.json());
    } catch (error) {
        console.error("Error sending score:", error);
    }
}

// -------------------------------------------
// Initialize everything when DOM is ready
// -------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
    // Initialize elements
    boardContainer = document.getElementById("board");
    startBtn = document.getElementById("start-button");
    overBtn = document.getElementById("over-button");
    homeBtn = document.getElementById("home-button");
    diffBtns = document.querySelectorAll(".diff-select button");
    errCounter = document.getElementById("err-counter");
    hintBtn = document.getElementById("hint");
    undoBtn = document.getElementById("undo");
    timerMin = document.getElementById("timer-min");
    timerSec = document.getElementById("timer-sec");
    numPad = document.getElementById("numPad");
    numHint = document.getElementById("num-hint");

    // Difficulty selection
    if (diffBtns && diffBtns.length > 0) {
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
            diffBtns.forEach((b) => b.classList.toggle("Dselected", b.id === savedDiff));
            selectedDifficulty = savedDiff;
        }
    }

    // Start button
    if (startBtn) {
        startBtn.addEventListener("click", () => {
            sessionStorage.setItem("difficulty", selectedDifficulty);
            window.location.href = "/loading";
        });
    }

    // Number pad
    if (numPad) {
        numPad.addEventListener("click", (e) => {
            const button = e.target.closest("button");
            if (!button || !selectedCell) return;
            const number = button.dataset.num;
            clearHighlights();
            highlightSameNumbers(number);
            selectedCell.classList.add("selected");
            highlightRowColBox(selectedCell);
            if (selectedCell.textContent) highlightSameNumbers(selectedCell.textContent);

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
                if (errCounter) errCounter.textContent = mistakes;
                selectedCell.classList.add("error");
                setTimeout(() => selectedCell.classList.remove("error"), 300);
                if (mistakes >= 3) gameOver();
            }
        });
    }

    // Undo button
    if (undoBtn) {
        undoBtn.addEventListener("click", () => {
            const last = undoStack.pop();
            if (last) {
                last.cell.textContent = "";
                last.cell.classList.remove("locked");
            }
        });
    }

    // Hint button
    if (hintBtn) {
        hintBtn.addEventListener("click", () => {
            if (hintsLeft <= 0 || !boardContainer) return;
            const emptyCells = Array.from(boardContainer.children).filter((c) => !c.textContent);
            if (emptyCells.length === 0) return;
            const randomCell = emptyCells[Math.floor(Math.random() * emptyCells.length)];
            const index = Array.from(boardContainer.children).indexOf(randomCell);
            randomCell.textContent = solution[index];
            randomCell.classList.add("hinted");
            hintsLeft--;
            if (numHint) numHint.textContent = hintsLeft;
        });
    }

    // Over/Home buttons
    if (overBtn) {
        overBtn.addEventListener("click", () => {
            document.cookie = "game_state=; path=/; max-age=0";
            window.location.href = "/";
        });
    }
    if (homeBtn) {
        homeBtn.addEventListener("click", () => {
            document.cookie = "game_state=; path=/; max-age=0";
            window.location.href = "/";
        });
    }

    // Initialize game if puzzle exists in sessionStorage
    if (boardContainer && sessionStorage.getItem("puzzle")) {
        currentBoard = sessionStorage.getItem("puzzle");
        solution = sessionStorage.getItem("solution");
        mistakes = 0;
        hintsLeft = 2;
        undoStack = [];
        if (errCounter) errCounter.textContent = mistakes;
        if (numHint) numHint.textContent = hintsLeft;
        generateBoard(currentBoard);
        startTimer();
    }
});
