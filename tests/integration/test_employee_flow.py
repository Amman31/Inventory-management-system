"""Integration: employee lifecycle operations (insert/update/delete)."""

from models.db import get_connection, initialize_database


def test_employee_insert_update_delete_flow(isolated_db):
    initialize_database()
    con = get_connection()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO employee(eid,name,email,gender,contact,dob,doj,pass,utype,address,salary) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        (
            1,
            "Ada",
            "ada@example.com",
            "Other",
            "555",
            "1/1/2000",
            "1/1/2020",
            "x",
            "Admin",
            "Addr",
            "100",
        ),
    )
    con.commit()

    cur.execute("SELECT name FROM employee WHERE eid=?", (1,))
    assert cur.fetchone()[0] == "Ada"

    cur.execute("UPDATE employee SET salary=? WHERE eid=?", ("200", 1))
    con.commit()
    cur.execute("SELECT salary FROM employee WHERE eid=?", (1,))
    assert cur.fetchone()[0] == "200"

    cur.execute("DELETE FROM employee WHERE eid=?", (1,))
    con.commit()
    cur.execute("SELECT COUNT(*) FROM employee WHERE eid=?", (1,))
    assert cur.fetchone()[0] == 0
    con.close()
