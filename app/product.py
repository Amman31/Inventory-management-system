from tkinter import Tk, Frame, Label, Entry, StringVar, END, RIDGE

from tkinter import ttk, messagebox

from config.database import get_connection
from app.sql_helpers import product_search_sql
from app.ui import (
    Theme,
    configure_crud_window,
    crud_action_buttons,
    scrolled_treeview,
    search_label_frame,
)


class productClass:
    def __init__(self, root):
        self.root = root
        configure_crud_window(self.root)

        self.var_cat = StringVar()
        self.cat_list = []
        self.sup_list = []
        self.var_pid = StringVar()
        self.var_sup = StringVar()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.fetch_cat_sup()

        product_Frame = Frame(self.root, bd=2, relief=RIDGE, bg=Theme.BG_WHITE)
        product_Frame.place(x=10, y=10, width=450, height=480)

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
        Label(product_Frame, text="Supplier", font=Theme.FONT_GOUDY_TITLE, bg=Theme.BG_WHITE).place(
            x=30, y=110
        )
        Label(product_Frame, text="Name", font=Theme.FONT_GOUDY_TITLE, bg=Theme.BG_WHITE).place(
            x=30, y=160
        )
        Label(product_Frame, text="Price", font=Theme.FONT_GOUDY_TITLE, bg=Theme.BG_WHITE).place(
            x=30, y=210
        )
        Label(product_Frame, text="Quantity", font=Theme.FONT_GOUDY_TITLE, bg=Theme.BG_WHITE).place(
            x=30, y=260
        )
        Label(product_Frame, text="Status", font=Theme.FONT_GOUDY_TITLE, bg=Theme.BG_WHITE).place(
            x=30, y=310
        )

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

        Entry(
            product_Frame,
            textvariable=self.var_name,
            font=Theme.FONT_GOUDY,
            bg=Theme.BG_ENTRY,
        ).place(x=150, y=160, width=200)
        Entry(
            product_Frame,
            textvariable=self.var_price,
            font=Theme.FONT_GOUDY,
            bg=Theme.BG_ENTRY,
        ).place(x=150, y=210, width=200)
        Entry(
            product_Frame,
            textvariable=self.var_qty,
            font=Theme.FONT_GOUDY,
            bg=Theme.BG_ENTRY,
        ).place(x=150, y=260, width=200)

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

        cols = ("pid", "Category", "Supplier", "name", "price", "qty", "status")
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

        product_frame, self.ProductTable = scrolled_treeview(
            self.root, cols, headings, widths
        )
        product_frame.place(x=480, y=100, width=600, height=390)
        self.ProductTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()
        self.fetch_cat_sup()
        self.cmb_cat["values"] = self.cat_list
        self.cmb_sup["values"] = self.sup_list

    def fetch_cat_sup(self):
        self.cat_list.clear()
        self.sup_list.clear()
        self.cat_list.append("Empty")
        self.sup_list.append("Empty")
        con = get_connection()
        cur = con.cursor()
        try:
            cur.execute("select name from category")
            cat = cur.fetchall()
            if len(cat) > 0:
                self.cat_list.clear()
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])
            cur.execute("select name from supplier")
            sup = cur.fetchall()
            if len(sup) > 0:
                self.sup_list.clear()
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")
        finally:
            con.close()

    def add(self):
        con = get_connection()
        cur = con.cursor()
        try:
            if (
                self.var_cat.get() in ("Select", "Empty")
                or self.var_sup.get() in ("Select", "Empty")
            ):
                messagebox.showerror("Error", "All fields are required", parent=self.root)
            else:
                cur.execute("Select * from product where name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Product already present", parent=self.root)
                else:
                    cur.execute(
                        "insert into product(Category,Supplier,name,price,qty,status) values(?,?,?,?,?,?)",
                        (
                            self.var_cat.get(),
                            self.var_sup.get(),
                            self.var_name.get(),
                            self.var_price.get(),
                            self.var_qty.get(),
                            self.var_status.get(),
                        ),
                    )
                    con.commit()
                    messagebox.showinfo("Success", "Product Added Successfully", parent=self.root)
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
            cur.execute("select * from product")
            rows = cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")
        finally:
            con.close()

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

    def update(self):
        con = get_connection()
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Please select product from list", parent=self.root)
            else:
                cur.execute("Select * from product where pid=?", (self.var_pid.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Product", parent=self.root)
                else:
                    cur.execute(
                        "update product set Category=?,Supplier=?,name=?,price=?,qty=?,status=? where pid=?",
                        (
                            self.var_cat.get(),
                            self.var_sup.get(),
                            self.var_name.get(),
                            self.var_price.get(),
                            self.var_qty.get(),
                            self.var_status.get(),
                            self.var_pid.get(),
                        ),
                    )
                    con.commit()
                    messagebox.showinfo("Success", "Product Updated Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")
        finally:
            con.close()

    def delete(self):
        con = get_connection()
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Select Product from the list", parent=self.root)
            else:
                cur.execute("Select * from product where pid=?", (self.var_pid.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Product", parent=self.root)
                else:
                    op = messagebox.askyesno(
                        "Confirm", "Do you really want to delete?", parent=self.root
                    )
                    if op:
                        cur.execute("delete from product where pid=?", (self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo(
                            "Delete", "Product Deleted Successfully", parent=self.root
                        )
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")
        finally:
            con.close()

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

    def search(self):
        con = get_connection()
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Select Search By option", parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror(
                    "Error", "Search input should be required", parent=self.root
                )
            else:
                sql, params = product_search_sql(
                    self.var_searchby.get(), self.var_searchtxt.get()
                )
                cur.execute(sql, params)
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert("", END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)
        except ValueError:
            messagebox.showerror("Error", "Select Search By option", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")
        finally:
            con.close()


if __name__ == "__main__":
    root = Tk()
    productClass(root)
    root.mainloop()
