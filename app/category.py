import os

from tkinter import Tk, Label, Entry, Button, StringVar, END, RIDGE, RAISED
from tkinter import messagebox
from PIL import Image, ImageTk

from config.database import get_connection
from config.settings import IMAGE_DIR
from app.ui import Theme, configure_crud_window, scrolled_treeview


class categoryClass:
    def __init__(self, root):
        self.root = root
        configure_crud_window(self.root)

        self.var_cat_id = StringVar()
        self.var_name = StringVar()

        Label(
            self.root,
            text="Manage Product Category",
            font=("goudy old style", 30),
            bg="#184a45",
            fg="white",
            bd=3,
            relief=RIDGE,
        ).pack(side="top", fill="x", padx=10, pady=20)

        Label(
            self.root,
            text="Enter Category Name",
            font=("goudy old style", 30),
            bg=Theme.BG_WHITE,
        ).place(x=50, y=100)
        Entry(
            self.root,
            textvariable=self.var_name,
            bg=Theme.BG_ENTRY,
            font=("goudy old style", 18),
        ).place(x=50, y=170, width=300)

        Button(
            self.root,
            text="ADD",
            command=self.add,
            font=Theme.FONT_GOUDY,
            bg="#4caf50",
            fg="white",
            cursor="hand2",
        ).place(x=360, y=170, width=150, height=30)
        Button(
            self.root,
            text="Delete",
            command=self.delete,
            font=Theme.FONT_GOUDY,
            bg="red",
            fg="white",
            cursor="hand2",
        ).place(x=520, y=170, width=150, height=30)

        cols = ("cid", "name")
        headings = {"cid": "C ID", "name": "Name"}
        widths = {"cid": 90, "name": 100}
        cat_frame, self.CategoryTable = scrolled_treeview(self.root, cols, headings, widths)
        cat_frame.place(x=700, y=100, width=380, height=100)
        self.CategoryTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()

        self._place_optional_image("cat.jpg", x=50, y=220)
        self._place_optional_image("category.jpg", x=580, y=220)

    def _place_optional_image(self, filename, x, y):
        path = os.path.join(IMAGE_DIR, filename)
        if not os.path.isfile(path):
            return
        im = Image.open(path)
        im = im.resize((500, 250))
        photo = ImageTk.PhotoImage(im)
        lbl = Label(self.root, image=photo, bd=2, relief=RAISED)
        lbl.image = photo
        lbl.place(x=x, y=y)

    def add(self):
        con = get_connection()
        cur = con.cursor()
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Category Name must be required", parent=self.root)
            else:
                cur.execute("Select * from category where name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Category already present", parent=self.root)
                else:
                    cur.execute("insert into category(name) values(?)", (self.var_name.get(),))
                    con.commit()
                    messagebox.showinfo("Success", "Category Added Successfully", parent=self.root)
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
            cur.execute("select * from category")
            rows = cur.fetchall()
            self.CategoryTable.delete(*self.CategoryTable.get_children())
            for row in rows:
                self.CategoryTable.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")
        finally:
            con.close()

    def clear(self):
        self.var_name.set("")
        self.show()

    def get_data(self, ev):
        f = self.CategoryTable.focus()
        content = self.CategoryTable.item(f)
        row = content["values"]
        self.var_cat_id.set(row[0])
        self.var_name.set(row[1])

    def delete(self):
        con = get_connection()
        cur = con.cursor()
        try:
            if self.var_cat_id.get() == "":
                messagebox.showerror("Error", "Category name must be required", parent=self.root)
            else:
                cur.execute("Select * from category where cid=?", (self.var_cat_id.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Category Name", parent=self.root)
                else:
                    op = messagebox.askyesno(
                        "Confirm", "Do you really want to delete?", parent=self.root
                    )
                    if op:
                        cur.execute("delete from category where cid=?", (self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo(
                            "Delete", "Category Deleted Successfully", parent=self.root
                        )
                        self.clear()
                        self.var_cat_id.set("")
                        self.var_name.set("")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")
        finally:
            con.close()


if __name__ == "__main__":
    root = Tk()
    categoryClass(root)
    root.mainloop()
