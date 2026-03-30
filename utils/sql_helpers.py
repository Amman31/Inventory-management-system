EMPLOYEE_SEARCH_COLUMNS = {"Email": "email", "Name": "name", "Contact": "contact"}

PRODUCT_SEARCH_COLUMNS = {"Category": "Category", "Supplier": "Supplier", "Name": "name"}


def employee_search_sql(search_by_label, search_term):
    col = EMPLOYEE_SEARCH_COLUMNS.get(search_by_label)
    if col is None:
        raise ValueError("Invalid employee search field")
    return ("SELECT * FROM employee WHERE " + col + " LIKE ?", (f"%{search_term}%",))


def product_search_sql(search_by_label, search_term):
    col = PRODUCT_SEARCH_COLUMNS.get(search_by_label)
    if col is None:
        raise ValueError("Invalid product search field")
    return ("SELECT * FROM product WHERE " + col + " LIKE ?", (f"%{search_term}%",))
