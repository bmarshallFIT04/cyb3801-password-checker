const passwordInput = document.getElementById("password");
const toggleButton = document.getElementById("togglePassword");
const checkButton = document.getElementById("checkPassword");

toggleButton.addEventListener("click", () => {
    const isHidden = passwordInput.type === "password";

    passwordInput.type = isHidden ? "text" : "password";
    toggleButton.textContent = isHidden ? "Hide" : "Show";
});

checkButton.addEventListener("click", async () => {
    const password = passwordInput.value;

    if (!password) {
        alert("Please enter a test password.");
        return;
    }

    checkButton.disabled = true;

    try {
        const response = await fetch("/api/check", {
            method: "POST"
        });

        if (!response.ok) {
            throw new Error("Server error");
        }

        const results = await response.json();

        document.getElementById("common").textContent =
            results.common_password;

        document.getElementById("injection").textContent =
            results.injection_protection;

        document.getElementById("compromised").textContent =
            results.compromised_password;

    } catch (error) {
        alert("Could not connect to the server.");
    } finally {
        checkButton.disabled = false;
    }
});
