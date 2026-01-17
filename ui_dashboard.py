from tkinter import *
from tkinter import messagebox
from ui_student import open_student_ui
from ui_marks import open_marks_ui
from ui_admin_users import open_user_management
from ui_login import show_login_again

# ================= THEME =================
BG_APP = "#f4f6f8"
BG_SIDEBAR = "#111827"
BG_SIDEBAR_BTN = "#1f2937"
BG_SIDEBAR_BTN_HOVER = "#374151"
ACCENT = "#2563eb"


def open_dashboard(parent, role):
    dashboard = Toplevel(parent)
    dashboard.title("College Management System")
    dashboard.state("zoomed")
    dashboard.configure(bg=BG_APP)

    # ================= SIDEBAR =================
    sidebar = Frame(dashboard, bg=BG_SIDEBAR, width=260)
    sidebar.pack(side=LEFT, fill=Y)
    sidebar.pack_propagate(False)

    # ---- LOGO / TITLE ----
    Label(
        sidebar,
        text="COLLEGE CMS",
        fg="white",
        bg=BG_SIDEBAR,
        font=("Segoe UI", 20, "bold")
    ).pack(pady=(30, 5))

    Label(
        sidebar,
        text=f"Logged in as: {role.capitalize()}",
        fg="#9ca3af",
        bg=BG_SIDEBAR,
        font=("Segoe UI", 10)
    ).pack(pady=(0, 30))

    # ---- NAV BUTTON FACTORY ----
    def nav_button(text, command):
        btn = Button(
            sidebar,
            text=text,
            bg=BG_SIDEBAR_BTN,
            fg="white",
            font=("Segoe UI", 11),
            relief=FLAT,
            height=2,
            anchor="w",
            padx=20,
            command=command
        )
        btn.pack(fill=X, padx=15, pady=6)

        btn.bind("<Enter>", lambda e: btn.config(bg=BG_SIDEBAR_BTN_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=BG_SIDEBAR_BTN))
        return btn

    # ---- ADMIN OPTIONS ----
    if role == "admin":
        nav_button("Students", lambda: open_student_ui(role))
        nav_button("Teachers / Users", open_user_management)

    # ---- COMMON OPTIONS ----
    nav_button("Marks", lambda: open_marks_ui(role))

    # ---- SPACER ----
    Frame(sidebar, bg=BG_SIDEBAR).pack(expand=True, fill=BOTH)

    # ---- LOGOUT (CORRECT WAY) ----
    def logout():
        if messagebox.askyesno("Logout", "Do you want to logout?"):
            dashboard.destroy()       # close dashboard only
            show_login_again(parent) # show login again

    Button(
        sidebar,
        text="Logout",
        bg="#dc2626",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        relief=FLAT,
        height=2,
        command=logout
    ).pack(fill=X, padx=20, pady=20)

    # ================= MAIN CONTENT =================
    content = Frame(dashboard, bg=BG_APP, padx=50, pady=40)
    content.pack(fill=BOTH, expand=True)

    # ---- WELCOME CARD ----
    welcome_card = Frame(
        content,
        bg="white",
        padx=40,
        pady=30,
        relief=RIDGE,
        bd=1
    )
    welcome_card.pack(anchor="nw", pady=20)

    Label(
        welcome_card,
        text=f"Welcome, {role.capitalize()} 👋",
        font=("Segoe UI", 26, "bold"),
        fg="#111827",
        bg="white"
    ).pack(anchor="w")

    Label(
        welcome_card,
        text="Use the menu on the left to manage students, users, and marks.",
        font=("Segoe UI", 12),
        fg="#6b7280",
        bg="white"
    ).pack(anchor="w", pady=(10, 0))

