from tkinter import Tk, Label, Entry, Text, StringVar, END

from tkinter import messagebox

from services import supplier_service
from components import Theme, configure_crud_window, crud_action_buttons, scrolled_treeview
from components.buttons import search_button

# Supplier class
class supplierClass:
    def __init__(self, root):
        self.root = root
        configure_crud_window(self.root)

        # Search text variable
        self.var_searchtxt = StringVar()
        # Supplier invoice variable
        self.var_sup_invoice = StringVar()
        # Name variable
        self.var_name = StringVar()
        # Contact variable
        self.var_contact = StringVar()

        # Invoice no. label
        Label(self.root, text="Invoice No.", bg=Theme.BG_WHITE, font=Theme.FONT_GOUDY).place(
            x=700, y=80
        )
        # Invoice no. entry
        Entry(
            self.root,
            textvariable=self.var_searchtxt,
            font=Theme.FONT_GOUDY,
            bg=Theme.BG_ENTRY,
        ).place(x=850, y=80, width=160)
        search_button(self.root, self.search, x=980, y=79, width=100, height=28)

        # Supplier details label
        Label(
            self.root,
            text="Supplier Details",
            font=("goudy old style", 20, "bold"),
            bg=Theme.BG_TITLE_BLUE,
            fg="white",
        ).place(x=50, y=10, width=1000, height=40)

        # Invoice no. label
        Label(self.root, text="Invoice No.", font=Theme.FONT_GOUDY, bg=Theme.BG_WHITE).place(
            x=50, y=80
        )
        # Invoice no. entry
        Entry(
            self.root,
            textvariable=self.var_sup_invoice,
            font=Theme.FONT_GOUDY,
            bg=Theme.BG_ENTRY,
        ).place(x=180, y=80, width=180)

        Label(self.root, text="Name", font=Theme.FONT_GOUDY, bg=Theme.BG_WHITE).place(x=50, y=120)
        # Name entry
        Entry(
            self.root,
            textvariable=self.var_name,
            font=Theme.FONT_GOUDY,
            bg=Theme.BG_ENTRY,
        ).place(x=180, y=120, width=180)

        Label(self.root, text="Contact", font=Theme.FONT_GOUDY, bg=Theme.BG_WHITE).place(
            x=50, y=160
        )
        # Contact entry
        Entry(
            self.root,
            textvariable=self.var_contact,
            font=Theme.FONT_GOUDY,
            bg=Theme.BG_ENTRY,
        ).place(x=180, y=160, width=180)

        Label(self.root, text="Description", font=Theme.FONT_GOUDY, bg=Theme.BG_WHITE).place(
            x=50, y=200
        )
        # Description text
        self.txt_desc = Text(self.root, font=Theme.FONT_GOUDY, bg=Theme.BG_ENTRY)
        self.txt_desc.place(x=180, y=200, width=470, height=120)

        # Crud action buttons
        crud_action_buttons(
            self.root,
            {
                "save": self.add,
                "update": self.update,
                "delete": self.delete,
                "clear": self.clear,
            },
            [
                (180, 370, 110, 35),
                (300, 370, 110, 35),
                (420, 370, 110, 35),
                (540, 370, 110, 35),
            ],
        )

        cols = ("invoice", "name", "contact", "desc")
        headings = {
            "invoice": "Invoice",
            "name": "Name",
            "contact": "Contact",
            "desc": "Description",
        }
        widths = {"invoice": 90, "name": 100, "contact": 100, "desc": 100}

        # Supplier table
        sup_frame, self.SupplierTable = scrolled_treeview(
            self.root, cols, headings, widths
        )
        sup_frame.place(x=700, y=120, width=380, height=350)
        self.SupplierTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()

    # Add supplier
    def add(self):
        ok, msg = supplier_service.add_supplier(
            self.var_sup_invoice.get(),
            self.var_name.get(),
            self.var_contact.get(),
            self.txt_desc.get("1.0", END),
        )
        if ok:
            messagebox.showinfo("Success", msg, parent=self.root)
            self.clear()
            self.show()
        else:
            messagebox.showerror("Error", msg, parent=self.root)

    # Show suppliers
    def show(self):
        try:
            rows = supplier_service.fetch_all_suppliers()
            self.SupplierTable.delete(*self.SupplierTable.get_children())
            for row in rows:
                self.SupplierTable.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    # Get supplier data
    def get_data(self, ev):
        f = self.SupplierTable.focus()
        content = self.SupplierTable.item(f)
        row = content["values"]
        self.var_sup_invoice.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])
        self.txt_desc.delete("1.0", END)
        self.txt_desc.insert(END, row[3])

    # Update supplier
    def update(self):
        ok, msg = supplier_service.update_supplier(
            self.var_sup_invoice.get(),
            self.var_name.get(),
            self.var_contact.get(),
            self.txt_desc.get("1.0", END),
        )
        if ok:
            messagebox.showinfo("Success", msg, parent=self.root)
            self.show()
        else:
            messagebox.showerror("Error", msg, parent=self.root)

    # Delete supplier
    def delete(self):
        inv = self.var_sup_invoice.get()
        if not inv:
            messagebox.showerror("Error", "Invoice No. must be required", parent=self.root)
            return
        if not supplier_service.supplier_invoice_exists(inv):
            messagebox.showerror("Error", "Invalid Invoice No.", parent=self.root)
            return
        if not messagebox.askyesno(
            "Confirm", "Do you really want to delete?", parent=self.root
        ):
            return
        ok, msg = supplier_service.delete_supplier_row(inv)
        if ok:
            messagebox.showinfo("Delete", msg, parent=self.root)
            self.clear()
        else:
            messagebox.showerror("Error", msg, parent=self.root)

    # Clear supplier data
    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_desc.delete("1.0", END)
        self.var_searchtxt.set("")
        self.show()

    # Search supplier
    def search(self):
        row, err = supplier_service.get_supplier_by_invoice(self.var_searchtxt.get())
        if err:
            messagebox.showerror("Error", err, parent=self.root)
            return
        self.SupplierTable.delete(*self.SupplierTable.get_children())
        self.SupplierTable.insert("", END, values=row)


if __name__ == "__main__":
    root = Tk()
    supplierClass(root)
    root.mainloop()
