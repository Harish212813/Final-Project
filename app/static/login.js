const loginForm = document.getElementById("login-form");
const message = document.getElementById("message");

loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    message.textContent = "";

    if (password.length < 8) {
        message.textContent =
            "Password must be at least 8 characters.";
        return;
    }

    try {
        const response = await fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email,
                password
            })
        });

        const data = await response.json();

        if (!response.ok) {
            message.textContent =
                data.detail || "Login failed.";
            return;
        }

        localStorage.setItem(
            "access_token",
            data.access_token
        );

        window.location.href = "/calculations-page";
        return;

    } catch (error) {
        message.textContent =
            "Unable to connect to server.";
    }
});