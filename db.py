import os
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "focus_worthy.db"

def init_db():
    """Initialize database from schema.sql"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    schema_path = Path(__file__).parent / "schema.sql"
    with open(schema_path, 'r') as f:
        cursor.executescript(f.read())
    
    conn.commit()
    conn.close()
    print(f"✓ Database initialized at {DB_PATH}")

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

if __name__ == "__main__":
    init_db()
