"""Unit tests: safe SQL helper builders."""

import pytest

from utils.sql_helpers import (
    employee_search_sql,
    product_search_sql,
    EMPLOYEE_SEARCH_COLUMNS,
    PRODUCT_SEARCH_COLUMNS,
)


def test_employee_search_sql_parameterized():
    sql, params = employee_search_sql("Email", "a@b.com")
    assert "email like ?" in sql.lower()
    assert params == ("%a@b.com%",)


def test_product_search_sql_parameterized():
    sql, params = product_search_sql("Name", "phone")
    assert "name like ?" in sql.lower()
    assert params == ("%phone%",)


def test_invalid_search_field_raises():
    with pytest.raises(ValueError):
        employee_search_sql("Drop Table", "x")
    with pytest.raises(ValueError):
        product_search_sql("; DELETE FROM product; --", "x")


def test_maps_cover_ui_labels():
    assert set(EMPLOYEE_SEARCH_COLUMNS) == {"Email", "Name", "Contact"}
    assert set(PRODUCT_SEARCH_COLUMNS) == {"Category", "Supplier", "Name"}
