from database.db_config import get_getconnection
from datetime import datetime


def place_order():
    conn = get_getconnection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            p.id AS product_id,
            p.name,
            p.price,
            p.stock,
            c.quantity
        FROM cart c
        JOIN products p ON c.product_id = p.id
    """)
    items = cursor.fetchall()

    if not items:
        conn.close()
        return None

    for item in items:
        if item["quantity"] > item["stock"]:
            conn.close()
            raise ValueError(f"Insufficient stock for {item['name']}")

    total_amount = sum(item["price"] * item["quantity"] for item in items)

    cursor.execute("""
        INSERT INTO orders (total_amount, created_at)
        VALUES (%s, %s)
    """, (total_amount, datetime.now()))

    order_id = cursor.lastrowid

    for item in items:
        cursor.execute("""
            INSERT INTO order_items (order_id, product_id, quantity, price)
            VALUES (%s, %s, %s, %s)
        """, (order_id, item["product_id"], item["quantity"], item["price"]))

        cursor.execute("""
            UPDATE products
            SET stock = stock - %s
            WHERE id = %s
        """, (item["quantity"], item["product_id"]))

    cursor.execute("DELETE FROM cart")

    conn.commit()
    conn.close()

    return order_id


def get_orders():
    conn = get_getconnection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, total_amount, created_at
        FROM orders
        ORDER BY created_at DESC
    """)

    orders = cursor.fetchall()
    conn.close()
    return orders
