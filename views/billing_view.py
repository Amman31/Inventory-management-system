import os
import tempfile
import time
from config import IMAGE_DIR
from services import billing_service
from components.table import scrolled_treeview

from tkinter import (Tk, Label,
    Button,
    Frame,
    Entry,
    Text,
    Scrollbar,
    StringVar,
    END,
    RIDGE,
    GROOVE,
    TOP,
    X,
    BOTH,
    RIGHT,
    Y,
    VERTICAL,
    LEFT,
    BOTTOM,
    messagebox,
)

# Billing class                 
class billClass:
    # Initialize billing class
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+110+80")
        # Set root geometry
        self.root.resizable(False, False)
        self.root.config(bg="white")
        self.cart_list = []
        self.chk_print = 0

        logo = os.path.join(IMAGE_DIR, "logo1.png")
        if os.path.isfile(logo):
            from tkinter import PhotoImage

            self.icon_title = PhotoImage(file=logo)
        else:
            from PIL import Image, ImageTk

            im = Image.new("RGB", (64, 64), (200, 200, 200))
            self.icon_title = ImageTk.PhotoImage(im)

        # Inventory management system label
        Label(
            self.root,
            text="Inventory Management System",
            image=self.icon_title,
            compound=LEFT,
            font=("times new roman", 40, "bold"),
            bg="#010c48",
            fg="white",
            anchor="w",
            padx=20,
        ).place(x=0, y=0, relwidth=1, height=70)

        # Logout button
        Button(
            self.root,
            text="Logout",
            font=("times new roman", 15, "bold"),
            bg="yellow",
            cursor="hand2",
        ).place(x=1150, y=10, height=50, width=150)

        # Clock label
        self.lbl_clock = Label(
            self.root,
            text="Welcome to Inventory Management System\t\t Date: DD:MM:YYYY\t\t Time: HH:MM:SS",
            font=("times new roman", 15),
            bg="#4d636d",
            fg="white",
        )
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        # Product frame 1
        ProductFrame1 = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        ProductFrame1.place(x=6, y=110, width=410, height=550)

        # Product frame 1 label
        Label(
            ProductFrame1,
            text="All Products",
            font=("goudy old style", 20, "bold"),
            bg="#262626",
            fg="white",
        ).pack(side=TOP, fill=X)

        # Search variable
        self.var_search = StringVar()

        # Product frame 2
        ProductFrame2 = Frame(ProductFrame1, bd=2, relief=RIDGE, bg="white")
        ProductFrame2.place(x=2, y=42, width=398, height=90)

        # Product frame 2 label
        Label(
            ProductFrame2,
            text="Search Product | By Name",
            font=("times new roman", 15, "bold"),
            bg="white",
            fg="green",
        ).place(x=2, y=5)

        # Product name label
        Label(
            ProductFrame2,
            text="Product Name",
            font=("times new roman", 15, "bold"),
            bg="white",
        ).place(x=2, y=45)
        # Product name entry
        Entry(
            ProductFrame2,
            textvariable=self.var_search,
            font=("times new roman", 15),
            bg="lightyellow",
        ).place(x=128, y=47, width=150, height=22)
        # Search button
        Button(
            ProductFrame2,
            text="Search",
            command=self.search,
            font=("goudy old style", 15),
            bg="#2196f3",
            fg="white",
            cursor="hand2",
        ).place(x=285, y=45, width=100, height=25)
        # Show all button
        Button(
            ProductFrame2,
            text="Show All",
            command=self.show,
            font=("goudy old style", 15),
            bg="#083531",
            fg="white",
            cursor="hand2",
        ).place(x=285, y=10, width=100, height=25)

        # Product columns
        pcols = ("pid", "name", "price", "qty", "status")
        # Product headings
        pheads = {
            "pid": "P ID",
            "name": "Name",
            "price": "Price",
            "qty": "Quantity",
            "status": "Status",
        }
        # Product widths
        pwidths = {"pid": 40, "name": 100, "price": 100, "qty": 40, "status": 90}
        # Product frame 3
        ProductFrame3, self.product_Table = scrolled_treeview(
            ProductFrame1, pcols, pheads, pwidths
        )
        ProductFrame3.place(x=2, y=140, width=398, height=375)
        self.product_Table.bind("<ButtonRelease-1>", self.get_data)
        self.show()
        # Note label
        Label(
            ProductFrame1,
            text="Note: 'Enter 0 Quantity to remove product from the Cart'",
            font=("goudy old style", 12),
            anchor="w",
            bg="white",
            fg="red",
        ).pack(side=BOTTOM, fill=X)
        # Customer name variable
        self.var_cname = StringVar()
        self.var_contact = StringVar()
        # Customer frame
        CustomerFrame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        CustomerFrame.place(x=420, y=110, width=530, height=70)
        # Customer details label
        Label(
            CustomerFrame,
            text="Customer Details",
            font=("goudy old style", 15),
            bg="lightgray",
        ).pack(side=TOP, fill=X)
        # Name label
        Label(CustomerFrame, text="Name", font=("times new roman", 15), bg="white").place(
            x=5, y=35
        )
        # Name entry
        Entry(
            CustomerFrame,
            textvariable=self.var_cname,
            font=("times new roman", 13),
            bg="lightyellow",
        ).place(x=80, y=35, width=180)

        # Contact no. label
        Label(
            CustomerFrame, text="Contact No.", font=("times new roman", 15), bg="white"
        ).place(x=270, y=35)
        # Contact no. entry
        Entry(
            CustomerFrame,
            textvariable=self.var_contact,
            font=("times new roman", 15),
            bg="lightyellow",
        ).place(x=380, y=35, width=140)

        # Cal cart frame
        Cal_Cart_Frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        Cal_Cart_Frame.place(x=420, y=190, width=530, height=360)

        # Cal input variable
        self.var_cal_input = StringVar()
        # Cal frame

        Cal_Frame = Frame(Cal_Cart_Frame, bd=9, relief=RIDGE, bg="white")
        Cal_Frame.place(x=5, y=10, width=268, height=340)

        # Cal input entry
        self.txt_cal_input = Entry(
            Cal_Frame,
            textvariable=self.var_cal_input,
            font=("arial", 15, "bold"),
            width=21,
            bd=10,
            relief=GROOVE,
            state="readonly",
            justify="right",
        )
        self.txt_cal_input.grid(row=0, columnspan=4)

        # Cal button
        def cal_btn(txt, r, c, pady=10):
            if txt == "C":
                return Button(
                    Cal_Frame,
                    text=txt,
                    font=("arial", 15, "bold"),
                    command=self.clear_cal,
                    bd=5,
                    width=4,
                    pady=pady,
                    cursor="hand2",
                ).grid(row=r, column=c)
            if txt == "=":
                return Button(
                    Cal_Frame,
                    text=txt,
                    font=("arial", 15, "bold"),
                    command=self.perform_cal,
                    bd=5,
                    width=4,
                    pady=pady,
                    cursor="hand2",
                ).grid(row=r, column=c)
            return Button(
                Cal_Frame,
                text=txt,
                font=("arial", 15, "bold"),
                command=lambda t=txt: self.get_input(t),
                bd=5,
                width=4,
                pady=pady,
                cursor="hand2",
            ).grid(row=r, column=c)
    # Cal buttons
        cal_btn(7, 1, 0)
        cal_btn(8, 1, 1)
        cal_btn(9, 1, 2)
        cal_btn("+", 1, 3)
        cal_btn(4, 2, 0)
        cal_btn(5, 2, 1)
        cal_btn(6, 2, 2)
        cal_btn("-", 2, 3)
        cal_btn(1, 3, 0)
        cal_btn(2, 3, 1)
        cal_btn(3, 3, 2)
        cal_btn("*", 3, 3)
        cal_btn(0, 4, 0, pady=15)
        cal_btn("C", 4, 1, pady=15)
        cal_btn("=", 4, 2, pady=15)
        cal_btn("/", 4, 3, pady=15)
        # Cart frame
        Cart_Frame = Frame(Cal_Cart_Frame, bd=3, relief=RIDGE)
        Cart_Frame.place(x=280, y=8, width=245, height=342)
        # Cart title label
        self.cartTitle = Label(
            Cart_Frame,
            text="Cart \t Total Products: [0]",
            font=("goudy old style", 15),
            bg="lightgray",
        )
        self.cartTitle.pack(side=TOP, fill=X)
        # Cart columns              
        ccols = ("pid", "name", "price", "qty")
        # Cart headings
        cheads = {"pid": "P ID", "name": "Name", "price": "Price", "qty": "Quantity"}
        # Cart widths
        cwidths = {"pid": 40, "name": 100, "price": 90, "qty": 30}
        # Cart inner frame
        cart_inner, self.CartTable = scrolled_treeview(Cart_Frame, ccols, cheads, cwidths)
        # Cart inner frame pack
        cart_inner.pack(fill=BOTH, expand=1)
        self.CartTable.bind("<ButtonRelease-1>", self.get_data_cart)
        # Product id variable
        self.var_pid = StringVar()
        # Product name variable
        self.var_pname = StringVar()
        # Product price variable
        self.var_price = StringVar()
        # Product quantity variable
        self.var_qty = StringVar()
        # Product stock variable
        self.var_stock = StringVar()
        # Add cart widgets frame
        # Add cart widgets frame
        Add_CartWidgets_Frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        Add_CartWidgets_Frame.place(x=420, y=550, width=530, height=110)
        # Product name label
        Label(
            Add_CartWidgets_Frame,
            text="Product Name",
            font=("times new roman", 15),
            bg="white",
        ).place(x=5, y=5)
        # Product name entry
        Entry(
            Add_CartWidgets_Frame,
            textvariable=self.var_pname,
            font=("times new roman", 15),
            bg="lightyellow",
            state="readonly",
        ).place(x=5, y=35, width=190, height=22)

        # Price per qty label
        Label(
            Add_CartWidgets_Frame,
            text="Price Per Qty",
            font=("times new roman", 15),
            bg="white",
        ).place(x=230, y=5)
        # Price per qty entry
        Entry(
            Add_CartWidgets_Frame,
            textvariable=self.var_price,
            font=("times new roman", 15),
            bg="lightyellow",
            state="readonly",
        ).place(x=230, y=35, width=150, height=22)

        # Quantity label
        Label(
            Add_CartWidgets_Frame,
            text="Quantity",
            font=("times new roman", 15),
            bg="white",
        ).place(x=390, y=5)
        # Quantity entry
        Entry(
            Add_CartWidgets_Frame,
            textvariable=self.var_qty,
            font=("times new roman", 15),
            bg="lightyellow",
        ).place(x=390, y=35, width=120, height=22)

        # In stock label
        self.lbl_inStock = Label(
            Add_CartWidgets_Frame,
            text="In Stock",
            font=("times new roman", 15),
            bg="white",
        )
        self.lbl_inStock.place(x=5, y=70)

        # Clear button
        Button(
            Add_CartWidgets_Frame,
            command=self.clear_cart,
            text="Clear",
            font=("times new roman", 15, "bold"),
            bg="lightgray",
            cursor="hand2",
        ).place(x=180, y=70, width=150, height=30)
        # Add | Update button
        Button(
            Add_CartWidgets_Frame,
            command=self.add_update_cart,
            text="Add | Update",
            font=("times new roman", 15, "bold"),
            bg="orange",
            cursor="hand2",
        ).place(x=340, y=70, width=180, height=30)

        # Bill frame
        billFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        billFrame.place(x=953, y=110, width=400, height=410)

        # Customer bill area label
        Label(
            billFrame,
            text="Customer Bill Area",
            font=("goudy old style", 20, "bold"),
            bg="#262626",
            fg="white",
        ).pack(side=TOP, fill=X)
        # Customer bill area scrollbar
        scrolly_b = Scrollbar(billFrame, orient=VERTICAL)
        scrolly_b.pack(side=RIGHT, fill=Y)
        # Customer bill area text
        self.txt_bill_area = Text(billFrame, yscrollcommand=scrolly_b.set)
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        scrolly_b.config(command=self.txt_bill_area.yview)
        # Bill menu frame

        billMenuFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        billMenuFrame.place(x=953, y=520, width=400, height=140)

        # Bill amount label
        self.lbl_amnt = Label(
            billMenuFrame,
            text="Bill Amount\n[0]",
            font=("goudy old style", 15, "bold"),
            bg="#3f51b5",
            fg="white",
        )
        self.lbl_amnt.place(x=2, y=5, width=120, height=70)

        # Discount label
        self.lbl_discount = Label(
            billMenuFrame,
            text="Discount\n[5%]",
            font=("goudy old style", 15, "bold"),
            bg="#8bc34a",
            fg="white",
        )
        self.lbl_discount.place(x=124, y=5, width=120, height=70)

        # Net pay label
        self.lbl_net_pay = Label(
            billMenuFrame,
            text="Net Pay\n[0]",
            font=("goudy old style", 15, "bold"),
            bg="#607d8b",
            fg="white",
        )
        self.lbl_net_pay.place(x=246, y=5, width=160, height=70)

        # Print button
        Button(
            billMenuFrame,
            text="Print",
            command=self.print_bill,
            cursor="hand2",
            font=("goudy old style", 15, "bold"),
            bg="lightgreen",
            fg="white",
        ).place(x=2, y=80, width=120, height=50)

        # Clear all button
        Button(
            billMenuFrame,
            text="Clear All",
            command=self.clear_all,
            cursor="hand2",
            font=("goudy old style", 15, "bold"),
            bg="gray",
            fg="white",
        ).place(x=124, y=80, width=120, height=50)

        # Generate bill button
        Button(
            billMenuFrame,
            text="Generate Bill",
            command=self.generate_bill,
            cursor="hand2",
            font=("goudy old style", 15, "bold"),
            bg="#009688",
            fg="white",
        ).place(x=246, y=80, width=160, height=50)

        self.show()
        self.update_date_time()

    # Get input
    def get_input(self, num):
        xnum = self.var_cal_input.get() + str(num)
        self.var_cal_input.set(xnum)

    # Clear cal
    def clear_cal(self):
        self.var_cal_input.set("")

    # Perform cal
    def perform_cal(self):
        result = self.var_cal_input.get()
        self.var_cal_input.set(str(eval(result)))

    # Show products
    def show(self):
        try:
            rows = billing_service.fetch_active_products_for_table()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    # Search products
    def search(self):
        rows, err = billing_service.search_active_products_by_name(self.var_search.get())
        if err:
            messagebox.showerror("Error", err, parent=self.root)
            return
        self.product_Table.delete(*self.product_Table.get_children())
        for row in rows:
            self.product_Table.insert("", END, values=row)

    # Get product data
    def get_data(self, ev):
        f = self.product_Table.focus()
        content = self.product_Table.item(f)
        row = content["values"]
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_inStock.config(text=f"In Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set("1")

    # Get cart data
    def get_data_cart(self, ev):
        f = self.CartTable.focus()
        content = self.CartTable.item(f)
        row = content["values"]
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        stock = None
        for r in self.cart_list:
            if str(r[0]) == str(row[0]):
                stock = r[4]
                break
        if stock is not None:
            self.lbl_inStock.config(text=f"In Stock [{str(stock)}]")
            self.var_stock.set(stock)

    # Add | Update cart
    def add_update_cart(self):
        ok, msg = billing_service.validate_cart_add(
            self.var_pid.get(), self.var_qty.get(), self.var_stock.get()
        )
        if not ok:
            messagebox.showerror("Error", msg, parent=self.root)
            return
        price_cal = self.var_price.get()
        cart_data = [
            self.var_pid.get(),
            self.var_pname.get(),
            price_cal,
            self.var_qty.get(),
            self.var_stock.get(),
        ]
        idx = billing_service.find_duplicate_cart_index(self.cart_list, self.var_pid.get())
        if idx >= 0:
            if not messagebox.askyesno(
                "Confirm",
                "Product already present\nDo you want to Update|Remove from the Cart List",
                parent=self.root,
            ):
                return
            self.cart_list = billing_service.update_cart_after_confirm(
                self.cart_list, idx, self.var_qty.get()
            )
        else:
            self.cart_list = billing_service.append_cart_row(self.cart_list, cart_data)
        self.show_cart()
        self.bill_update()

    # Bill update
    def bill_update(self):
        self.bill_amnt, self.discount, self.net_pay = billing_service.compute_bill_totals(
            self.cart_list
        )
        self.lbl_amnt.config(text=f"Bill Amnt\n{str(self.bill_amnt)}")
        self.lbl_net_pay.config(text=f"Net Pay\n{str(self.net_pay)}")
        self.cartTitle.config(
            text=f"Cart \t Total Products: [{str(len(self.cart_list))}]"
        )

    # Show cart
    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert("", END, values=row[:4])
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

    # Generate bill
    def generate_bill(self):
        ok, msg = billing_service.validate_generate_bill(
            self.var_cname.get(), self.var_contact.get(), self.cart_list
        )
        if not ok:
            messagebox.showerror("Error", msg, parent=self.root)
            return
        self.invoice = billing_service.generate_invoice_number()
        top = billing_service.format_bill_top_text(
            self.var_cname.get(), self.var_contact.get(), self.invoice
        )
        self.txt_bill_area.delete("1.0", END)
        self.txt_bill_area.insert("1.0", top)
        for seg in billing_service.format_bill_middle_lines(self.cart_list):
            self.txt_bill_area.insert(END, seg)
        ok_db, err = billing_service.commit_cart_to_inventory(self.cart_list)
        if not ok_db:
            messagebox.showerror("Error", f"Error due to : {err}", parent=self.root)
            return
        self.bill_amnt, self.discount, self.net_pay = billing_service.compute_bill_totals(
            self.cart_list
        )
        bottom = billing_service.format_bill_bottom_text(
            self.bill_amnt, self.discount, self.net_pay
        )
        self.txt_bill_area.insert(END, bottom)
        billing_service.save_bill_file(self.invoice, self.txt_bill_area.get("1.0", END))
        messagebox.showinfo("Saved", "Bill has been generated", parent=self.root)
        self.chk_print = 1
        self.show()

    # Clear cart
    def clear_cart(self):
        self.var_pid.set("")
        self.var_pname.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.lbl_inStock.config(text="In Stock")
        self.var_stock.set("")

    # Clear all
    def clear_all(self):
        self.cart_list.clear()
        self.clear_cart()
        self.show()
        self.show_cart()
        self.var_cname.set("")
        self.var_contact.set("")
        self.chk_print = 0
        self.txt_bill_area.delete("1.0", END)
        self.cartTitle.config(text="Cart \t Total Products: [0]")
        self.var_search.set("")

    # Update date time
    def update_date_time(self):
        time_ = time.strftime("%I:%M:%S")
        date_ = time.strftime("%d-%m-%Y")
        self.lbl_clock.config(
            text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}"
        )
        self.lbl_clock.after(200, self.update_date_time)

    # Print bill
    def print_bill(self):
        if self.chk_print == 1:
            messagebox.showinfo("Print", "Please wait while printing", parent=self.root)
            new_file = tempfile.mktemp(".txt")
            with open(new_file, "w", encoding="utf-8") as f:
                f.write(self.txt_bill_area.get("1.0", END))
            if os.name == "nt":
                os.startfile(new_file, "print")
            else:
                messagebox.showinfo(
                    "Print", "Saved to temp file; open and print manually.", parent=self.root
                )
        else:
            messagebox.showinfo(
                "Print", "Please generate bill to print the receipt", parent=self.root
            )


if __name__ == "__main__":
    root = Tk()
    billClass(root)
    root.mainloop()
