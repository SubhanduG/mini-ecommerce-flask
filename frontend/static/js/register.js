document.addEventListener("DOMContentLoaded", () => {
    const registerForm = document.getElementById("registerForm");
    const otpDiv = document.getElementById("otpDiv");
    const verifyOtpBtn = document.getElementById("verifyOtpBtn");
    const msgDiv = document.getElementById("msg");

    let registeredEmail = "";

    if (!registerForm || !otpDiv || !verifyOtpBtn || !msgDiv) return console.error("Required elements not found");

    registerForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        msgDiv.textContent = "";
        msgDiv.className = "";

        const username = document.getElementById("username").value.trim();
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value.trim();

        if (!username || !email || !password) {
            msgDiv.textContent = "All fields are required.";
            msgDiv.className = "alert alert-danger";
            return;
        }

        try {
            const response = await fetch("/auth/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, email, password })
            });

            const text = await response.text();
            let data;
            try {
                data = JSON.parse(text);
            } catch {
                msgDiv.textContent = "Unexpected server response";
                msgDiv.className = "alert alert-danger";
                return;
            }

            if (response.ok) {
                msgDiv.textContent = data.message;
                msgDiv.className = "alert alert-success";

                registeredEmail = email;
                registerForm.style.display = "none";
                otpDiv.style.display = "block";
            } else {
                msgDiv.textContent = data.error || "Registration failed";
                msgDiv.className = "alert alert-danger";
            }

        } catch (err) {
            console.error(err);
            msgDiv.textContent = "Server error. Please try again.";
            msgDiv.className = "alert alert-danger";
        }
    });

    verifyOtpBtn.addEventListener("click", async () => {
        msgDiv.textContent = "";
        msgDiv.className = "";

        const otp = document.getElementById("otp").value.trim();
        if (!otp) {
            msgDiv.textContent = "OTP is required";
            msgDiv.className = "alert alert-danger";
            return;
        }

        try {
            const response = await fetch("/auth/verify-otp", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email: registeredEmail, otp })
            });

            const text = await response.text();
            let data;
            try {
                data = JSON.parse(text);
            } catch {
                msgDiv.textContent = "Unexpected server response";
                msgDiv.className = "alert alert-danger";
                return;
            }

            if (response.ok) {
                msgDiv.textContent = data.message;
                msgDiv.className = "alert alert-success";
                setTimeout(() => window.location.href = "/login", 1500);
            } else {
                msgDiv.textContent = data.error || "Invalid OTP";
                msgDiv.className = "alert alert-danger";
            }

        } catch (err) {
            console.error(err);
            msgDiv.textContent = "Server error. Please try again.";
            msgDiv.className = "alert alert-danger";
        }
    });
});