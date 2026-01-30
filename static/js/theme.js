document.addEventListener("DOMContentLoaded", async () => {
    const body = document.body;
    const lightBtn = document.getElementById("light-mode");
    const darkBtn = document.getElementById("dark-mode");

    // Reads the saved theme (or sets light)
    const savedTheme = localStorage.getItem("theme") || "light";
    body.classList.toggle("dark-theme", savedTheme === "dark");

    if (savedTheme === "dark") {
        darkBtn.disabled = true;
        lightBtn.disabled = false;
        lightBtn.classList.remove("active");
        darkBtn.classList.add("active");
    } else {
        lightBtn.disabled = true;
        darkBtn.disabled = false;
        darkBtn.classList.remove("active");
        lightBtn.classList.add("active");
    }

    // Function to change theme
    const setTheme = (theme) => {
        const isLight = theme === "light";
        body.classList.toggle("dark-theme", !isLight);
        localStorage.setItem("theme", theme);

        lightBtn.disabled = isLight;
        darkBtn.disabled = !isLight;
        lightBtn.classList.toggle("active", isLight);
        darkBtn.classList.toggle("active", !isLight);
    };

    // Event listeners
    lightBtn.addEventListener("click", () => setTheme("light"));
    darkBtn.addEventListener("click", () => setTheme("dark"));
});
