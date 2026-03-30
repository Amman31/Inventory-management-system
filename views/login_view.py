from __future__ import annotations

from tkinter import Label, Entry, Button, StringVar, messagebox

from components import Theme
from services.login_service import authenticate


class LoginView:
    def __init__(self, root, on_login):
        self.root = root
        self.on_login = on_login

        self.root.geometry("600x430+280+160")
        self.root.resizable(False, False)
        self.root.config(bg="white")

        self.var_email = StringVar()
        self.var_password = StringVar()

        # Set inventory management system label
        Label(
            self.root,
            text="Inventory Management System",
            font=("times new roman", 22, "bold"),
            bg="#010c48",
            fg="white",
            padx=10,
            pady=10,
        ).pack(side="top", fill="x")

        # Set login label
        Label(
            self.root,
            text="Login",
            font=("goudy old style", 28, "bold"),
            bg="white",
            fg="#0f4d7d",
        ).place(x=220, y=85)

        # Set email label
        Label(self.root, text="Email", font=Theme.FONT_GOUDY_BOLD, bg="white").place(
            x=120, y=160
        )
        # Set email entry
        Entry(
            self.root,
            textvariable=self.var_email,
            font=Theme.FONT_GOUDY,
            bg=Theme.BG_ENTRY,
        ).place(x=240, y=160, width=240, height=30)

        # Set password label
        Label(
            self.root,
            text="Password",
            font=Theme.FONT_GOUDY_BOLD,
            bg="white",
        ).place(x=95, y=210)
        # Set password entry
        Entry(
            self.root,
            textvariable=self.var_password,
            show="*",
            font=Theme.FONT_GOUDY,
            bg=Theme.BG_ENTRY,
        ).place(x=240, y=210, width=240, height=30)

        # Set login button
        Button(
            self.root,
            text="Login",
            command=self.login,
            font=("times new roman", 18, "bold"),
            bg="#2196f3",
            fg="white",
            cursor="hand2",
        ).place(x=240, y=300, width=120, height=40)

        # Set exit button
        Button(
            self.root,
            text="Exit",
            command=self.root.destroy,
            font=("times new roman", 18, "bold"),
            bg="gray",
            fg="white",
            cursor="hand2",
        ).place(x=370, y=300, width=110, height=40)

    # Login function
    def login(self):
        # Authenticate user
        ok, role, msg = authenticate(self.var_email.get(), self.var_password.get())
        if not ok:
            messagebox.showerror("Error", msg, parent=self.root)
            return
        if self.on_login:
            self.on_login(role)

