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

            // Clicking on a prefilled cell selects it and highlights same numbers
            cell.addEventListener("click", () => {
                selectCell(cell);
                highlightSameNumbers(char);
            });

            // Show same numbers on hover too
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
            // Normal editable cell
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
// Start Game (with Flask API)
// -------------------------------------------
startBtn.addEventListener("click", async () => {
    // Reset UI variables
    mistakes = 0;
    hintsLeft = 2;
    errCounter.textContent = mistakes;
    numHint.textContent = hintsLeft;

    // Track time for generation speed
    const t0 = performance.now();

    try {
        // Generate a new puzzle via Flask API
        const generateResponse = await fetch("/api/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ difficulty: selectedDifficulty }),
        });

        if (!generateResponse.ok) {
            throw new Error("Failed to generate puzzle");
        }

        const generateData = await generateResponse.json();
        const board = generateData.puzzle;

        // Solve the puzzle via Flask API
        const solveResponse = await fetch("/api/solve", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ board: board }),
        });

        if (!solveResponse.ok) {
            throw new Error("Failed to solve puzzle");
        }

        const solveData = await solveResponse.json();
        const solved = solveData.solution;

        const t1 = performance.now();
        const genTime = ((t1 - t0) / 1000).toFixed(2);

        console.log(
            `Generated new ${selectedDifficulty} puzzle in ${genTime}s`,
        );

        // Save game state to sessionStorage for the game page
        sessionStorage.setItem("puzzle", board);
        sessionStorage.setItem("solution", solved);
        sessionStorage.setItem("timestamp", Date.now());

        // Navigate to game page
        window.location.href = "/game";
    } catch (error) {
        console.error("Error starting game:", error);
        alert("Error generating puzzle. Please try again.");
    }
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

    // Highlight all same numbers even if no cell selected
    clearHighlights();
    highlightSameNumbers(number);

    // Also reapply selection highlight if one is active
    if (selectedCell) {
        selectedCell.classList.add("selected");
        highlightRowColBox(selectedCell);
        if (selectedCell.textContent)
            highlightSameNumbers(selectedCell.textContent);
    }

    // If a cell is selected, place the number
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
        // Set cookie to indicate win
        document.cookie = "game_state=won; path=/; max-age=300";
        window.location.href = "/win";
    }
}

function gameOver() {
    stopTimer();
    // Set cookie to indicate loss
    document.cookie = "game_state=lost; path=/; max-age=300";
    window.location.href = "/over";
}

// -------------------------------------------
// Retry / Home
// -------------------------------------------
overBtn.addEventListener("click", () => {
    // Clear game state cookie
    document.cookie = "game_state=; path=/; max-age=0";
    window.location.href = "/";
});

homeBtn.addEventListener("click", () => {
    // Clear game state cookie
    document.cookie = "game_state=; path=/; max-age=0";
    window.location.href = "/";
});

// -------------------------------------------
// Initialize game page (when loaded)
// -------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
    // Check if we're on the game page and have puzzle data
    if (boardContainer && sessionStorage.getItem("puzzle")) {
        currentBoard = sessionStorage.getItem("puzzle");
        solution = sessionStorage.getItem("solution");

        // Reset game variables
        mistakes = 0;
        hintsLeft = 2;
        undoStack = [];
        errCounter.textContent = mistakes;
        numHint.textContent = hintsLeft;

        // Load board visually
        generateBoard(currentBoard);

        // Start timer
        startTimer();
    }
});
