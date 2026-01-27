from flask import Blueprint, render_template, session, redirect, url_for

pages_bp = Blueprint("pages", __name__)


@pages_bp.route("/")
def home():
    return render_template("index.html")


@pages_bp.route("/dashboard")
def dashboard():
    return render_template("index.html")


@pages_bp.route("/order-summary")
def order_summary_page():
    return render_template("order_summary.html")
