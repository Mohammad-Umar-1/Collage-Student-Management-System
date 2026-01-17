from tkinter import *
from tkinter import messagebox
from auth import login


def start_login(root):
    from ui_dashboard import open_dashboard  # ✅ moved here

    root.title("College Student Management System")
    root.state("zoomed")
    root.configure(bg="#f4f6f8")

    card = Frame(root, bg="white", padx=45, pady=45, relief=RIDGE, bd=1)
    card.place(relx=0.5, rely=0.5, anchor=CENTER)

    Label(card, text="COLLEGE CMS",
          font=("Segoe UI", 24, "bold"),
          fg="#111827", bg="white").pack(pady=(0, 5))

    Label(card, text="Login to your account",
          font=("Segoe UI", 11),
          fg="#6b7280", bg="white").pack(pady=(0, 25))

    Label(card, text="Username",
          font=("Segoe UI", 11, "bold"),
          bg="white").pack(anchor="w")

    username = Entry(card, font=("Segoe UI", 11), width=32)
    username.pack(pady=(6, 15))
    username.focus()

    Label(card, text="Password",
          font=("Segoe UI", 11, "bold"),
          bg="white").pack(anchor="w")

    password = Entry(card, show="*", font=("Segoe UI", 11), width=32)
    password.pack(pady=(6, 20))

    def handle_login():
        role = login(username.get(), password.get())
        if role:
            root.withdraw()
            open_dashboard(root, role)
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    Button(card, text="Login",
           font=("Segoe UI", 12, "bold"),
           bg="#2563eb", fg="white",
           relief=FLAT, height=2,
           command=handle_login).pack(fill=X)

    root.bind("<Return>", lambda e: handle_login())
    def exit_app():
        if messagebox.askyesno("Exit", "Are you sure you want to exit the application?"):
            root.destroy()
    Button(
        card,
        text="Exit",
        font=("Segoe UI", 11, "bold"),
        bg="#dc2626",
        fg="white",
        relief=FLAT,
        height=2,
        command=exit_app
    ).pack(fill=X, pady=(0, 10))


def show_login_again(root):
    root.deiconify()
    root.state("zoomed")
    root.lift()            # bring to front
    root.focus_force()
