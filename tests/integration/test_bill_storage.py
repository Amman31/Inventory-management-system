"""Integration: bill text files are written under configured BILL_DIR."""

import os

from config.settings import BILL_DIR


def test_bill_dir_exists_after_settings_import():
    assert os.path.isdir(BILL_DIR)


def test_write_and_read_bill_roundtrip(isolated_bill_dir):
    path = os.path.join(str(isolated_bill_dir), "999.txt")
    content = "line1\nline2\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    with open(path, "r", encoding="utf-8") as f:
        assert f.read() == content
