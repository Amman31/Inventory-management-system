"""Unit tests: schema initialization and DB connectivity."""

import sqlite3

from models.db import initialize_database, get_connection


def test_initialize_database_creates_tables(isolated_db):
    initialize_database()
    con = sqlite3.connect(str(isolated_db))
    cur = con.cursor()
    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    )
    names = {row[0] for row in cur.fetchall()}
    con.close()
    assert "employee" in names
    assert "supplier" in names
    assert "category" in names
    assert "product" in names


def test_get_connection_opens_same_file(isolated_db):
    initialize_database()
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("INSERT INTO category(name) VALUES (?)", ("TestCat",))
        con.commit()
    finally:
        con.close()

    con2 = sqlite3.connect(str(isolated_db))
    cur2 = con2.cursor()
    cur2.execute("SELECT name FROM category WHERE name=?", ("TestCat",))
    row = cur2.fetchone()
    con2.close()
    assert row is not None
    assert row[0] == "TestCat"


def test_initialize_database_idempotent(isolated_db):
    initialize_database()
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
        n = cur.fetchone()[0]
    finally:
        con.close()
    assert n >= 4
