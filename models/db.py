import sqlite3

import config
from models.models import CREATE_TABLES

# Get connection
def get_connection():
    return sqlite3.connect(config.DATABASE_PATH)

# Initialize database
def initialize_database():
    con = sqlite3.connect(config.DATABASE_PATH)
    cur = con.cursor()
    for stmt in CREATE_TABLES:
        cur.execute(stmt)
        con.commit()
    con.close()
