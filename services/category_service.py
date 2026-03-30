from models.db import get_connection

__all__ = [
    "fetch_all_categories",
    "add_category",
    "category_exists",
    "delete_category_row",
]


def fetch_all_categories():
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("select * from category")
        return cur.fetchall()
    finally:
        con.close()


def add_category(name):
    if not name:
        return False, "Category Name must be required"
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("Select * from category where name=?", (name,))
        if cur.fetchone() is not None:
            return False, "Category already present"
        cur.execute("insert into category(name) values(?)", (name,))
        con.commit()
        return True, "Category Added Successfully"
    except Exception as ex:
        return False, f"Error due to : {str(ex)}"
    finally:
        con.close()


def category_exists(cid):
    if not cid:
        return False
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("Select * from category where cid=?", (cid,))
        return cur.fetchone() is not None
    finally:
        con.close()


def delete_category_row(cid):
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("delete from category where cid=?", (cid,))
        con.commit()
        return True, "Category Deleted Successfully"
    except Exception as ex:
        return False, f"Error due to : {str(ex)}"
    finally:
        con.close()
