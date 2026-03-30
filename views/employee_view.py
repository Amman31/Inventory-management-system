from tkinter import Tk, Label, Entry, Text, StringVar, END
from tkinter import ttk, messagebox

from services import employee_service
from components import (
    Theme,
    configure_crud_window,
    crud_action_buttons,
    primary_title_bar,
    scrolled_treeview,
    search_label_frame,
)


class employeeClass:
    def __init__(self, root):
        self.root = root
        configure_crud_window(self.root)

        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        self.var_emp_id = StringVar()
        self.var_gender = StringVar()
        self.var_contact = StringVar()
        self.var_name = StringVar()
        self.var_dob = StringVar()
        self.var_doj = StringVar()
        self.var_email = StringVar()
        self.var_pass = StringVar()
        self.var_utype = StringVar()
        self.var_salary = StringVar()

        _, cmb_search = search_label_frame(
            self.root,
            "Search Employee",
            self.var_searchby,
            ("Select", "Email", "Name", "Contact"),
            self.var_searchtxt,
            self.search,
            x=250,
            y=20,
            width=600,
            height=70,
        )
        cmb_search.current(0)
        # Primary title bar
        primary_title_bar(
            self.root, "Employee Details", x=50, y=100, width=1000, font=Theme.FONT_GOUDY
        )
        # Employee ID label
        Label(self.root, text="Emp ID", font=Theme.FONT_GOUDY, bg=Theme.BG_WHITE).place(
            x=50, y=150
        )
        # Gender label
        Label(self.root, text="Gender", font=Theme.FONT_GOUDY, bg=Theme.BG_WHITE).place(
            x=350, y=150
        )
        # Contact label
        Label(self.root, text="Contact", font=Theme.FONT_GOUDY, bg=Theme.BG_WHITE).place(
            x=750, y=150
        )

        # Employee ID entry
        Entry(
            self.root,
            textvariable=self.var_emp_id,
            font=Theme.FONT_GOUDY,
            bg=Theme.BG_ENTRY,
        ).place(x=150, y=150, width=180)
        # Gender combobox
        cmb_gender = ttk.Combobox(
            self.root,
            textvariable=self.var_gender,
            values=("Select", "Male", "Female", "Other"),
            state="readonly",
            justify="center",
            font=Theme.FONT_GOUDY,
        )
        cmb_gender.place(x=500, y=150, width=180)
        cmb_gender.current(0)
        # Contact entry
        Entry(
            self.root,
            textvariable=self.var_contact,
            font=Theme.FONT_GOUDY,
            bg=Theme.BG_ENTRY,
        ).place(x=850, y=150, width=180)

        # Name label
        Label(self.root, text="Name", font=Theme.FONT_GOUDY, bg=Theme.BG_WHITE).place(x=50, y=190)
        # Date of Birth label
        Label(self.root, text="D.O.B.", font=Theme.FONT_GOUDY, bg=Theme.BG_WHITE).place(
            x=350, y=190
        )
        # Date of Joining label
        Label(self.root, text="D.O.J.", font=Theme.FONT_GOUDY, bg=Theme.BG_WHITE).place(
            x=750, y=190
        )

        # Name entry
        Entry(
            self.root, textvariable=self.var_name, font=Theme.FONT_GOUDY, bg=Theme.BG_ENTRY
        ).place(x=150, y=190, width=180)
        # Date of Birth entry
        Entry(
            self.root, textvariable=self.var_dob, font=Theme.FONT_GOUDY, bg=Theme.BG_ENTRY
        ).place(x=500, y=190, width=180)
        # Date of Joining entry
        Entry(
            self.root, textvariable=self.var_doj, font=Theme.FONT_GOUDY, bg=Theme.BG_ENTRY
        ).place(x=850, y=190, width=180)

        # Email label
        Label(self.root, text="Email", font=Theme.FONT_GOUDY, bg=Theme.BG_WHITE).place(
            x=50, y=230
        )
        # Password label
        Label(self.root, text="Password", font=Theme.FONT_GOUDY, bg=Theme.BG_WHITE).place(
            x=350, y=230
        )
        # User Type label
        Label(self.root, text="User Type", font=Theme.FONT_GOUDY, bg=Theme.BG_WHITE).place(
            x=750, y=230
        )

        # Email entry
        Entry(
            self.root, textvariable=self.var_email, font=Theme.FONT_GOUDY, bg=Theme.BG_ENTRY
        ).place(x=150, y=230, width=180)
        # Password entry
        Entry(
            self.root, textvariable=self.var_pass, font=Theme.FONT_GOUDY, bg=Theme.BG_ENTRY
        ).place(x=500, y=230, width=180)
        # User Type combobox
        cmb_utype = ttk.Combobox(
            self.root,
            textvariable=self.var_utype,
            values=("Admin", "Employee"),
            state="readonly",
            justify="center",
            font=Theme.FONT_GOUDY,
        )
        cmb_utype.place(x=850, y=230, width=180)
        cmb_utype.current(0)

        # Address label
        Label(self.root, text="Address", font=Theme.FONT_GOUDY, bg=Theme.BG_WHITE).place(
            x=50, y=270
        )
        # Salary label
        Label(self.root, text="Salary", font=Theme.FONT_GOUDY, bg=Theme.BG_WHITE).place(
            x=500, y=270
        )

        # Address textbox
        self.txt_address = Text(self.root, font=Theme.FONT_GOUDY, bg=Theme.BG_ENTRY)
        self.txt_address.place(x=150, y=270, width=300, height=60)
        Entry(
            self.root,
            textvariable=self.var_salary,
            font=Theme.FONT_GOUDY,
            bg=Theme.BG_ENTRY,
        ).place(x=600, y=270, width=180)

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
                (500, 305, 110, 28),
                (620, 305, 110, 28),
                (740, 305, 110, 28),
                (860, 305, 110, 28),
            ],
        )

        # Columns
        cols = (
            "eid",
            "name",
            "email",
            "gender",
            "contact",
            "dob",
            "doj",
            "pass",
            "utype",
            "address",
            "salary",
        )
        # Headings
        headings = {
            "eid": "EMP ID",
            "name": "Name",
            "email": "Email",
            "gender": "Gender",
            "contact": "Contact",
            "dob": "D.O.B",
            "doj": "D.O.J",
            "pass": "Password",
            "utype": "User Type",
            "address": "Address",
            "salary": "Salary",
        }
        widths = {c: 100 for c in cols}
        widths["eid"] = 90
        # Employee table
        emp_frame, self.EmployeeTable = scrolled_treeview(
            self.root, cols, headings, widths
        )
        emp_frame.place(x=0, y=350, relwidth=1, height=150)
        self.EmployeeTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()

    # Add employee
    def add(self):
        ok, msg = employee_service.add_employee(
            self.var_emp_id.get(),
            self.var_name.get(),
            self.var_email.get(),
            self.var_gender.get(),
            self.var_contact.get(),
            self.var_dob.get(),
            self.var_doj.get(),
            self.var_pass.get(),
            self.var_utype.get(),
            self.txt_address.get("1.0", END),
            self.var_salary.get(),
        )
        if ok:
            messagebox.showinfo("Success", msg, parent=self.root)
            self.clear()
            self.show()
        else:
            messagebox.showerror("Error", msg, parent=self.root)

    # Show employees
    def show(self):
        try:
            rows = employee_service.fetch_all_employees()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    # Get employee data
    def get_data(self, ev):
        f = self.EmployeeTable.focus()
        content = self.EmployeeTable.item(f)
        row = content["values"]
        self.var_emp_id.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_contact.set(row[4])
        self.var_dob.set(row[5])
        self.var_doj.set(row[6])
        self.var_pass.set(row[7])
        self.var_utype.set(row[8])
        self.txt_address.delete("1.0", END)
        self.txt_address.insert(END, row[9])
        self.var_salary.set(row[10])

    # Update employee
    def update(self):
        ok, msg = employee_service.update_employee(
            self.var_emp_id.get(),
            self.var_name.get(),
            self.var_email.get(),
            self.var_gender.get(),
            self.var_contact.get(),
            self.var_dob.get(),
            self.var_doj.get(),
            self.var_pass.get(),
            self.var_utype.get(),
            self.txt_address.get("1.0", END),
            self.var_salary.get(),
        )
        if ok:
            messagebox.showinfo("Success", msg, parent=self.root)
            self.show()
        else:
            messagebox.showerror("Error", msg, parent=self.root)

    # Delete employee
    def delete(self):
        eid = self.var_emp_id.get()
        if not eid:
            messagebox.showerror("Error", "Employee ID must be required", parent=self.root)
            return
        if not employee_service.employee_exists(eid):
            messagebox.showerror("Error", "Invalid Employee ID", parent=self.root)
            return
        if not messagebox.askyesno(
            "Confirm", "Do you really want to delete?", parent=self.root
        ):
            return
        ok, msg = employee_service.delete_employee_row(eid)
        if ok:
            messagebox.showinfo("Delete", msg, parent=self.root)
            self.clear()
        else:
            messagebox.showerror("Error", msg, parent=self.root)

    # Clear employee data
    def clear(self):
        self.var_emp_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_doj.set("")
        self.var_pass.set("")
        self.var_utype.set("Admin")
        self.txt_address.delete("1.0", END)
        self.var_salary.set("")
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")
        self.show()

    # Search employees
    def search(self):
        rows, err = employee_service.search_employees(
            self.var_searchby.get(), self.var_searchtxt.get()
        )
        if err:
            messagebox.showerror("Error", err, parent=self.root)
            return
        self.EmployeeTable.delete(*self.EmployeeTable.get_children())
        for row in rows:
            self.EmployeeTable.insert("", END, values=row)


if __name__ == "__main__":
    root = Tk()
    employeeClass(root)
    root.mainloop()
