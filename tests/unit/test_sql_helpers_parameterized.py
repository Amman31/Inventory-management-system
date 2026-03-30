from utils.sql_helpers import employee_search_sql, product_search_sql


def test_search_sql_parameterized_employee_and_product():
    sql, params = employee_search_sql("Email", "a@b.com")
    assert "email like ?" in sql.lower()
    assert params == ("%a@b.com%",)

    sql2, params2 = product_search_sql("Name", "phone")
    assert "name like ?" in sql2.lower()
    assert params2 == ("%phone%",)

