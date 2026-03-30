from tkinter import Tk, Label, Entry, Text, StringVar, END

from tkinter import messagebox

from config.database import get_connection
from app.ui import Theme, configure_crud_window, crud_action_buttons, scrolled_treeview
from app.ui.buttons import search_button


class supplierClass:
    def __init__(self, root):
        self.root = root
        configure_crud_window(self.root)

        self.var_searchtxt = StringVar()
        self.var_sup_invoice = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()

        Label(self.root, text="Invoice No.", bg=Theme.BG_WHITE, font=Theme.FONT_GOUDY).place(
            x=700, y=80
        )
        Entry(
            self.root,
            textvariable=self.var_searchtxt,
            font=Theme.FONT_GOUDY,
            bg=Theme.BG_ENTRY,
        ).place(x=850, y=80, width=160)
        search_button(self.root, self.search, x=980, y=79, width=100, height=28)

        Label(
            self.root,
            text="Supplier Details",
            font=("goudy old style", 20, "bold"),
            bg=Theme.BG_TITLE_BLUE,
            fg="white",
        ).place(x=50, y=10, width=1000, height=40)

        Label(self.root, text="Invoice No.", font=Theme.FONT_GOUDY, bg=Theme.BG_WHITE).place(
            x=50, y=80
        )
        Entry(
            self.root,
            textvariable=self.var_sup_invoice,
            font=Theme.FONT_GOUDY,
            bg=Theme.BG_ENTRY,
        ).place(x=180, y=80, width=180)

        Label(self.root, text="Name", font=Theme.FONT_GOUDY, bg=Theme.BG_WHITE).place(x=50, y=120)
        Entry(
            self.root,
            textvariable=self.var_name,
            font=Theme.FONT_GOUDY,
            bg=Theme.BG_ENTRY,
        ).place(x=180, y=120, width=180)

        Label(self.root, text="Contact", font=Theme.FONT_GOUDY, bg=Theme.BG_WHITE).place(
            x=50, y=160
        )
        Entry(
            self.root,
            textvariable=self.var_contact,
            font=Theme.FONT_GOUDY,
            bg=Theme.BG_ENTRY,
        ).place(x=180, y=160, width=180)

        Label(self.root, text="Description", font=Theme.FONT_GOUDY, bg=Theme.BG_WHITE).place(
            x=50, y=200
        )
        self.txt_desc = Text(self.root, font=Theme.FONT_GOUDY, bg=Theme.BG_ENTRY)
        self.txt_desc.place(x=180, y=200, width=470, height=120)

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

        sup_frame, self.SupplierTable = scrolled_treeview(
            self.root, cols, headings, widths
        )
        sup_frame.place(x=700, y=120, width=380, height=350)
        self.SupplierTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()

    def add(self):
        con = get_connection()
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice must be required", parent=self.root)
            else:
                cur.execute(
                    "Select * from supplier where invoice=?", (self.var_sup_invoice.get(),)
                )
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror(
                        "Error", "Invoice no. is already assigned", parent=self.root
                    )
                else:
                    cur.execute(
                        "insert into supplier(invoice,name,contact,desc) values(?,?,?,?)",
                        (
                            self.var_sup_invoice.get(),
                            self.var_name.get(),
                            self.var_contact.get(),
                            self.txt_desc.get("1.0", END),
                        ),
                    )
                    con.commit()
                    messagebox.showinfo("Success", "Supplier Added Successfully", parent=self.root)
                    self.clear()
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")
        finally:
            con.close()

    def show(self):
        con = get_connection()
        cur = con.cursor()
        try:
            cur.execute("select * from supplier")
            rows = cur.fetchall()
            self.SupplierTable.delete(*self.SupplierTable.get_children())
            for row in rows:
                self.SupplierTable.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")
        finally:
            con.close()

    def get_data(self, ev):
        f = self.SupplierTable.focus()
        content = self.SupplierTable.item(f)
        row = content["values"]
        self.var_sup_invoice.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])
        self.txt_desc.delete("1.0", END)
        self.txt_desc.insert(END, row[3])

    def update(self):
        con = get_connection()
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice must be required", parent=self.root)
            else:
                cur.execute(
                    "Select * from supplier where invoice=?", (self.var_sup_invoice.get(),)
                )
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Invoice No.", parent=self.root)
                else:
                    cur.execute(
                        "update supplier set name=?,contact=?,desc=? where invoice=?",
                        (
                            self.var_name.get(),
                            self.var_contact.get(),
                            self.txt_desc.get("1.0", END),
                            self.var_sup_invoice.get(),
                        ),
                    )
                    con.commit()
                    messagebox.showinfo("Success", "Supplier Updated Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")
        finally:
            con.close()

    def delete(self):
        con = get_connection()
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice No. must be required", parent=self.root)
            else:
                cur.execute(
                    "Select * from supplier where invoice=?", (self.var_sup_invoice.get(),)
                )
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Invoice No.", parent=self.root)
                else:
                    op = messagebox.askyesno(
                        "Confirm", "Do you really want to delete?", parent=self.root
                    )
                    if op:
                        cur.execute(
                            "delete from supplier where invoice=?", (self.var_sup_invoice.get(),)
                        )
                        con.commit()
                        messagebox.showinfo(
                            "Delete", "Supplier Deleted Successfully", parent=self.root
                        )
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")
        finally:
            con.close()

    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_desc.delete("1.0", END)
        self.var_searchtxt.set("")
        self.show()

    def search(self):
        con = get_connection()
        cur = con.cursor()
        try:
            if self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Invoice No. should be required", parent=self.root)
            else:
                cur.execute("select * from supplier where invoice=?", (self.var_searchtxt.get(),))
                row = cur.fetchone()
                if row is not None:
                    self.SupplierTable.delete(*self.SupplierTable.get_children())
                    self.SupplierTable.insert("", END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")
        finally:
            con.close()


if __name__ == "__main__":
    root = Tk()
    supplierClass(root)
    root.mainloop()
