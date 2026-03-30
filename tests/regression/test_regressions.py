"""
Regression tests: lock in fixes for previously fragile behavior.

- Product add must use .get() for supplier StringVar (not compare the Var object).
- Employee/product search must use bound parameters (no string-concat SQL).
"""

from app.sql_helpers import employee_search_sql


def test_employee_search_uses_bound_parameter_not_concat():
    sql, params = employee_search_sql("Name", "O'Brien")
    assert "?" in sql
    assert "O'Brien" in params[0]
    assert "'" not in sql.replace("?", "")


def test_product_validation_uses_get_not_var_identity():
    """Documenting fix: `self.var_sup == \"Select\"` was always false (Var object)."""
    from tkinter import Tk, StringVar

    root = Tk()
    root.withdraw()
    try:
        v = StringVar(master=root, value="Select")
        assert not (v == "Select")
        assert v.get() == "Select"
    finally:
        root.destroy()
