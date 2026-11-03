import pytest
from app.db.database import DatabaseManager

def test_database_initialization_and_row_counts(memory_db: DatabaseManager):
    """Verify that tables are created and seeded with exact expected counts."""
    with memory_db.get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM categories;")
        assert cursor.fetchone()[0] == 9

        cursor.execute("SELECT COUNT(*) FROM customers;")
        assert cursor.fetchone()[0] == 50

        cursor.execute("SELECT COUNT(*) FROM products;")
        assert cursor.fetchone()[0] == 65

        cursor.execute("SELECT COUNT(*) FROM orders;")
        assert cursor.fetchone()[0] == 20

        cursor.execute("SELECT COUNT(*) FROM order_items;")
        assert cursor.fetchone()[0] == 22

        cursor.execute("SELECT COUNT(*) FROM promotions;")
        assert cursor.fetchone()[0] == 25

def test_foreign_key_join_integrity(memory_db: DatabaseManager):
    """Verify foreign key relations between products, categories, and promotions."""
    with memory_db.get_connection() as conn:
        cursor = conn.cursor()
        
        # Check products joined with category
        cursor.execute("""
            SELECT p.product_id, p.name, c.name as category_name, p.price_brl
            FROM products p
            JOIN categories c ON p.category_id = c.category_id
            WHERE p.name LIKE '%Yamaha C40%';
        """)
        row = cursor.fetchone()
        assert row is not None
        assert "Yamaha C40" in row["name"]
        assert row["category_name"] == "Violões"
        assert row["price_brl"] > 0

def test_order_and_items_join(memory_db: DatabaseManager):
    """Verify orders joined with customer and items."""
    with memory_db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT o.order_id, c.name as customer_name, o.status, o.tracking_code,
                   p.name as product_name, oi.quantity
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            JOIN order_items oi ON o.order_id = oi.order_id
            JOIN products p ON oi.product_id = p.product_id
            WHERE o.order_id = 1;
        """)
        rows = cursor.fetchall()
        assert len(rows) > 0
        assert rows[0]["customer_name"] != ""
        assert rows[0]["status"] != ""

