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

from config.settings import IMAGE_DIR, BILL_DIR
from app.ui import Theme, configure_crud_window


class salesClass:
    def __init__(self, root):
        self.root = root
        configure_crud_window(self.root)

        self.blll_list = []
        self.var_invoice = StringVar()

        Label(
            self.root,
            text="View Customer Bills",
            font=("goudy old style", 30),
            bg="#184a45",
            fg="white",
            bd=3,
            relief=RIDGE,
        ).pack(side=TOP, fill=X, padx=10, pady=20)

        Label(self.root, text="Invoice No.", font=Theme.FONT_TIMES, bg=Theme.BG_WHITE).place(
            x=50, y=100
        )
        Entry(
            self.root,
            textvariable=self.var_invoice,
            font=Theme.FONT_TIMES,
            bg=Theme.BG_ENTRY,
        ).place(x=160, y=100, width=180, height=28)

        Button(
            self.root,
            text="Search",
            command=self.search,
            font=Theme.FONT_TIMES_BOLD,
            bg="#2196f3",
            fg="white",
            cursor="hand2",
        ).place(x=360, y=100, width=120, height=28)

        Button(
            self.root,
            text="Clear",
            command=self.clear,
            font=Theme.FONT_TIMES_BOLD,
            bg="lightgray",
            cursor="hand2",
        ).place(x=490, y=100, width=120, height=28)

        sales_Frame = Frame(self.root, bd=3, relief=RIDGE)
        sales_Frame.place(x=50, y=140, width=200, height=330)

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

        bill_Frame = Frame(self.root, bd=3, relief=RIDGE)
        bill_Frame.place(x=280, y=140, width=410, height=330)

        Label(
            bill_Frame,
            text="Customer Bill Area",
            font=("goudy old style", 20),
            bg="orange",
        ).pack(side=TOP, fill=X)

        scrolly2 = Scrollbar(bill_Frame, orient=VERTICAL)
        self.bill_area = Text(bill_Frame, bg=Theme.BG_ENTRY, yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT, fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH, expand=1)

        image_path = os.path.join(IMAGE_DIR, "cat2.jpg")
        if os.path.isfile(image_path):
            from PIL import Image, ImageTk

            self.bill_photo = Image.open(image_path)
            self.bill_photo = self.bill_photo.resize((450, 300))
            self.bill_photo = ImageTk.PhotoImage(self.bill_photo)
            Label(self.root, image=self.bill_photo, bd=0).place(x=700, y=110)

        self.show()

    def show(self):
        self.blll_list.clear()
        self.Sales_List.delete(0, END)
        if not os.path.isdir(BILL_DIR):
            return
        for i in os.listdir(BILL_DIR):
            if i.endswith(".txt"):
                self.Sales_List.insert(END, i)
                self.blll_list.append(i.split(".")[0])

    def get_data(self, ev):
        index_ = self.Sales_List.curselection()
        if not index_:
            return

        file_name = self.Sales_List.get(index_)
        self.bill_area.delete("1.0", END)

        file_path = os.path.join(BILL_DIR, file_name)
        with open(file_path, "r", encoding="utf-8", errors="replace") as fp:
            for line in fp:
                self.bill_area.insert(END, line)

    def search(self):
        if self.var_invoice.get() == "":
            messagebox.showerror("Error", "Invoice no. should be required", parent=self.root)
        elif self.var_invoice.get() in self.blll_list:
            file_path = os.path.join(BILL_DIR, f"{self.var_invoice.get()}.txt")
            self.bill_area.delete("1.0", END)
            with open(file_path, "r", encoding="utf-8", errors="replace") as fp:
                for line in fp:
                    self.bill_area.insert(END, line)
        else:
            messagebox.showerror("Error", "Invalid Invoice No.", parent=self.root)

    def clear(self):
        self.show()
        self.bill_area.delete("1.0", END)


if __name__ == "__main__":
    root = Tk()
    salesClass(root)
    root.mainloop()
