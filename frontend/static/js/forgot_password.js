document.addEventListener("DOMContentLoaded", () => {
    const forgotForm = document.getElementById("forgotForm");
    const resetDiv = document.getElementById("resetDiv");
    const resetBtn = document.getElementById("resetBtn");
    const msgDiv = document.getElementById("msg");

    let forgotEmail = "";

    if (!forgotForm || !resetBtn || !msgDiv) return console.error("Required elements not found");

    forgotForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        msgDiv.textContent = "";
        msgDiv.className = "";

        const email = document.getElementById("email").value.trim();
        if (!email) {
            msgDiv.textContent = "Email is required";
            msgDiv.className = "alert alert-danger";
            return;
        }

        try {
            const response = await fetch("/auth/forgot-password", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email })
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

                forgotEmail = email;
                resetDiv.style.display = "block";
                forgotForm.style.display = "none";
            } else {
                msgDiv.textContent = data.error || "Email not found";
                msgDiv.className = "alert alert-danger";
            }

        } catch (err) {
            console.error(err);
            msgDiv.textContent = "Server error. Please try again.";
            msgDiv.className = "alert alert-danger";
        }
    });

    resetBtn.addEventListener("click", async () => {
        msgDiv.textContent = "";
        msgDiv.className = "";

        const otp = document.getElementById("otp").value.trim();
        const newPassword = document.getElementById("newPassword").value.trim();

        if (!otp || !newPassword) {
            msgDiv.textContent = "OTP and new password are required";
            msgDiv.className = "alert alert-danger";
            return;
        }

        try {
            const response = await fetch("/auth/reset-password", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email: forgotEmail, otp, new_password: newPassword })
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
                msgDiv.textContent = data.error || "Failed to reset password";
                msgDiv.className = "alert alert-danger";
            }

        } catch (err) {
            console.error(err);
            msgDiv.textContent = "Server error. Please try again.";
            msgDiv.className = "alert alert-danger";
        }
    });
});