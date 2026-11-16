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

        // Convert the response into a JS object first so validation errors can be read
        const results = await response.json();

        // Check if the response had a validation/server error (e.g., >128 chars or null bytes)
        if (!response.ok) {
            alert(results.error || "Invalid password input.");
            return;
        }

        // Display the results in the HTML safely using .textContent (prevents DOM XSS)
        document.getElementById("common").textContent = results.common_password;

        const injection = document.getElementById("injection");
        injection.textContent = results.injection_protection;
        injection.classList.toggle("safe", results.injection_protection.startsWith("SAFE:"));
        injection.classList.toggle("danger", results.injection_protection.startsWith("WARNING") || results.injection_protection.startsWith("BLOCKED"));
        /*
            Compromised Password Result
        */
        const compromised = document.getElementById("compromised");
        compromised.textContent = results.compromised_password.message;
        compromised.classList.toggle("safe", results.compromised_password.is_compromised === false);
        compromised.classList.toggle("danger", results.compromised_password.is_compromised === true);

    } catch (error) {
        // Display error if the request fails
        alert("Could not connect to the server.");
    } finally {
        // Reactivate the button after the request is complete
        checkButton.disabled = false;
    }
});
