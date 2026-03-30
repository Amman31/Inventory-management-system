import pytest

# Isolated database
@pytest.fixture
def isolated_db(tmp_path, monkeypatch):
    # Point the app at a fresh SQLite file under tmp_path
    db_dir = tmp_path / "database"
    db_dir.mkdir()
    db_path = db_dir / "ims.db"
    monkeypatch.setattr("config.DATABASE_PATH", str(db_path))
    monkeypatch.setattr("config.DATABASE_DIR", str(db_dir))
    return db_path

# Isolated bill directory
@pytest.fixture
def isolated_bill_dir(tmp_path, monkeypatch):
    bill = tmp_path / "bill"
    bill.mkdir()
    monkeypatch.setattr("config.BILL_DIR", str(bill))
    return bill
