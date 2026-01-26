from flask import Blueprint, jsonify
from backend.app.services.product_service import get_all_products

product_bp = Blueprint("products", __name__, url_prefix="/products")


@product_bp.route("", methods=["GET"])
def list_products():
    product = get_all_products()
    return jsonify(product), 200
