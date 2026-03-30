import sqlite3

import config
from models.models import CREATE_STATEMENTS


def get_connection():
    return sqlite3.connect(config.DATABASE_PATH)


def initialize_database():
    con = sqlite3.connect(config.DATABASE_PATH)
    cur = con.cursor()
    for stmt in CREATE_STATEMENTS:
        cur.execute(stmt)
        con.commit()
    con.close()
