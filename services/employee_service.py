from models.db import get_connection
from utils.sql_helpers import employee_search_sql

# All employee service functions
__all__ = [
    "employee_search_sql",
    "fetch_all_employees",
    "add_employee",
    "update_employee",
    "employee_exists",
    "delete_employee_row",
    "search_employees",
]

# Fetch all employees
def fetch_all_employees():
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("select * from employee")
        return cur.fetchall()
    finally:
        con.close()


# Add employee
def add_employee(
    eid,
    name,
    email,
    gender,
    contact,
    dob,
    doj,
    password,
    utype,
    address,
    salary,
):
    if not eid:
        return False, "Employee ID must be required"
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("Select * from employee where eid=?", (eid,))
        if cur.fetchone() is not None:
            return False, "This Employee ID is already assigned"
        cur.execute(
            "insert into employee(eid,name,email,gender,contact,dob,doj,pass,utype,address,salary) values(?,?,?,?,?,?,?,?,?,?,?)",
            (
                eid,
                name,
                email,
                gender,
                contact,
                dob,
                doj,
                password,
                utype,
                address,
                salary,
            ),
        )
        con.commit()
        return True, "Employee Added Successfully"
    except Exception as ex:
        return False, f"Error due to : {str(ex)}"
    finally:
        con.close()


# Update employee
def update_employee(
    eid,
    name,
    email,
    gender,
    contact,
    dob,
    doj,
    password,
    utype,
    address,
    salary,
):
    if not eid:
        return False, "Employee ID must be required"
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("Select * from employee where eid=?", (eid,))
        if cur.fetchone() is None:
            return False, "Invalid Employee ID"
        cur.execute(
            "update employee set name=?,email=?,gender=?,contact=?,dob=?,doj=?,pass=?,utype=?,address=?,salary=? where eid=?",
            (
                name,
                email,
                gender,
                contact,
                dob,
                doj,
                password,
                utype,
                address,
                salary,
                eid,
            ),
        )
        con.commit()
        return True, "Employee Updated Successfully"
    except Exception as ex:
        return False, f"Error due to : {str(ex)}"
    finally:
        con.close()


# Check if employee exists
def employee_exists(eid):
    if not eid:
        return False
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("Select * from employee where eid=?", (eid,))
        return cur.fetchone() is not None
    finally:
        con.close()


# Delete employee row
def delete_employee_row(eid):
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("delete from employee where eid=?", (eid,))
        con.commit()
        return True, "Employee Deleted Successfully"
    except Exception as ex:
        return False, f"Error due to : {str(ex)}"
    finally:
        con.close()


# Search employees
def search_employees(search_by, search_term):
    if search_by == "Select":
        return None, "Select Search By option"
    if not search_term:
        return None, "Search input should be required"
    con = get_connection()
    try:
        sql, params = employee_search_sql(search_by, search_term)
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
