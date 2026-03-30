import os
import time

from tkinter import Tk, Label, Button, Frame, RIDGE, LEFT, TOP, X, BOTTOM, Toplevel
from tkinter import messagebox
from PIL import Image, ImageTk

from views.employee_view import employeeClass
from views.supplier_view import supplierClass
from views.category_view import categoryClass
from views.product_view import productClass
from views.sales_view import salesClass
from views.billing_view import billClass
from config import IMAGE_DIR
from services import dashboard_service

# Inventory Management System class
class IMS:
    def __init__(self, root, user_role: str = "employee", on_logout=None):
        self.root = root
        self.user_role = (user_role or "").strip().lower()
        self.on_logout = on_logout
        self.root.geometry("1350x750+110+20")

        self._child_windows = []

        # Menu items
        self._menu_all = (
            ("Employee", self.employee),
            ("Supplier", self.supplier),
            ("Category", self.category),
            ("Products", self.product),
            ("Sales", self.sales),
            ("Billings", self.billings),
        )
        self.menu = self._menu_all
        if self.user_role != "admin":
            # Employees can access only Sales + Billings.
            self.menu = (
                ("Sales", self.sales),
                ("Billings", self.billings),
            )
        self.root.resizable(False, False)
        self.root.config(bg="white")

        # Title of the dashboard
        logo_path = os.path.join(IMAGE_DIR, "logo1.png")
        self.icon_title = PhotoImageSafe(self.root, logo_path)
        title = Label(self.root, text="Inventory Management System", image=self.icon_title, compound=LEFT, font=("times new roman", 40, "bold"), bg="#010c48", fg="white", anchor="w", padx=20)
        title.place(x=0, y=0, relwidth=1, height=70)

        # Logout button
        Button(
            self.root,
            text="Logout",
            font=("times new roman", 15, "bold"),
            bg="yellow",
            cursor="hand2",
            command=self.logout,
        ).place(x=1150, y=10, height=50, width=150)

        # Clock label
        self.lbl_clock = Label(self.root, text="Welcome to Inventory Management System\t\t Date: DD:MM:YYYY\t\t Time: HH:MM:SS", font=("times new roman", 15), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        # Menu logo
        menu_logo_path = os.path.join(IMAGE_DIR, "menu_im.png")
        self.MenuLogo = load_tk_image(menu_logo_path, (200, 200))

        # Left menu
        LeftMenu = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        LeftMenu.place(x=0, y=102, width=200, height=765)

        # Menu logo and text
        Label(LeftMenu, image=self.MenuLogo).pack(side=TOP, fill=X)
        Label(LeftMenu, text="Menu", font=("times new roman", 20), bg="#009688").pack(
            side=TOP, fill=X
        )

        # Side icon
        side_icon = os.path.join(IMAGE_DIR, "side.png")
        self.icon_side = PhotoImageSafe(self.root, side_icon)

        # Menu buttons
        for text, cmd in self.menu:
            Button(LeftMenu, text=text, command=cmd, image=self.icon_side, compound=LEFT, padx=5, anchor="w", font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)

        # Exit button
        Button(LeftMenu, text="Exit", image=self.icon_side, compound=LEFT, padx=5, anchor="w", font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2", command=self.root.destroy).pack(side=TOP, fill=X)

        # Labels for the dashboard
        # Employee label
        self.lbl_employee = Label(self.root, text="Total Employee\n{ 0 }", bd=5, relief=RIDGE, bg="#33bbf9", fg="white", font=("goudy old style", 20, "bold")) 
        self.lbl_employee.place(x=300, y=120, height=150, width=300)

        # Supplier label
        self.lbl_supplier = Label(self.root, text="Total Supplier\n{ 0 }", bd=5, relief=RIDGE, bg="#ff5722", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_supplier.place(x=650, y=120, height=150, width=300)

        # Category label
        self.lbl_category = Label(self.root, text="Total Category\n{ 0 }", bd=5, relief=RIDGE, bg="#009688", fg="white", font=("goudy old style", 20, "bold")) 
        self.lbl_category.place(x=1000, y=120, height=150, width=300)

        # Product label
        self.lbl_product = Label(self.root, text="Total Product\n{ 0 }", bd=5, relief=RIDGE, bg="#607d8b", fg="white", font=("goudy old style", 20, "bold")) 
        self.lbl_product.place(x=300, y=300, height=150, width=300)

        # Sales label
        self.lbl_sales = Label(self.root, text="Total Sales\n{ 0 }", bd=5, relief=RIDGE, bg="#ffc107", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_sales.place(x=650, y=300, height=150, width=300)

        # IMS-Inventory Management System label
        Label(self.root, text="IMS-Inventory Management System", font=("times new roman", 12), bg="#4d636d", fg="white").pack(side=BOTTOM, fill=X)

        self.update_content()

    # Employee view
    def employee(self):
        self.new_win = Toplevel(self.root)
        self._child_windows.append(self.new_win)
        employeeClass(self.new_win)

    # Supplier view
    def supplier(self):
        self.new_win = Toplevel(self.root)
        self._child_windows.append(self.new_win)
        supplierClass(self.new_win)

    # Category view
    def category(self):
        self.new_win = Toplevel(self.root)
        self._child_windows.append(self.new_win)
        categoryClass(self.new_win)

    # Product view
    def product(self):
        self.new_win = Toplevel(self.root)
        self._child_windows.append(self.new_win)
        productClass(self.new_win)

    # Sales view
    def sales(self):
        self.new_win = Toplevel(self.root)
        self._child_windows.append(self.new_win)
        salesClass(self.new_win)
    
    # Billings view
    def billings(self):
        self.new_win = Toplevel(self.root)
        self._child_windows.append(self.new_win)
        billClass(self.new_win)

    def logout(self):
        # Close any open feature windows.
        for w in self._child_windows:
            try:
                w.destroy()
            except Exception:
                pass
        self._child_windows = []
        if self.on_logout:
            self.on_logout()

    # Update content
    def update_content(self):
        try:
            counts = dashboard_service.fetch_dashboard_counts()
            self.lbl_product.config(text=f"Total Product\n[ {counts['product']} ]")
            self.lbl_category.config(text=f"Total Category\n[ {counts['category']} ]")
            self.lbl_employee.config(text=f"Total Employee\n[ {counts['employee']} ]")
            self.lbl_supplier.config(text=f"Total Supplier\n[ {counts['supplier']} ]")
            self.lbl_sales.config(text=f"Total Sales\n[ {counts['sales_bills']} ]")

            time_ = time.strftime("%I:%M:%S")
            date_ = time.strftime("%d-%m-%Y")
            self.lbl_clock.config(
                text=f"Welcome to Inventory Management System\t\t Date: {date_}\t\t Time: {time_}"
            )

            self.lbl_clock.after(200, self.update_content)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

def PhotoImageSafe(root, path):
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

# Main function
if __name__ == "__main__":
    root = Tk()
    IMS(root, user_role="admin")
    root.mainloop()
