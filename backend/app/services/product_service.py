from database.db_config import get_getconnection


def get_all_products():
    conn = get_getconnection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            name,
            price,
            stock,
            created_at
        FROM products
        ORDER BY created_at DESC
    """)

    products = cursor.fetchall()
    conn.close()

    return products
