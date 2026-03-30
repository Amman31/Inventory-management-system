"""Regression tests: lock in fixes for fragile behavior."""

from utils.sql_helpers import employee_search_sql


def test_employee_search_uses_bound_parameter_not_concat():
    sql, params = employee_search_sql("Name", "O'Brien")
    assert "?" in sql
    assert "O'Brien" in params[0]
    assert "'" not in sql.replace("?", "")

