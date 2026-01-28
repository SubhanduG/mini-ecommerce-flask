document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");
    const loginMsg = document.getElementById("msg");

    if (!loginForm) {
        console.error("loginForm not found");
        return;
    }

    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        loginMsg.textContent = "";
        loginMsg.className = "";

        const identifier = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value.trim();

        if (!identifier || !password) {
            loginMsg.textContent = "Username/email and password are required.";
            loginMsg.className = "alert alert-danger";
            return;
        }

        try {
            const response = await fetch(loginForm.getAttribute("action"), {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "include",
                body: JSON.stringify({ identifier, password })
            });

            const text = await response.text();
            let data;
            try {
                data = JSON.parse(text);
            } catch {
                console.error("Non-JSON response:", text);
                throw new Error("Invalid server response");
            }

            if (response.ok) {
                window.location.href = "/dashboard";
            } else {
                loginMsg.textContent = data.error || "Login failed";
                loginMsg.className = "alert alert-danger";
            }
        } catch (err) {
            console.error(err);
            loginMsg.textContent = "Server error. Please try again.";
            loginMsg.className = "alert alert-danger";
        }
    });
});