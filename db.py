import sqlite3
from datetime import datetime

DB_FILE = "prices.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            url TEXT,
            price TEXT,
            checked_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_price(product_name: str, url: str, price: str):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "INSERT INTO price_history (product_name, url, price, checked_at) VALUES (?, ?, ?, ?)",
        (product_name, url, price, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def get_last_price(url: str):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "SELECT price, checked_at FROM price_history WHERE url = ? ORDER BY id DESC LIMIT 1",
        (url,)
    )
    row = c.fetchone()
    conn.close()
    return row