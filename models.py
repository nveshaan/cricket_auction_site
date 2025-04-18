import sqlite3

def get_db():
    conn = sqlite3.connect("auction.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with open('schema.sql') as f:
        db = get_db()
        db.executescript(f.read())
        db.commit()
