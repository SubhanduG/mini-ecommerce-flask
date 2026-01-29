from database.db_config import get_getconnection
from datetime import datetime
from flask import session


from database.db_config import get_getconnection
from datetime import datetime
from flask import session


def place_order():
    if "user_id" not in session:
        raise ValueError("Login required to place order")

    user_id = session["user_id"]

    conn = get_getconnection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("START TRANSACTION;")

        cursor.execute("""
            SELECT
                p.id AS product_id,
                p.name,
                p.price,
                p.stock,
                c.quantity
            FROM cart c
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id = %s
            FOR UPDATE
        """, (user_id,))
        items = cursor.fetchall()

        if not items:
            return None

        for item in items:
            if item["quantity"] > item["stock"]:
                raise ValueError(f"Insufficient stock for {item['name']}")

        total_amount = sum(item["price"] * item["quantity"] for item in items)

        cursor.execute("""
            INSERT INTO orders (user_id, total_amount, created_at)
            VALUES (%s, %s, %s)
        """, (user_id, total_amount, datetime.now()))
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

        cursor.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))

        conn.commit()
        return order_id

    except Exception as e:
        conn.rollback()
        print("PLACE ORDER FAILED:", e)
        raise

    finally:
        conn.close()


def get_orders():
    if "user_id" not in session:
        return []

    user_id = session["user_id"]

    conn = get_getconnection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, total_amount, created_at
        FROM orders
        WHERE user_id = %s
        ORDER BY created_at DESC
    """, (user_id,))

    orders = cursor.fetchall()
    conn.close()
    return orders
