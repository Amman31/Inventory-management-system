from tkinter import Tk

from models.db import initialize_database
from views.dashboard import IMS


def main():
    # Step 1: Initialize DB automatically
    initialize_database()

    # Step 2: Start GUI
    root = Tk()
    app = IMS(root)
    root.mainloop()


if __name__ == "__main__":
    main()
