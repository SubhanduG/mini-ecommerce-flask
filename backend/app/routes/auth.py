from flask import Blueprint, request, jsonify, session
from backend.app.services.auth_service import (
    create_user, verify_registration_otp, authenticate_user,
    send_forgot_password_otp, reset_password_with_otp
)

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/me", methods=["GET"])
def current_user():
    if "user_id" in session:
        return jsonify({"logged_in": True}), 200
    return jsonify({"logged_in": False}), 200


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required"}), 400

    try:
        create_user(username, email, password)
        return jsonify({"message": "OTP sent to your email. Verify to complete registration."}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print("REGISTER ERROR:", e)
        return jsonify({"error": "Internal server error"}), 500


@auth_bp.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    otp = data.get("otp")
    if not email or not otp:
        return jsonify({"error": "Email and OTP are required"}), 400

    if verify_registration_otp(email, otp):
        return jsonify({"message": "Registration verified. You can log in now."}), 200
    return jsonify({"error": "Invalid or expired OTP"}), 400


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    identifier = data.get("identifier")
    password = data.get("password")

    if not identifier or not password:
        return jsonify({"error": "Identifier and password are required"}), 400

    try:
        user = authenticate_user(identifier, password)
        if not user:
            return jsonify({"error": "Invalid credentials"}), 401
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        return jsonify({"message": "Login successful"}), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 403


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"}), 200


@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    if not email:
        return jsonify({"error": "Email is required"}), 400

    if send_forgot_password_otp(email):
        return jsonify({"message": "OTP sent to your email"}), 200
    return jsonify({"error": "Email not registered"}), 404


@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    otp = data.get("otp")
    new_password = data.get("new_password")

    if not email or not otp or not new_password:
        return jsonify({"error": "Email, OTP, and new password are required"}), 400

    if reset_password_with_otp(email, otp, new_password):
        return jsonify({"message": "Password reset successful"}), 200
    return jsonify({"error": "Invalid OTP or expired"}), 400
