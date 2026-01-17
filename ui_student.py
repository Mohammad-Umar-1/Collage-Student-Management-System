from tkinter import *
from tkinter import ttk, messagebox
from student import add_student, update_student, delete_student, get_all_students
from ui_scroll import ScrollablePage
from export_utils import (
    get_students_year,
    get_students_with_marks,
    export_excel,
    export_pdf
)


def open_student_ui(role):
    win = Toplevel()
    win.title("Student Management")
    win.state("zoomed")

    page = ScrollablePage(win)
    page.pack(fill=BOTH, expand=True)

    # ================= HEADER =================
    Label(
        page.content,
        text="Student Management",
        font=("Segoe UI", 22, "bold"),
        bg="#f4f6f8"
    ).pack(pady=20)

    # ================= FORM =================
    form = Frame(page.content, bg="white", padx=30, pady=30, relief=RIDGE, bd=1)
    form.pack(fill=X, padx=60)

    fields = [
        "Admission No", "Name", "Gender", "Year",
        "Section", "Phone", "Email", "Address"
    ]
    entries = {}

    for i, f in enumerate(fields):
        Label(form, text=f, bg="white").grid(row=i, column=0, sticky="w", pady=6)

        if f == "Gender":
            e = ttk.Combobox(form, values=["Male", "Female"], state="readonly")
        elif f == "Year":
            e = ttk.Combobox(form, values=[1, 2, 3, 4], state="readonly")
        else:
            e = Entry(form)

        e.grid(row=i, column=1, padx=10, pady=6)
        entries[f] = e

    # ================= BUTTONS =================
    btns = Frame(page.content, bg="#f4f6f8")
    btns.pack(pady=15)

    def save():
        add_student(
            entries["Admission No"].get(),
            entries["Name"].get(),
            entries["Gender"].get(),
            int(entries["Year"].get()),
            entries["Section"].get(),
            entries["Phone"].get(),
            entries["Email"].get(),
            entries["Address"].get()
        )
        load_students()
        clear()

    def update():
        update_student(
            entries["Admission No"].get(),
            entries["Name"].get(),
            entries["Gender"].get(),
            int(entries["Year"].get()),
            entries["Section"].get(),
            entries["Phone"].get(),
            entries["Email"].get(),
            entries["Address"].get()
        )
        load_students()

    def delete():
        if messagebox.askyesno("Confirm", "Delete student?"):
            delete_student(entries["Admission No"].get())
            load_students()
            clear()

    Button(btns, text="Add", bg="#16a34a", fg="white", width=14, command=save).grid(row=0, column=0, padx=8)
    Button(btns, text="Update", bg="#2563eb", fg="white", width=14, command=update).grid(row=0, column=1, padx=8)
    Button(btns, text="Delete", bg="#dc2626", fg="white", width=14, command=delete).grid(row=0, column=2, padx=8)

    # ================= EXPORT =================
    export_bar = Frame(page.content, bg="white", padx=20, pady=20, relief=RIDGE, bd=1)
    export_bar.pack(fill=X, padx=60, pady=20)

    Label(export_bar, text="Export (Year-wise)", font=("Segoe UI", 14, "bold"), bg="white").grid(row=0, columnspan=4, sticky="w")

    year_cb = ttk.Combobox(export_bar, values=[1, 2, 3, 4], state="readonly")
    year_cb.grid(row=1, column=0, padx=10)


    def export_students_excel():
        if not year_cb.get():
            messagebox.showerror("Error", "Select year")
            return
        df = get_students_year(year_cb.get())
        export_excel(df, f"students_year_{year_cb.get()}")

    def export_students_pdf():
        if not year_cb.get():
            messagebox.showerror("Error", "Select year")
            return
        df = get_students_year(year_cb.get())
        export_pdf(df, f"students_year_{year_cb.get()}", "Student List")

    def export_marks_excel():
        if not year_cb.get():
            messagebox.showerror("Error", "Select year")
            return
        df = get_students_with_marks(year_cb.get())
        export_excel(df, f"students_marks_year_{year_cb.get()}")

    def export_marks_pdf():
        if not year_cb.get():
            messagebox.showerror("Error", "Select year")
            return
        df = get_students_with_marks(year_cb.get())
        export_pdf(df, f"students_marks_year_{year_cb.get()}", "Student Marks")
        if not year_cb.get():
            messagebox.showerror("Error", "Select year")
            return
        df = get_students_year(year_cb.get())
        export_excel(df, f"students_year_{year_cb.get()}")

    def export_students_pdf():
        if not year_cb.get():
            messagebox.showerror("Error", "Select year")
            return
        df = get_students_year(year_cb.get())
        export_pdf(df, f"students_year_{year_cb.get()}", "Student List")

    def export_marks_excel():
        if not year_cb.get():
            messagebox.showerror("Error", "Select year")
            return
        df = get_students_with_marks(year_cb.get())
        export_excel(df, f"students_marks_year_{year_cb.get()}")

    def export_marks_pdf():
        if not year_cb.get():
            messagebox.showerror("Error", "Select year")
            return
        df = get_students_with_marks(year_cb.get())
        export_pdf(df, f"students_marks_year_{year_cb.get()}", "Student Marks")
    Button(export_bar, text="Students → Excel", command=export_students_excel).grid(row=1, column=1, padx=10)
    Button(export_bar, text="Students → PDF", command=export_students_pdf).grid(row=1, column=2, padx=10)
    Button(export_bar, text="Marks → Excel", command=export_marks_excel).grid(row=2, column=1, padx=10, pady=5)
    Button(export_bar, text="Marks → PDF", command=export_marks_pdf).grid(row=2, column=2, padx=10, pady=5)

    # ================= TABLE =================
    table = ttk.Treeview(
        page.content,
        columns=fields,
        show="headings",
        height=12
    )
    for f in fields:
        table.heading(f, text=f.upper())
        table.column(f, width=140, anchor="center")

    table.pack(fill=BOTH, expand=True, padx=60, pady=20)

    def load_students():
        table.delete(*table.get_children())
        for row in get_all_students():
            table.insert("", END, values=row)

    def clear():
        for e in entries.values():
            e.delete(0, END)

    def select_row(event):
        sel = table.focus()
        if not sel:
            return
        vals = table.item(sel)["values"]
        for i, k in enumerate(entries):
            entries[k].delete(0, END)
            entries[k].insert(0, vals[i])

    table.bind("<<TreeviewSelect>>", select_row)

    load_students()
