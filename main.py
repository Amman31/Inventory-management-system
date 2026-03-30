from tkinter import Tk

from models.db import initialize_database
from views.dashboard import IMS

def main():
    initialize_database()

    # Start the GUI
    root = Tk()
    app = IMS(root)
    root.mainloop()

if __name__ == "__main__":
    main()
