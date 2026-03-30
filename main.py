from tkinter import Tk
from app.dashboard import IMS
from config.database import initialize_database

def main():
    # Step 1: Initialize DB automatically
    initialize_database()

    # Step 2: Start GUI
    root = Tk()
    app = IMS(root)
    root.mainloop()

if __name__ == "__main__":
    main()