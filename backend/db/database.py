# database.py — SQLite setup using Python's built-in sqlite3
# Handles product cache, search history, and user preferences
import sqlite3
import json
from datetime import datetime

DB_PATH = "shopping_assistant.db"

def get_connection():
    """Returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # rows behave like dicts
    return conn

def init_db():
    """
    Creates all tables on first run.
    Call this once at startup from main.py.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Stores fetched product results to avoid redundant API calls
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            results TEXT NOT NULL,       -- JSON string of product list
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)

    # Logs every user query for analytics / context
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            timestamp TEXT DEFAULT (datetime('now'))
        )
    """)

    # Optional: stores budget and category preferences per session
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            budget_max REAL,
            preferred_category TEXT,
            updated_at TEXT DEFAULT (datetime('now'))
        )
    """)

    conn.commit()
    conn.close()

def cache_products(query: str, products: list):
    """Save product results for a query to avoid re-fetching."""
    conn = get_connection()
    conn.execute(
        "INSERT INTO product_cache (query, results) VALUES (?, ?)",
        (query, json.dumps(products))
    )
    conn.commit()
    conn.close()

def get_cached_products(query: str):
    """
    Returns cached products if found, else None.
    Simple exact-match cache — can be improved with fuzzy match later.
    """
    conn = get_connection()
    row = conn.execute(
        "SELECT results FROM product_cache WHERE query = ? ORDER BY created_at DESC LIMIT 1",
        (query,)
    ).fetchone()
    conn.close()
    return json.loads(row["results"]) if row else None

def log_search(query: str):
    """Log every user query to search history."""
    conn = get_connection()
    conn.execute("INSERT INTO search_history (query) VALUES (?)", (query,))
    conn.commit()
    conn.close()