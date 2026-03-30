import os
import time

from tkinter import Tk, Label, Button, Frame, RIDGE, LEFT, TOP, X, BOTH, BOTTOM, Toplevel
from tkinter import messagebox
from PIL import Image, ImageTk

from app.employee import employeeClass
from app.supplier import supplierClass
from app.category import categoryClass
from app.product import productClass
from app.sales import salesClass
from config.database import get_connection
from config.settings import IMAGE_DIR, BILL_DIR


class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+110+80")
        self.menu = (
            ("Employee", self.employee),
            ("Supplier", self.supplier),
            ("Category", self.category),
            ("Products", self.product),
            ("Sales", self.sales),
        )
        self.root.resizable(False, False)
        self.root.config(bg="white")

        logo_path = os.path.join(IMAGE_DIR, "logo1.png")
        self.icon_title = PhotoImageSafe(self.root, logo_path)
        title = Label(
            self.root,
            text="Inventory Management System",
            image=self.icon_title,
            compound=LEFT,
            font=("times new roman", 40, "bold"),
            bg="#010c48",
            fg="white",
            anchor="w",
            padx=20,
        )
        title.place(x=0, y=0, relwidth=1, height=70)

        Button(self.root, text="Logout", font=("times new roman", 15, "bold"),bg="yellow", cursor="hand2").place(x=1150, y=10, height=50, width=150)

        self.lbl_clock = Label(
            self.root,
            text="Welcome to Inventory Management System\t\t Date: DD:MM:YYYY\t\t Time: HH:MM:SS",
            font=("times new roman", 15),
            bg="#4d636d",
            fg="white",
        )
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        menu_logo_path = os.path.join(IMAGE_DIR, "menu_im.png")
        self.MenuLogo = load_tk_image(menu_logo_path, (200, 200))

        LeftMenu = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        LeftMenu.place(x=0, y=102, width=200, height=565)

        Label(LeftMenu, image=self.MenuLogo).pack(side=TOP, fill=X)
        Label(LeftMenu, text="Menu", font=("times new roman", 20), bg="#009688").pack(
            side=TOP, fill=X
        )

        side_icon = os.path.join(IMAGE_DIR, "side.png")
        self.icon_side = PhotoImageSafe(self.root, side_icon)

        for text, cmd in self.menu:
            Button(
                LeftMenu,
                text=text,
                command=cmd,
                image=self.icon_side,
                compound=LEFT,
                padx=5,
                anchor="w",
                font=("times new roman", 20, "bold"),
                bg="white",
                bd=3,
                cursor="hand2",
            ).pack(side=TOP, fill=X)

        Button(
            LeftMenu,
            text="Exit",
            image=self.icon_side,
            compound=LEFT,
            padx=5,
            anchor="w",
            font=("times new roman", 20, "bold"),
            bg="white",
            bd=3,
            cursor="hand2",
            command=self.root.destroy,
        ).pack(side=TOP, fill=X)

        self.lbl_employee = Label(
            self.root,
            text="Total Employee\n{ 0 }",
            bd=5,
            relief=RIDGE,
            bg="#33bbf9",
            fg="white",
            font=("goudy old style", 20, "bold"),
        )
        self.lbl_employee.place(x=300, y=120, height=150, width=300)

        self.lbl_supplier = Label(
            self.root,
            text="Total Supplier\n{ 0 }",
            bd=5,
            relief=RIDGE,
            bg="#ff5722",
            fg="white",
            font=("goudy old style", 20, "bold"),
        )
        self.lbl_supplier.place(x=650, y=120, height=150, width=300)

        self.lbl_category = Label(
            self.root,
            text="Total Category\n{ 0 }",
            bd=5,
            relief=RIDGE,
            bg="#009688",
            fg="white",
            font=("goudy old style", 20, "bold"),
        )
        self.lbl_category.place(x=1000, y=120, height=150, width=300)

        self.lbl_product = Label(
            self.root,
            text="Total Product\n{ 0 }",
            bd=5,
            relief=RIDGE,
            bg="#607d8b",
            fg="white",
            font=("goudy old style", 20, "bold"),
        )
        self.lbl_product.place(x=300, y=300, height=150, width=300)

        self.lbl_sales = Label(
            self.root,
            text="Total Sales\n{ 0 }",
            bd=5,
            relief=RIDGE,
            bg="#ffc107",
            fg="white",
            font=("goudy old style", 20, "bold"),
        )
        self.lbl_sales.place(x=650, y=300, height=150, width=300)

        Label(
            self.root,
            text="IMS-Inventory Management System",
            font=("times new roman", 12),
            bg="#4d636d",
            fg="white",
        ).pack(side=BOTTOM, fill=X)

        self.update_content()

    def employee(self):
        self.new_win = Toplevel(self.root)
        employeeClass(self.new_win)

    def supplier(self):
        self.new_win = Toplevel(self.root)
        supplierClass(self.new_win)

    def category(self):
        self.new_win = Toplevel(self.root)
        categoryClass(self.new_win)

    def product(self):
        self.new_win = Toplevel(self.root)
        productClass(self.new_win)

    def sales(self):
        self.new_win = Toplevel(self.root)
        salesClass(self.new_win)

    def update_content(self):
        con = get_connection()
        cur = con.cursor()
        try:
            cur.execute("select * from product")
            product = cur.fetchall()
            self.lbl_product.config(text=f"Total Product\n[ {len(product)} ]")

            cur.execute("select * from category")
            category = cur.fetchall()
            self.lbl_category.config(text=f"Total Category\n[ {len(category)} ]")

            cur.execute("select * from employee")
            employee = cur.fetchall()
            self.lbl_employee.config(text=f"Total Employee\n[ {len(employee)} ]")

            cur.execute("select * from supplier")
            supplier = cur.fetchall()
            self.lbl_supplier.config(text=f"Total Supplier\n[ {len(supplier)} ]")

            bill = len([f for f in os.listdir(BILL_DIR) if f.endswith(".txt")])
            self.lbl_sales.config(text=f"Total Sales\n[ {bill} ]")

            time_ = time.strftime("%I:%M:%S")
            date_ = time.strftime("%d-%m-%Y")
            self.lbl_clock.config(
                text=f"Welcome to Inventory Management System\t\t Date: {date_}\t\t Time: {time_}"
            )

            self.lbl_clock.after(200, self.update_content)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()


def PhotoImageSafe(root, path):
    """Return a Tk-compatible image; placeholder if the file is missing."""
    if os.path.isfile(path):
        from tkinter import PhotoImage

        return PhotoImage(file=path)
    im = Image.new("RGB", (64, 64), (230, 230, 230))
    return ImageTk.PhotoImage(im)


def load_tk_image(path, size):
    if not os.path.isfile(path):
        im = Image.new("RGB", size, (240, 240, 240))
        return ImageTk.PhotoImage(im)
    img = Image.open(path).resize(size)
    return ImageTk.PhotoImage(img)


if __name__ == "__main__":
    root = Tk()
    IMS(root)
    root.mainloop()
