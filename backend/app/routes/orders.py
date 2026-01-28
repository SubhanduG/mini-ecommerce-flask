from flask import Blueprint, jsonify, session
from backend.app.services.order_service import place_order, get_orders

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")


def require_login():
    if "user_id" not in session:
        return jsonify({"error": "Login required"}), 401
    return None


@orders_bp.route("/confirm", methods=["POST"])
def confirm_order():
    login_error = require_login()
    if login_error:
        return login_error

    try:
        order_id = place_order()
        if order_id is None:
            return jsonify({"error": "Your cart is empty"}), 400

        return jsonify({
            "message": "Order placed successfully",
            "order_id": order_id
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        print("PLACE ORDER ERROR:", e)
        return jsonify({"error": "Internal server error"}), 500


@orders_bp.route("", methods=["GET"])
def order_history():
    login_error = require_login()
    if login_error:
        return login_error

    try:
        orders = get_orders()
        return jsonify(orders), 200

    except Exception as e:
        print("GET ORDERS ERROR:", e)
        return jsonify({"error": "Internal server error"}), 500
