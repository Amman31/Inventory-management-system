import os

from config import BILL_DIR

__all__ = [
    "list_bill_display_entries",
    "read_bill_lines_by_filename",
    "read_bill_lines_by_invoice",
]


def list_bill_display_entries():
    """Returns (filenames_for_listbox, invoice_ids_without_extension)."""
    filenames = []
    invoice_ids = []
    if not os.path.isdir(BILL_DIR):
        return filenames, invoice_ids
    for i in os.listdir(BILL_DIR):
        if i.endswith(".txt"):
            filenames.append(i)
            invoice_ids.append(i.split(".")[0])
    return filenames, invoice_ids


def read_bill_lines_by_filename(filename):
    file_path = os.path.join(BILL_DIR, filename)
    lines = []
    with open(file_path, "r", encoding="utf-8", errors="replace") as fp:
        for line in fp:
            lines.append(line)
    return lines


def read_bill_lines_by_invoice(invoice_id):
    file_path = os.path.join(BILL_DIR, f"{invoice_id}.txt")
    lines = []
    with open(file_path, "r", encoding="utf-8", errors="replace") as fp:
        for line in fp:
            lines.append(line)
    return lines


def invoice_exists(invoice_id, known_invoice_ids):
    return invoice_id in known_invoice_ids
