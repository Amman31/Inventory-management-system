from tkinter import Tk, Frame, Label, Entry, StringVar, END, RIDGE

from tkinter import ttk, messagebox

from services import product_service
from components import (
    Theme,
    configure_crud_window,
    crud_action_buttons,
    scrolled_treeview,
    search_label_frame,
)

# Product class
class productClass:
    def __init__(self, root):
        self.root = root
        configure_crud_window(self.root)

        # Category variable
        self.var_cat = StringVar()
        # Category list
        self.cat_list = []
        self.sup_list = []
        # Product ID variable
        self.var_pid = StringVar()
        # Supplier variable
        self.var_sup = StringVar()
        # Name variable
        self.var_name = StringVar()
        # Price variable
        self.var_price = StringVar()
        # Quantity variable
        self.var_qty = StringVar()
        # Status variable
        self.var_status = StringVar()
        # Search by variable
        self.var_searchby = StringVar()
        # Search text variable
        self.var_searchtxt = StringVar()

        # Fetch category and supplier list
        self.fetch_cat_sup()

        # Product frame
        product_Frame = Frame(self.root, bd=2, relief=RIDGE, bg=Theme.BG_WHITE)
        product_Frame.place(x=10, y=10, width=450, height=480)

        # Category label
        Label(
            product_Frame,
            text="Manage Product Details",
            font=Theme.FONT_GOUDY_TITLE,
            bg=Theme.BG_TITLE_BLUE,
            fg="white",
        ).pack(side="top", fill="x")

        Label(product_Frame, text="Category", font=Theme.FONT_GOUDY_TITLE, bg=Theme.BG_WHITE).place(
            x=30, y=60
        )
        # Supplier label
        Label(product_Frame, text="Supplier", font=Theme.FONT_GOUDY_TITLE, bg=Theme.BG_WHITE).place(
            x=30, y=110
        )
        # Name label
        Label(product_Frame, text="Name", font=Theme.FONT_GOUDY_TITLE, bg=Theme.BG_WHITE).place(
            x=30, y=160
        )
        # Price label
        Label(product_Frame, text="Price", font=Theme.FONT_GOUDY_TITLE, bg=Theme.BG_WHITE).place(
            x=30, y=210
        )
        # Quantity label
        Label(product_Frame, text="Quantity", font=Theme.FONT_GOUDY_TITLE, bg=Theme.BG_WHITE).place(
            x=30, y=260
        )
        # Status label
        Label(product_Frame, text="Status", font=Theme.FONT_GOUDY_TITLE, bg=Theme.BG_WHITE).place(
            x=30, y=310
        )

        # Category combobox
        self.cmb_cat = ttk.Combobox(
            product_Frame,
            textvariable=self.var_cat,
            values=self.cat_list,
            state="readonly",
            justify="center",
            font=Theme.FONT_GOUDY,
        )
        self.cmb_cat.place(x=150, y=60, width=200)
        self.cmb_cat.current(0)

        # Supplier combobox
        self.cmb_sup = ttk.Combobox(
            product_Frame,
            textvariable=self.var_sup,
            values=self.sup_list,
            state="readonly",
            justify="center",
            font=Theme.FONT_GOUDY,
        )
        self.cmb_sup.place(x=150, y=110, width=200)
        self.cmb_sup.current(0)

        # Name entry
        Entry(
            product_Frame,
            textvariable=self.var_name,
            font=Theme.FONT_GOUDY,
            bg=Theme.BG_ENTRY,
        ).place(x=150, y=160, width=200)
        # Price entry
        Entry(
            product_Frame,
            textvariable=self.var_price,
            font=Theme.FONT_GOUDY,
            bg=Theme.BG_ENTRY,
        ).place(x=150, y=210, width=200)
        # Quantity entry
        Entry(
            product_Frame,
            textvariable=self.var_qty,
            font=Theme.FONT_GOUDY,
            bg=Theme.BG_ENTRY,
        ).place(x=150, y=260, width=200)

        # Status combobox
        cmb_status = ttk.Combobox(
            product_Frame,
            textvariable=self.var_status,
            values=("Active", "Inactive"),
            state="readonly",
            justify="center",
            font=Theme.FONT_GOUDY,
        )
        cmb_status.place(x=150, y=310, width=200)
        cmb_status.current(0)

        # Crud action buttons
        crud_action_buttons(
            product_Frame,
            {
                "save": self.add,
                "update": self.update,
                "delete": self.delete,
                "clear": self.clear,
            },
            [
                (10, 400, 100, 40),
                (120, 400, 100, 40),
                (230, 400, 100, 40),
                (340, 400, 100, 40),
            ],
        )

        # Search label frame
        _, cmb_search = search_label_frame(
            self.root,
            "Search Product",
            self.var_searchby,
            ("Select", "Category", "Supplier", "Name"),
            self.var_searchtxt,
            self.search,
            x=480,
            y=10,
            width=600,
            height=80,
            btn_y=9,
        )
        cmb_search.current(0)

        # Columns
        cols = ("pid", "Category", "Supplier", "name", "price", "qty", "status")
        # Headings
        headings = {
            "pid": "P ID",
            "Category": "Category",
            "Supplier": "Supplier",
            "name": "Name",
            "price": "Price",
            "qty": "Quantity",
            "status": "Status",
        }
        widths = {c: 100 for c in cols}
        widths["pid"] = 90

        # Product table
        product_frame, self.ProductTable = scrolled_treeview(
            self.root, cols, headings, widths
        )
        product_frame.place(x=480, y=100, width=600, height=390)
        self.ProductTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()
        self.fetch_cat_sup()
        self.cmb_cat["values"] = self.cat_list
        self.cmb_sup["values"] = self.sup_list

    # Fetch category and supplier list
    def fetch_cat_sup(self):
        try:
            self.cat_list, self.sup_list = product_service.fetch_category_and_supplier_names()
        except RuntimeError as ex:
            self.cat_list = ["Empty"]
            self.sup_list = ["Empty"]
            messagebox.showerror("Error", str(ex), parent=self.root)

    # Add product
    def add(self):
        ok, msg = product_service.add_product(
            self.var_cat.get(),
            self.var_sup.get(),
            self.var_name.get(),
            self.var_price.get(),
            self.var_qty.get(),
            self.var_status.get(),
        )
        if ok:
            messagebox.showinfo("Success", msg, parent=self.root)
            self.clear()
            self.show()
        else:
            messagebox.showerror("Error", msg, parent=self.root)

    # Show products
    def show(self):
        try:
            rows = product_service.fetch_all_products()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    # Get product data
    def get_data(self, ev):
        f = self.ProductTable.focus()
        content = self.ProductTable.item(f)
        row = content["values"]
        self.var_pid.set(row[0])
        self.var_cat.set(row[1])
        self.var_sup.set(row[2])
        self.var_name.set(row[3])
        self.var_price.set(row[4])
        self.var_qty.set(row[5])
        self.var_status.set(row[6])

    # Update product
    def update(self):
        ok, msg = product_service.update_product(
            self.var_pid.get(),
            self.var_cat.get(),
            self.var_sup.get(),
            self.var_name.get(),
            self.var_price.get(),
            self.var_qty.get(),
            self.var_status.get(),
        )
        if ok:
            messagebox.showinfo("Success", msg, parent=self.root)
            self.show()
        else:
            messagebox.showerror("Error", msg, parent=self.root)

    # Delete product
    def delete(self):
        pid = self.var_pid.get()
        if not pid:
            messagebox.showerror("Error", "Select Product from the list", parent=self.root)
            return
        if not product_service.product_exists(pid):
            messagebox.showerror("Error", "Invalid Product", parent=self.root)
            return
        if not messagebox.askyesno(
            "Confirm", "Do you really want to delete?", parent=self.root
        ):
            return
        ok, msg = product_service.delete_product_row(pid)
        if ok:
            messagebox.showinfo("Delete", msg, parent=self.root)
            self.clear()
        else:
            messagebox.showerror("Error", msg, parent=self.root)

    # Clear product data
    def clear(self):
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_status.set("Active")
        self.var_pid.set("")
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")
        self.show()

    # Search products
    def search(self):
        rows, err = product_service.search_products(
            self.var_searchby.get(), self.var_searchtxt.get()
        )
        if err:
            messagebox.showerror("Error", err, parent=self.root)
            return
        self.ProductTable.delete(*self.ProductTable.get_children())
        for row in rows:
            self.ProductTable.insert("", END, values=row)


if __name__ == "__main__":
    root = Tk()
    productClass(root)
    root.mainloop()
