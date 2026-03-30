import os
import time

from config import BILL_DIR
from models.db import get_connection

__all__ = [
    "fetch_active_products_for_table",
    "search_active_products_by_name",
    "validate_cart_add",
    "find_duplicate_cart_index",
    "append_cart_row",
    "update_cart_after_confirm",
    "compute_bill_totals",
    "generate_invoice_number",
    "format_bill_top_text",
    "format_bill_bottom_text",
    "format_bill_middle_lines",
    "commit_cart_to_inventory",
    "save_bill_file",
]


def fetch_active_products_for_table():
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute(
            "select pid,name,price,qty,status from product where status='Active'"
        )
        return cur.fetchall()
    except Exception as ex:
        raise RuntimeError(f"Error due to : {str(ex)}") from ex
    finally:
        con.close()


def search_active_products_by_name(name_pattern):
    if not name_pattern:
        return None, "Search input should be required"
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute(
            "select pid,name,price,qty,status from product where name LIKE ?",
            (f"%{name_pattern}%",),
        )
        rows = cur.fetchall()
        if not rows:
            return None, "No record found!!!"
        return rows, None
    except Exception as ex:
        return None, f"Error due to : {str(ex)}"
    finally:
        con.close()


def validate_cart_add(pid, qty_str, stock_str):
    if not pid:
        return False, "Please select product from the list"
    if not qty_str:
        return False, "Quantity is required"
    if int(qty_str) > int(stock_str):
        return False, "Invalid Quantity"
    return True, None


def find_duplicate_cart_index(cart_list, pid):
    for index_, row in enumerate(cart_list):
        if str(pid) == str(row[0]):
            return index_
    return -1


def append_cart_row(cart_list, cart_row):
    return cart_list + [cart_row]


def update_cart_after_confirm(cart_list, index_, new_qty_str):
    new_list = [list(r) for r in cart_list]
    if new_qty_str == "0":
        new_list.pop(index_)
    else:
        new_list[index_][3] = new_qty_str
    return new_list


def compute_bill_totals(cart_list):
    bill_amnt = 0.0
    for row in cart_list:
        bill_amnt = bill_amnt + (float(row[2]) * int(row[3]))
    discount = (bill_amnt * 5) / 100
    net_pay = bill_amnt - discount
    return bill_amnt, discount, net_pay


def generate_invoice_number():
    return int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y"))


def format_bill_top_text(cname, contact, invoice):
    return f"""
\t\tXYZ-Inventory
\t Phone No. 9899459288 , Delhi-110053
{str("=" * 46)}
 Customer Name: {cname}
 Ph. no. : {contact}
 Bill No. {str(invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("=" * 46)}
 Product Name\t\t\tQTY\tPrice
{str("=" * 46)}
"""


def format_bill_bottom_text(bill_amnt, discount, net_pay):
    return f"""
{str("=" * 46)}
 Bill Amount\t\t\t\tRs.{bill_amnt}
 Discount\t\t\t\tRs.{discount}
 Net Pay\t\t\t\tRs.{net_pay}
{str("=" * 46)}\n
"""


def format_bill_middle_lines(cart_list):
    """Returns list of text segments to append to bill body (inventory commit separate)."""
    segments = []
    for row in cart_list:
        name = row[1]
        qty = row[3]
        price = float(row[2]) * int(row[3])
        segments.append("\n " + name + "\t\t\t" + str(qty) + "\tRs." + str(price))
    return segments


def commit_cart_to_inventory(cart_list):
    con = get_connection()
    try:
        cur = con.cursor()
        for row in cart_list:
            pid = row[0]
            qty_sold = int(row[3])
            stock = int(row[4])
            qty = stock - qty_sold
            if qty_sold == stock:
                status = "Inactive"
            else:
                status = "Active"
            cur.execute(
                "update product set qty=?,status=? where pid=?",
                (qty, status, pid),
            )
            con.commit()
        return True, None
    except Exception as ex:
        return False, str(ex)
    finally:
        con.close()


def save_bill_file(invoice, text_body):
    bill_path = os.path.join(BILL_DIR, f"{str(invoice)}.txt")
    with open(bill_path, "w", encoding="utf-8") as fp:
        fp.write(text_body)
    return bill_path


def validate_generate_bill(cname, contact, cart_list):
    if not cname or not contact:
        return False, "Customer Details are required"
    if len(cart_list) == 0:
        return False, "Please Add product to the Cart!!!"
    return True, None
