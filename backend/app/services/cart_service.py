from database.db_config import get_getconnection


def add_to_cart(product_id, quantity):
    if quantity <= 0:
        return

    conn = get_getconnection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO cart (product_id, quantity)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE quantity = quantity + VALUES(quantity)
    """, (product_id, quantity))

    conn.commit()
    conn.close()


def get_cart_items():
    conn = get_getconnection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            p.name,
            p.price,
            c.quantity,
            (p.price * c.quantity) AS total
        FROM cart c
        JOIN products p ON c.product_id = p.id
    """)

    items = cursor.fetchall()
    conn.close()

    return items


def get_cart_count():
    conn = get_getconnection()
    cursor = conn.cursor()

    cursor.execute("SELECT COALESCE(SUM(quantity), 0) FROM cart")
    count = cursor.fetchone()[0]

    conn.close()
    return count


def get_cart_details():
    conn = get_getconnection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            p.name,
            p.price,
            c.quantity,
            (p.price * c.quantity) AS total
        FROM cart c
        JOIN products p ON c.product_id = p.id
    """)

    items = cursor.fetchall()
    total_amount = sum(item["total"] for item in items)

    conn.close()
    return items, total_amount
