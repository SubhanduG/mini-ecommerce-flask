from flask import Blueprint, render_template, session, redirect, url_for

pages_bp = Blueprint("pages", __name__)


@pages_bp.route("/")
def home():
    return render_template("index.html")


@pages_bp.route("/login")
def login_page():
    if "user_id" in session:
        return redirect(url_for("pages.dashboard"))
    return render_template("login.html")


@pages_bp.route("/register")
def register_page():
    if "user_id" in session:
        return redirect(url_for("pages.dashboard"))
    return render_template("register.html")


@pages_bp.route("/forgot-password")
def forgot_password_page():
    if "user_id" in session:
        return redirect(url_for("pages.dashboard"))
    return render_template("forgot_password.html")


@pages_bp.route("/dashboard")
def dashboard():
    return render_template("index.html")


@pages_bp.route("/order-summary")
def order_summary_page():
    if "user_id" not in session:
        return redirect(url_for("pages.login_page"))
    return render_template("order_summary.html")
