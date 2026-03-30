from models.db import get_connection

__all__ = [
    "fetch_all_suppliers",
    "add_supplier",
    "update_supplier",
    "supplier_invoice_exists",
    "delete_supplier_row",
    "get_supplier_by_invoice",
]

# Fetch all suppliers
def fetch_all_suppliers():
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("select * from supplier")
        return cur.fetchall()
    finally:
        con.close()

# Add supplier
def add_supplier(invoice, name, contact, desc):
    if not invoice:
        return False, "Invoice must be required"
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("Select * from supplier where invoice=?", (invoice,))
        if cur.fetchone() is not None:
            return False, "Invoice no. is already assigned"
        cur.execute(
            "insert into supplier(invoice,name,contact,desc) values(?,?,?,?)",
            (invoice, name, contact, desc),
        )
        con.commit()
        return True, "Supplier Added Successfully"
    except Exception as ex:
        return False, f"Error due to : {str(ex)}"
    finally:
        con.close()

# Update supplier
def update_supplier(invoice, name, contact, desc):
    if not invoice:
        return False, "Invoice must be required"
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("Select * from supplier where invoice=?", (invoice,))
        if cur.fetchone() is None:
            return False, "Invalid Invoice No."
        cur.execute(
            "update supplier set name=?,contact=?,desc=? where invoice=?",
            (name, contact, desc, invoice),
        )
        con.commit()
        return True, "Supplier Updated Successfully"
    except Exception as ex:
        return False, f"Error due to : {str(ex)}"
    finally:
        con.close()

# Check if supplier invoice exists
def supplier_invoice_exists(invoice):
    if not invoice:
        return False
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("Select * from supplier where invoice=?", (invoice,))
        return cur.fetchone() is not None
    finally:
        con.close()

# Delete supplier row
def delete_supplier_row(invoice):
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("delete from supplier where invoice=?", (invoice,))
        con.commit()
        return True, "Supplier Deleted Successfully"
    except Exception as ex:
        return False, f"Error due to : {str(ex)}"
    finally:
        con.close()

# Get supplier by invoice
def get_supplier_by_invoice(invoice):
    if not invoice:
        return None, "Invoice No. should be required"
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("select * from supplier where invoice=?", (invoice,))
        row = cur.fetchone()
        if row is None:
            return None, "No record found!!!"
        return row, None
    except Exception as ex:
        return None, f"Error due to : {str(ex)}"
    finally:
        con.close()
