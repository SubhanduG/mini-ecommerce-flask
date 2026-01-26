from database.db_config import get_getconnection
from collections import OrderedDict


def get_all_products():
    conn = get_getconnection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, price, stock, created_at FROM products")
    products = cursor.fetchall()
    conn.close()
    return [OrderedDict({
        "id": p["id"],
        "name": p["name"],
        "price": p["price"],
        "stock": p["stock"],
        "created_at": p["created_at"]
    }) for p in products]
