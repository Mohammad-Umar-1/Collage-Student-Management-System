from tkinter import ttk

def apply_style(root):
    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure(
        "TButton",
        font=("Segoe UI", 11),
        padding=8
    )

    style.configure(
        "Treeview",
        font=("Segoe UI", 10),
        rowheight=28
    )

    style.configure(
        "Treeview.Heading",
        font=("Segoe UI", 11, "bold")
    )

    style.configure(
        "TLabel",
        font=("Segoe UI", 11)
    )
