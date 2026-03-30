import sqlite3

from models.db import get_connection, initialize_database
from utils.admin_initialization import ensure_admin_exists


def test_admin_bootstrap_creates_default_admin(isolated_db):
    initialize_database()
    ok = ensure_admin_exists()
    assert ok is True

    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute(
            "select name,email,utype from employee where email=? limit 1",
            ("admin@example.com",),
        )
        row = cur.fetchone()
    finally:
        con.close()

    assert row is not None
    assert row[0] == "Administrator"
    assert row[1] == "admin@example.com"
    assert row[2] == "admin"

