from flask import session
from database.db_config import get_getconnection


def is_logged_in():
    return "user_id" in session


def add_to_cart(user_id, product_id, quantity):
    if quantity <= 0:
        return

    conn = get_getconnection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO cart (user_id, product_id, quantity)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE quantity = quantity + VALUES(quantity)
    """, (user_id, product_id, quantity))

    conn.commit()
    conn.close()


def get_cart_items(user_id):
    conn = get_getconnection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            p.id AS product_id,
            p.name,
            p.price,
            c.quantity,
            (p.price * c.quantity) AS total
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = %s
    """, (user_id,))

    items = cursor.fetchall()
    conn.close()
    return items


def get_cart_count(user_id):
    conn = get_getconnection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COALESCE(SUM(quantity),0) FROM cart WHERE user_id = %s", (user_id,))
    count = cursor.fetchone()[0]

    conn.close()
    return count


def get_cart_details(user_id):
    conn = get_getconnection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            p.id AS product_id,
            p.name,
            p.price,
            c.quantity,
            (p.price * c.quantity) AS total
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = %s
    """, (user_id,))

    items = cursor.fetchall()
    total_amount = sum(item["total"] for item in items)

    conn.close()
    return items, total_amount


def clear_cart(user_id):
    conn = get_getconnection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))
    conn.commit()
    conn.close()
