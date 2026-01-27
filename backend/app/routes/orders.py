from flask import Blueprint, jsonify
from backend.app.services.order_service import place_order, get_orders

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")


@orders_bp.route("/confirm", methods=["POST"])
def confirm_order():
    try:
        order_id = place_order()
        if order_id is None:
            return jsonify({"error": "Cart is empty"}), 400

        return jsonify({
            "message": "Order placed successfully",
            "order_id": order_id
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@orders_bp.route("", methods=["GET"])
def order_history():
    return jsonify(get_orders()), 200
