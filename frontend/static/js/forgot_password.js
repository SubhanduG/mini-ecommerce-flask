const forgotForm = document.getElementById("forgotForm");
const resetDiv = document.getElementById("resetDiv");
const resetBtn = document.getElementById("resetBtn");
const msgDiv = document.getElementById("msg");

let forgotEmail = "";

forgotForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    msgDiv.textContent = "";
    msgDiv.className = "";

    const email = document.getElementById("email").value.trim();
    if (!email) {
        msgDiv.textContent = "Enter your email";
        msgDiv.className = "alert alert-danger";
        return;
    }

    try {
        const response = await fetch(forgotForm.getAttribute("action"), {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email }),
        });

        const data = await response.json();

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
        msgDiv.textContent = "Something went wrong";
        msgDiv.className = "alert alert-danger";
    }
});

resetBtn.addEventListener("click", async () => {
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
            body: JSON.stringify({ email: forgotEmail, otp, new_password: newPassword }),
        });

        const data = await response.json();

        if (response.ok) {
            msgDiv.textContent = data.message;
            msgDiv.className = "alert alert-success";
            setTimeout(() => (window.location.href = "/login"), 1500);
        } else {
            msgDiv.textContent = data.error || "Failed to reset password";
            msgDiv.className = "alert alert-danger";
        }
    } catch (err) {
        console.error(err);
        msgDiv.textContent = "Something went wrong";
        msgDiv.className = "alert alert-danger";
    }
});
