from __future__ import annotations

from models.db import get_connection

# Admin user details
ADMIN_USER = {
    "name": "Administrator",
    "email": "admin@example.com",
    "gender": "Male",
    "contact": "0000000000",
    "dob": "2000-01-01",
    "doj": "2024-01-01",
    "password": "admin123",
    "utype": "admin",
    "address": "System Generated",
    "salary": "0",
}

# Ensure admin exists in the database
def ensure_admin_exists() -> bool:
    # Get connection to the database
    con = get_connection()
    try:
        cur = con.cursor()

        # Check if admin exists by unique email
        cur.execute("select 1 from employee where email=? limit 1", (ADMIN_USER["email"],))
        if cur.fetchone() is not None:
            return True

        # Insert admin into the database
        cur.execute(
            "insert into employee(name,email,gender,contact,dob,doj,pass,utype,address,salary) values(?,?,?,?,?,?,?,?,?,?)",
            (
                ADMIN_USER["name"],
                ADMIN_USER["email"],
                ADMIN_USER["gender"],
                ADMIN_USER["contact"],
                ADMIN_USER["dob"],
                ADMIN_USER["doj"],
                ADMIN_USER["password"],
                ADMIN_USER["utype"],
                ADMIN_USER["address"],
                ADMIN_USER["salary"],
            ),
        )
        con.commit()
        return True
    except Exception:
        return False
    finally:
        con.close()

