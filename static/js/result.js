// result.js
// -------------------------------------------
// Result screen logic
// -------------------------------------------

document.addEventListener("DOMContentLoaded", () => {
    const finalScoreEl = document.getElementById("final-score");
    
    // Exit if not on result page
    if (!finalScoreEl) return;
    
    const resultDifficultyEl = document.getElementById("result-difficulty");
    const resultTimeEl = document.getElementById("result-time");
    const resultMistakesEl = document.getElementById("result-mistakes");
    const historyListEl = document.getElementById("history-list");
    const playAgainBtn = document.getElementById("play-again-btn");
    const homeBtnResult = document.getElementById("home-btn-result");

    // Get score data from sessionStorage
    const finalScore = sessionStorage.getItem("finalScore") || "0";
    const gameTime = parseInt(sessionStorage.getItem("gameTime") || "0");
    const gameMistakes = parseInt(
        sessionStorage.getItem("gameMistakes") || "0",
    );
    const gameDifficulty = sessionStorage.getItem("gameDifficulty") || "easy";

    // Format time
    const minutes = Math.floor(gameTime / 60);
    const seconds = gameTime % 60;
    const timeString = `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;

    // Update display
    finalScoreEl.textContent = finalScore;
    resultDifficultyEl.textContent =
        gameDifficulty.charAt(0).toUpperCase() + gameDifficulty.slice(1);
    resultTimeEl.textContent = timeString;
    resultMistakesEl.textContent = gameMistakes;

    // Load score history from backend
    loadScoreHistory();

    // Event listeners
    playAgainBtn.addEventListener("click", () => {
        sessionStorage.clear();
        window.location.href = "/";
    });

    homeBtnResult.addEventListener("click", () => {
        sessionStorage.clear();
        window.location.href = "/";
    });
});

// -------------------------------------------
// Load score history
// -------------------------------------------
async function loadScoreHistory() {
    const historyListEl = document.getElementById("history-list");
    if (!historyListEl) return;

    try {
        const response = await fetch("/api/get-scores", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });

        if (!response.ok) {
            historyListEl.innerHTML =
                '<p data-i18n="no-scores">No scores yet</p>';
            return;
        }

        const data = await response.json();
        const scores = data.scores || [];

        if (scores.length === 0) {
            historyListEl.innerHTML =
                '<p data-i18n="no-scores">No scores yet</p>';
            return;
        }

        // Display only the last 5 scores
        const recentScores = scores.slice(0, 5);
        historyListEl.innerHTML = recentScores
            .map(
                (score) => `
            <div class="history-item">
                <div class="history-item-left">
                    <span class="difficulty-badge ${score.difficulty}">${score.difficulty.toUpperCase()}</span>
                    <span>${formatTime(score.time_seconds)}</span>
                </div>
                <div class="history-score">${score.score}</div>
            </div>
        `,
            )
            .join("");
    } catch (error) {
        console.error("Error loading score history:", error);
        historyListEl.innerHTML =
            '<p data-i18n="error">Error loading scores</p>';
    }
}

// -------------------------------------------
// Helper functions
// -------------------------------------------
function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${String(mins).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;
}
