from flask import Blueprint, request, jsonify, session
from backend.app.services.cart_service import (
    add_to_cart,
    get_cart_items,
    get_cart_count,
    get_cart_details
)

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")


def require_login():
    if "user_id" not in session:
        return jsonify({"error": "Login required"}), 401
    return None


@cart_bp.route("", methods=["POST"])
def add_cart_item():
    if "user_id" not in session:
        return jsonify({"error": "Login required"}), 401
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    try:
        add_to_cart(session["user_id"], data.get(
            "product_id"), data.get("quantity", 1))
        return jsonify({"message": "Added to cart"}), 201
    except Exception as e:
        print("CART ERROR:", e)
        return jsonify({"error": "Internal server error"}), 500


@cart_bp.route("", methods=["GET"])
def view_cart():
    login_error = require_login()
    if login_error:
        return login_error

    items = get_cart_items(session["user_id"])
    return jsonify(items), 200


@cart_bp.route("/count", methods=["GET"])
def cart_count():
    login_error = require_login()
    if login_error:
        return login_error

    count = get_cart_count(session["user_id"])
    return jsonify({"count": count}), 200


@cart_bp.route("/details", methods=["GET"])
def cart_details():
    login_error = require_login()
    if login_error:
        return login_error

    items, total = get_cart_details(session["user_id"])
    return jsonify({
        "items": items,
        "total": total
    }), 200
