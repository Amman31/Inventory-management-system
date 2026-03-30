import os

from tkinter import (
    Tk,
    Label,
    Entry,
    Frame,
    Text,
    Scrollbar,
    Listbox,
    Button,
    StringVar,
    END,
    VERTICAL,
    BOTH,
    RIGHT,
    Y,
    RIDGE,
    TOP,
    X,
)
from tkinter import messagebox

from config import IMAGE_DIR
from services import sales_service
from components import Theme, configure_crud_window


# Sales class
class salesClass:
    def __init__(self, root):
        self.root = root
        configure_crud_window(self.root)

        # Invoice list
        self.blll_list = []
        # Invoice variable
        self.var_invoice = StringVar()

        # View customer bills label
        Label(
            self.root,
            text="View Customer Bills",
            font=("goudy old style", 30),
            bg="#184a45",
            fg="white",
            bd=3,
            relief=RIDGE,
        ).pack(side=TOP, fill=X, padx=10, pady=20)

        # Invoice no. label
        Label(self.root, text="Invoice No.", font=Theme.FONT_TIMES, bg=Theme.BG_WHITE).place(
            x=50, y=100
        )
        # Invoice no. entry
        Entry(
            self.root,
            textvariable=self.var_invoice,
            font=Theme.FONT_TIMES,
            bg=Theme.BG_ENTRY,
        ).place(x=160, y=100, width=180, height=28)

        # Search button
        Button(
            self.root,
            text="Search",
            command=self.search,
            font=Theme.FONT_TIMES_BOLD,
            bg="#2196f3",
            fg="white",
            cursor="hand2",
        ).place(x=360, y=100, width=120, height=28)

        # Clear button
        Button(
            self.root,
            text="Clear",
            command=self.clear,
            font=Theme.FONT_TIMES_BOLD,
            bg="lightgray",
            cursor="hand2",
        ).place(x=490, y=100, width=120, height=28)

        # Sales frame
        sales_Frame = Frame(self.root, bd=3, relief=RIDGE)
        sales_Frame.place(x=50, y=140, width=200, height=330)

        # Sales list
        scrolly = Scrollbar(sales_Frame, orient=VERTICAL)
        self.Sales_List = Listbox(
            sales_Frame,
            font=Theme.FONT_GOUDY,
            bg=Theme.BG_WHITE,
            yscrollcommand=scrolly.set,
        )
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=self.Sales_List.yview)
        self.Sales_List.pack(fill=BOTH, expand=1)
        self.Sales_List.bind("<ButtonRelease-1>", self.get_data)

        # Bill frame
        bill_Frame = Frame(self.root, bd=3, relief=RIDGE)
        bill_Frame.place(x=280, y=140, width=410, height=330)

        # Customer bill area label
        Label(
            bill_Frame,
            text="Customer Bill Area",
            font=("goudy old style", 20),
            bg="orange",
        ).pack(side=TOP, fill=X)

        # Customer bill area scrollbar
        scrolly2 = Scrollbar(bill_Frame, orient=VERTICAL)
        self.bill_area = Text(bill_Frame, bg=Theme.BG_ENTRY, yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT, fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH, expand=1)

        # Customer bill area image
        image_path = os.path.join(IMAGE_DIR, "cat2.jpg")
        if os.path.isfile(image_path):
            from PIL import Image, ImageTk

            self.bill_photo = Image.open(image_path)
            self.bill_photo = self.bill_photo.resize((450, 300))
            self.bill_photo = ImageTk.PhotoImage(self.bill_photo)
            Label(self.root, image=self.bill_photo, bd=0).place(x=700, y=110)

        self.show()

    # Show sales
    def show(self):
        self.blll_list.clear()
        self.Sales_List.delete(0, END)
        filenames, invoice_ids = sales_service.list_bill_display_entries()
        self.blll_list = invoice_ids
        for fn in filenames:
            self.Sales_List.insert(END, fn)

    # Get sales data
    def get_data(self, ev):
        index_ = self.Sales_List.curselection()
        if not index_:
            return

        file_name = self.Sales_List.get(index_)
        self.bill_area.delete("1.0", END)

        for line in sales_service.read_bill_lines_by_filename(file_name):
            self.bill_area.insert(END, line)

    # Search sales
    def search(self):
        if self.var_invoice.get() == "":
            messagebox.showerror("Error", "Invoice no. should be required", parent=self.root)
        elif sales_service.invoice_exists(self.var_invoice.get(), self.blll_list):
            self.bill_area.delete("1.0", END)
            for line in sales_service.read_bill_lines_by_invoice(self.var_invoice.get()):
                self.bill_area.insert(END, line)
        else:
            messagebox.showerror("Error", "Invalid Invoice No.", parent=self.root)

    # Clear sales
    def clear(self):
        self.show()
        self.bill_area.delete("1.0", END)

if __name__ == "__main__":
    root = Tk()
    salesClass(root)
    root.mainloop()
