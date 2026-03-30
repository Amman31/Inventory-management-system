"""Integration: database operations across multiple statements (employee lifecycle)."""

from config.database import initialize_database, get_connection


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

    cur.execute(
        "UPDATE employee SET salary=? WHERE eid=?",
        ("200", 1),
    )
    con.commit()
    cur.execute("SELECT salary FROM employee WHERE eid=?", (1,))
    assert cur.fetchone()[0] == "200"

    cur.execute("DELETE FROM employee WHERE eid=?", (1,))
    con.commit()
    cur.execute("SELECT COUNT(*) FROM employee WHERE eid=?", (1,))
    assert cur.fetchone()[0] == 0
    con.close()


def test_category_and_product_referential_style_flow(isolated_db):
    """Scenario: add category and supplier rows, then a product row (integration-style)."""
    initialize_database()
    con = get_connection()
    cur = con.cursor()
    cur.execute("INSERT INTO category(name) VALUES (?)", ("Phones",))
    cur.execute(
        "INSERT INTO supplier(invoice,name,contact,desc) VALUES (?,?,?,?)",
        (1, "ACME", "123", "vendor"),
    )
    con.commit()

    cur.execute(
        "INSERT INTO product(Category,Supplier,name,price,qty,status) VALUES (?,?,?,?,?,?)",
        ("Phones", "ACME", "Gadget", "10", "5", "Active"),
    )
    con.commit()
    cur.execute("SELECT Category, Supplier, name FROM product WHERE name=?", ("Gadget",))
    row = cur.fetchone()
    con.close()
    assert row == ("Phones", "ACME", "Gadget")
