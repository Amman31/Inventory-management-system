from models.db import get_connection
from utils.sql_helpers import product_search_sql

__all__ = [
    "product_search_sql",
    "fetch_category_and_supplier_names",
    "fetch_all_products",
    "add_product",
    "update_product",
    "product_exists",
    "delete_product_row",
    "search_products",
]

# Fetch category and supplier names
def fetch_category_and_supplier_names():
    cat_list = ["Empty"]
    sup_list = ["Empty"]
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("select name from category")
        cat = cur.fetchall()
        if len(cat) > 0:
            cat_list = ["Select"]
            for i in cat:
                cat_list.append(i[0])
        cur.execute("select name from supplier")
        sup = cur.fetchall()
        if len(sup) > 0:
            sup_list = ["Select"]
            for i in sup:
                sup_list.append(i[0])
        return cat_list, sup_list
    except Exception as ex:
        raise RuntimeError(f"Error due to : {str(ex)}") from ex
    finally:
        con.close()

# Fetch all products
def fetch_all_products():
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("select * from product")
        return cur.fetchall()
    finally:
        con.close()

# Add product
def add_product(category, supplier, name, price, qty, status):
    if category in ("Select", "Empty") or supplier in ("Select", "Empty"):
        return False, "All fields are required"
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("Select * from product where name=?", (name,))
        if cur.fetchone() is not None:
            return False, "Product already present"
        cur.execute(
            "insert into product(Category,Supplier,name,price,qty,status) values(?,?,?,?,?,?)",
            (category, supplier, name, price, qty, status),
        )
        con.commit()
        return True, "Product Added Successfully"
    except Exception as ex:
        return False, f"Error due to : {str(ex)}"
    finally:
        con.close()

# Update product
def update_product(pid, category, supplier, name, price, qty, status):
    if not pid:
        return False, "Please select product from list"
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("Select * from product where pid=?", (pid,))
        if cur.fetchone() is None:
            return False, "Invalid Product"
        cur.execute(
            "update product set Category=?,Supplier=?,name=?,price=?,qty=?,status=? where pid=?",
            (category, supplier, name, price, qty, status, pid),
        )
        con.commit()
        return True, "Product Updated Successfully"
    except Exception as ex:
        return False, f"Error due to : {str(ex)}"
    finally:
        con.close()

# Check if product exists
def product_exists(pid):
    if not pid:
        return False
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("Select * from product where pid=?", (pid,))
        return cur.fetchone() is not None
    finally:
        con.close()

# Delete product row
def delete_product_row(pid):
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("delete from product where pid=?", (pid,))
        con.commit()
        return True, "Product Deleted Successfully"
    except Exception as ex:
        return False, f"Error due to : {str(ex)}"
    finally:
        con.close()

# Search products
def search_products(search_by, search_term):
    if search_by == "Select":
        return None, "Select Search By option"
    if not search_term:
        return None, "Search input should be required"
    con = get_connection()
    try:
        sql, params = product_search_sql(search_by, search_term)
        cur = con.cursor()
        cur.execute(sql, params)
        rows = cur.fetchall()
        if not rows:
            return None, "No record found!!!"
        return rows, None
    except ValueError:
        return None, "Select Search By option"
    except Exception as ex:
        return None, f"Error due to : {str(ex)}"
    finally:
        con.close()
