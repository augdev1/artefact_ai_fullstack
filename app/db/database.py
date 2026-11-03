import os
import csv
import glob
import sqlite3
import logging
from pathlib import Path
from typing import Generator, Any, List, Dict, Optional
from contextlib import contextmanager

from app.config import settings
from app.db.etl import DataPipeline

logger = logging.getLogger(__name__)

CREATE_TABLES_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    city TEXT
);

CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    price_brl REAL NOT NULL,
    name TEXT NOT NULL,
    category_id INTEGER REFERENCES categories(category_id),
    description TEXT,
    stock_quantity INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'active',
    specs TEXT,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    order_date TEXT NOT NULL,
    status TEXT NOT NULL,
    total_brl REAL NOT NULL,
    payment_method TEXT,
    tracking_code TEXT,
    estimated_delivery TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS order_items (
    order_id INTEGER NOT NULL REFERENCES orders(order_id),
    quantity INTEGER NOT NULL DEFAULT 1,
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    PRIMARY KEY (order_id, product_id)
);

CREATE TABLE IF NOT EXISTS promotions (
    promotion_id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    discount_percent REAL NOT NULL,
    description TEXT,
    is_active INTEGER NOT NULL DEFAULT 0
);

-- Persistent Conversation History per User Session
CREATE TABLE IF NOT EXISTS conversation_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    tools_called TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for lightning-fast retrieval
CREATE INDEX IF NOT EXISTS idx_products_name ON products(name COLLATE NOCASE);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_products_price ON products(price_brl);
CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_tracking ON orders(tracking_code);
CREATE INDEX IF NOT EXISTS idx_promotions_product ON promotions(product_id);
CREATE INDEX IF NOT EXISTS idx_promotions_active ON promotions(is_active);
CREATE INDEX IF NOT EXISTS idx_conv_session ON conversation_history(session_id);
"""

class DatabaseManager:
    def __init__(self, db_path: Path | str | None = None):
        if db_path is None:
            self.db_path = str(settings.DATABASE_PATH)
        else:
            self.db_path = str(db_path)
        self._shared_conn: sqlite3.Connection | None = None

    @contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        if self.db_path == ":memory:":
            if self._shared_conn is None:
                self._shared_conn = sqlite3.connect(":memory:", check_same_thread=False)
                self._shared_conn.row_factory = sqlite3.Row
                self._shared_conn.execute("PRAGMA foreign_keys = ON;")
            try:
                yield self._shared_conn
                self._shared_conn.commit()
            except Exception:
                self._shared_conn.rollback()
                raise
        else:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON;")
            try:
                yield conn
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                conn.close()

    def close(self) -> None:
        if self._shared_conn is not None:
            self._shared_conn.close()
            self._shared_conn = None

    def init_database(self, force_reload: bool = False) -> None:
        """Create tables and seed data from CSV files through ETL pipeline."""
        if self.db_path != ":memory:":
            os.makedirs(os.path.dirname(os.path.abspath(self.db_path)), exist_ok=True)

        with self.get_connection() as conn:
            conn.executescript(CREATE_TABLES_SQL)

            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM products;")
            count = cursor.fetchone()[0]

            if count > 0 and not force_reload:
                logger.info("Database already initialized with %d products.", count)
                return

            if force_reload:
                cursor.execute("DELETE FROM order_items;")
                cursor.execute("DELETE FROM promotions;")
                cursor.execute("DELETE FROM orders;")
                cursor.execute("DELETE FROM products;")
                cursor.execute("DELETE FROM customers;")
                cursor.execute("DELETE FROM categories;")

            self._seed_from_csvs(conn)

    def _find_csv(self, pattern: str) -> Optional[str]:
        matches = glob.glob(str(settings.DATA_DIR / pattern))
        return matches[0] if matches else None

    def _seed_from_csvs(self, conn: sqlite3.Connection) -> None:
        """Parse original challenge CSVs using DataPipeline ETL and seed SQLite."""
        # 1. Categories
        cat_file = self._find_csv("*categories*.csv")
        if cat_file:
            cats = DataPipeline.process_categories(cat_file)
            rows = [(c["category_id"], c["name"], c["description"]) for c in cats]
            conn.executemany(
                "INSERT OR REPLACE INTO categories (category_id, name, description) VALUES (?, ?, ?);",
                rows
            )

        # 2. Customers
        cust_file = self._find_csv("*customers*.csv")
        if cust_file:
            custs = DataPipeline.process_customers(cust_file)
            rows = [(c["customer_id"], c["name"], c["phone"], c["email"], c["city"]) for c in custs]
            conn.executemany(
                "INSERT OR REPLACE INTO customers (customer_id, name, phone, email, city) VALUES (?, ?, ?, ?, ?);",
                rows
            )

        # 3. Products
        prod_file = self._find_csv("*products*.csv")
        if prod_file:
            prods = DataPipeline.process_products(prod_file)
            rows = [
                (
                    p["product_id"], p["price_brl"], p["name"], p["category_id"],
                    p["description"], p["stock_quantity"], p["status"], p["specs"], p["created_at"]
                )
                for p in prods
            ]
            conn.executemany(
                """INSERT OR REPLACE INTO products 
                (product_id, price_brl, name, category_id, description, stock_quantity, status, specs, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);""",
                rows
            )

        # 4. Orders
        ord_file = self._find_csv("*orders*.csv")
        if ord_file:
            ords = DataPipeline.process_orders(ord_file)
            rows = [
                (
                    o["order_id"], o["customer_id"], o["order_date"], o["status"],
                    o["total_brl"], o["payment_method"], o["tracking_code"], o["estimated_delivery"], o["notes"]
                )
                for o in ords
            ]
            conn.executemany(
                """INSERT OR REPLACE INTO orders 
                (order_id, customer_id, order_date, status, total_brl, payment_method, tracking_code, estimated_delivery, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);""",
                rows
            )

        # 5. Order Items
        items_file = self._find_csv("*order_items*.csv")
        if items_file:
            items = DataPipeline.process_order_items(items_file)
            rows = [(it["order_id"], it["quantity"], it["product_id"]) for it in items]
            conn.executemany(
                "INSERT OR REPLACE INTO order_items (order_id, quantity, product_id) VALUES (?, ?, ?);",
                rows
            )

        # 6. Promotions
        promo_file = self._find_csv("*promotions*.csv")
        if promo_file:
            promos = DataPipeline.process_promotions(promo_file)
            rows = [
                (p["promotion_id"], p["product_id"], p["discount_percent"], p["description"], p["is_active"])
                for p in promos
            ]
            conn.executemany(
                """INSERT OR REPLACE INTO promotions 
                (promotion_id, product_id, discount_percent, description, is_active)
                VALUES (?, ?, ?, ?, ?);""",
                rows
            )

        logger.info("Successfully seeded database with cleaned, normalized ETL data.")

    # Persistent Conversation History Operations
    def save_conversation_message(
        self,
        session_id: str,
        role: str,
        content: str,
        tools_called: Optional[List[str]] = None
    ) -> None:
        """Persist a message into the conversation_history table."""
        tools_str = ",".join(tools_called) if tools_called else None
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO conversation_history (session_id, role, content, tools_called)
                   VALUES (?, ?, ?, ?);""",
                (session_id, role, content, tools_str)
            )

    def get_conversation_history(self, session_id: str, limit: int = 30) -> List[Dict[str, Any]]:
        """Retrieve stored conversation messages for a session."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id, session_id, role, content, tools_called, created_at
                   FROM conversation_history
                   WHERE session_id = ?
                   ORDER BY id ASC
                   LIMIT ?;""",
                (session_id, limit)
            )
            rows = cursor.fetchall()
            return [
                {
                    "id": r["id"],
                    "session_id": r["session_id"],
                    "role": r["role"],
                    "content": r["content"],
                    "tools_called": r["tools_called"].split(",") if r["tools_called"] else [],
                    "created_at": r["created_at"]
                }
                for r in rows
            ]

    def clear_conversation_history(self, session_id: str) -> None:
        """Clear conversation history for a session."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM conversation_history WHERE session_id = ?;", (session_id,))

    def list_persisted_sessions(self) -> List[str]:
        """List distinct active sessions in history."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT session_id FROM conversation_history ORDER BY id DESC;")
            return [r[0] for r in cursor.fetchall()]

db_manager = DatabaseManager()
