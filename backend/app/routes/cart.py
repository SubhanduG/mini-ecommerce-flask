from flask import Blueprint, request, jsonify
from backend.app.services.cart_service import (
    add_to_cart,
    get_cart_items,
    get_cart_count,
    get_cart_details
)

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")


@cart_bp.route("", methods=["POST"])
def add_cart_item():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid request"}), 400

    add_to_cart(data.get("product_id"), data.get("quantity", 1))
    return jsonify({"message": "Added to cart"}), 201


@cart_bp.route("", methods=["GET"])
def view_cart():
    return jsonify(get_cart_items()), 200


@cart_bp.route("/count", methods=["GET"])
def cart_count():
    return jsonify({"count": get_cart_count()}), 200


@cart_bp.route("/details", methods=["GET"])
def cart_details():
    items, total = get_cart_details()
    return jsonify({
        "items": items,
        "total": total
    }), 200
