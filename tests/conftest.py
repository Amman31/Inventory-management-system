import pytest


@pytest.fixture
def isolated_db(tmp_path, monkeypatch):
    """Point the app at a fresh SQLite file under tmp_path."""
    db_dir = tmp_path / "database"
    db_dir.mkdir()
    db_path = db_dir / "ims.db"
    monkeypatch.setattr("config.settings.DATABASE_PATH", str(db_path))
    monkeypatch.setattr("config.settings.DATABASE_DIR", str(db_dir))
    return db_path


@pytest.fixture
def isolated_bill_dir(tmp_path, monkeypatch):
    bill = tmp_path / "bill"
    bill.mkdir()
    monkeypatch.setattr("config.settings.BILL_DIR", str(bill))
    return bill
