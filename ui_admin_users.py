from tkinter import *
from tkinter import ttk, messagebox
from db import get_connection
from auth import create_user


def open_user_management():
    win = Toplevel()
    win.title("Teacher Account Management")
    win.state("zoomed")
    win.configure(bg="#f4f6f8")

    # ================= SCROLLABLE CONTAINER =================
    canvas = Canvas(win, bg="#f4f6f8", highlightthickness=0)
    scrollbar = ttk.Scrollbar(win, orient=VERTICAL, command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    content = Frame(canvas, bg="#f4f6f8")
    canvas.create_window((0, 0), window=content, anchor="nw")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    content.bind("<Configure>", on_configure)

    def on_mousewheel(event):
        canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    canvas.bind_all("<MouseWheel>", on_mousewheel)

    # ================= HEADER =================
    Label(
        content,
        text="Teacher Account Management",
        font=("Segoe UI", 22, "bold"),
        bg="#f4f6f8",
        fg="#111827"
    ).pack(pady=(20, 5))

    Label(
        content,
        text="Create, update, and remove teacher login access",
        font=("Segoe UI", 11),
        bg="#f4f6f8",
        fg="#6b7280"
    ).pack(pady=(0, 25))

    # ================= MAIN CONTAINER =================
    container = Frame(content, bg="#f4f6f8")
    container.pack(fill=BOTH, expand=True, padx=60)

    # =================================================
    # LEFT CARD — CREATE / UPDATE
    # =================================================
    left = Frame(container, bg="white", padx=30, pady=30, relief=RIDGE, bd=1)
    left.pack(side=LEFT, fill=Y, padx=(0, 30))

    Label(
        left,
        text="Create / Update Teacher",
        font=("Segoe UI", 16, "bold"),
        bg="white"
    ).pack(pady=(0, 20))

    Label(left, text="Username", bg="white").pack(anchor="w")
    username = Entry(left, width=28)
    username.pack(pady=5)

    Label(left, text="Password", bg="white").pack(anchor="w")
    password = Entry(left, width=28, show="*")
    password.pack(pady=5)

    selected_id = {"id": None}

    def clear_form():
        username.delete(0, END)
        password.delete(0, END)
        selected_id["id"] = None

    def create_teacher():
        if not username.get() or not password.get():
            messagebox.showerror("Error", "All fields required")
            return

        if create_user(username.get(), password.get(), "teacher"):
            messagebox.showinfo("Success", "Teacher created")
            clear_form()
            load_teachers()
        else:
            messagebox.showerror("Error", "Username already exists")

    def update_teacher():
        if not selected_id["id"]:
            messagebox.showerror("Error", "Select a teacher to update")
            return

        if not password.get():
            messagebox.showerror("Error", "Enter new password")
            return

        con = get_connection()
        cur = con.cursor()
        cur.execute(
            "UPDATE users SET password=? WHERE id=?",
            (password.get(), selected_id["id"])
        )
        con.commit()
        con.close()

        messagebox.showinfo("Updated", "Password updated")
        clear_form()
        load_teachers()

    Button(
        left,
        text="Create Teacher",
        bg="#16a34a",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        width=20,
        relief=FLAT,
        command=create_teacher
    ).pack(pady=(15, 5))

    Button(
        left,
        text="Update Password",
        bg="#2563eb",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        width=20,
        relief=FLAT,
        command=update_teacher
    ).pack(pady=5)

    # =================================================
    # RIGHT CARD — TEACHER LIST
    # =================================================
    right = Frame(container, bg="white", padx=30, pady=30, relief=RIDGE, bd=1)
    right.pack(side=LEFT, fill=BOTH, expand=True)

    Label(
        right,
        text="Existing Teachers",
        font=("Segoe UI", 16, "bold"),
        bg="white"
    ).pack(pady=(0, 15))

    table = ttk.Treeview(
        right,
        columns=("id", "username"),
        show="headings",
        height=15
    )
    table.heading("id", text="ID")
    table.heading("username", text="USERNAME")
    table.column("id", width=80, anchor="center")
    table.column("username", width=250, anchor="center")
    table.pack(fill=BOTH, expand=True)

    def load_teachers():
        table.delete(*table.get_children())
        con = get_connection()
        cur = con.cursor()
        cur.execute("SELECT id, username FROM users WHERE role='teacher'")
        for row in cur.fetchall():
            table.insert("", END, values=row)
        con.close()

    def on_select(event):
        sel = table.focus()
        if not sel:
            return
        uid, uname = table.item(sel)["values"]
        selected_id["id"] = uid
        username.delete(0, END)
        username.insert(0, uname)
        password.delete(0, END)

    def delete_teacher():
        if not selected_id["id"]:
            messagebox.showerror("Error", "Select a teacher to delete")
            return

        if not messagebox.askyesno("Confirm", "Delete this teacher account?"):
            return

        con = get_connection()
        cur = con.cursor()
        cur.execute("DELETE FROM users WHERE id=?", (selected_id["id"],))
        con.commit()
        con.close()

        messagebox.showinfo("Deleted", "Teacher deleted")
        clear_form()
        load_teachers()

    table.bind("<<TreeviewSelect>>", on_select)

    Button(
        right,
        text="Delete Selected Teacher",
        bg="#dc2626",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        width=25,
        relief=FLAT,
        command=delete_teacher
    ).pack(pady=15)

    load_teachers()
