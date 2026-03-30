from __future__ import annotations

import os

from tkinter import Tk

from config import DATABASE_PATH
from models.db import initialize_database
from utils.admin_initialization import ensure_admin_exists
from views.dashboard import IMS
from views.login_view import LoginView


def _clear_root(root: Tk) -> None:
    # Remove prior widgets when switching between Login and Dashboard.
    for w in root.winfo_children():
        w.destroy()


def main():
    # Ensure tables exist.
    initialize_database()

    # First-run bootstrap: create default admin.
    ensure_admin_exists()

    root = Tk()

    def show_login():
        _clear_root(root)
        LoginView(root, on_login=show_dashboard)

    def show_dashboard(role: str):
        _clear_root(root)
        IMS(root, user_role=role, on_logout=show_login)

    show_login()
    root.mainloop()


if __name__ == "__main__":
    main()
