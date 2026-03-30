import sqlite3

from models.db import initialize_database


def test_initialize_database_creates_tables(isolated_db):
    initialize_database()
    con = sqlite3.connect(str(isolated_db))
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    names = {row[0] for row in cur.fetchall()}
    con.close()
    assert {"employee", "supplier", "category", "product"}.issubset(names)

