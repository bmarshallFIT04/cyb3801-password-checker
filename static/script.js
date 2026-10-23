// HTML elements on the page
const passwordInput = document.getElementById("password");
const toggleButton = document.getElementById("togglePassword");
const checkButton = document.getElementById("checkPassword");

// Show or hide the password when the user clicks the "Show/Hide" button
toggleButton.addEventListener("click", () => {
    const isHidden = passwordInput.type === "password";
    passwordInput.type = isHidden ? "text" : "password";
    toggleButton.textContent = isHidden ? "Hide" : "Show";
});

// Run the password checks when the user clicks the "Check Password" button
checkButton.addEventListener("click", async () => {
    // Get the entered password
    const password = passwordInput.value;
    if (!password) {
        alert("Please enter a test password.");
        return;
    }
   
    // Disable check button to prevent multiple requests while waiting
    checkButton.disabled = true;

    try {
        // Send the password to Flask for checking
        const response = await fetch("/api/check", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                password: password
            })
        });

        // Check if the response had an error
        if (!response.ok) {
            throw new Error("Server error");
        }

        // Convert the response into a JS object
        const results = await response.json();

        // Display the results in the HTML
        document.getElementById("common").textContent = results.common_password;
        document.getElementById("injection").textContent = results.injection_protection;
        document.getElementById("compromised").textContent = results.compromised_password;

    } catch (error) {
        // Display error if the request fails
        alert("Could not connect to the server.");
    } finally {
        // Reactivate the button after the request is complete
        checkButton.disabled = false;
    }
});
