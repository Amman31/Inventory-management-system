from __future__ import annotations

from models.db import get_connection

# Normalize role
def _normalize_role(utype: str | None) -> str:
    if not utype:
        return "employee"
    value = str(utype).strip().lower()
    if value == "admin":
        return "admin"
    return "employee"

# Authenticate user
def authenticate(email: str, password: str) -> tuple[bool, str | None, str]:
    # Validate user credentials
    if not email or not password:
        return False, None, "Email and password are required"
    # Get connection to the database
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute(
            "select utype from employee where email=? and pass=? limit 1",
            (email, password),
        )
        row = cur.fetchone()
        if row is None:
            return False, None, "Invalid email or password"
        role = _normalize_role(row[0])
        return True, role, "Login successful"
    finally:
        con.close()

