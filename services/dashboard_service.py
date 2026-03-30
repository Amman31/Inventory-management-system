import os

from config import BILL_DIR
from models.db import get_connection

__all__ = ["fetch_dashboard_counts"]


def fetch_dashboard_counts():
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("select * from product")
        n_product = len(cur.fetchall())
        cur.execute("select * from category")
        n_category = len(cur.fetchall())
        cur.execute("select * from employee")
        n_employee = len(cur.fetchall())
        cur.execute("select * from supplier")
        n_supplier = len(cur.fetchall())
        bill = 0
        if os.path.isdir(BILL_DIR):
            bill = len([f for f in os.listdir(BILL_DIR) if f.endswith(".txt")])
        return {
            "product": n_product,
            "category": n_category,
            "employee": n_employee,
            "supplier": n_supplier,
            "sales_bills": bill,
        }
    finally:
        con.close()
