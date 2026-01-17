from tkinter import *
from tkinter import ttk, messagebox
from ui_scroll import ScrollablePage
from marks import (
    get_students_by_year,
    get_marks_for_student,
    save_mark,
    delete_mark
)


def open_marks_ui(role):
    win = Toplevel()
    win.title("Marks Management")
    win.state("zoomed")

    # ================= SCROLLABLE PAGE =================
    page = ScrollablePage(win)
    page.pack(fill=BOTH, expand=True)

    # ================= HEADER =================
    Label(
        page.content,
        text="Marks Management",
        font=("Segoe UI", 22, "bold"),
        fg="#111827",
        bg="#f4f6f8"
    ).pack(pady=20)

    body = Frame(page.content, bg="#f4f6f8")
    body.pack(fill=BOTH, expand=True, padx=30)

    # ================= LEFT PANEL =================
    left = Frame(body, bg="#f3f4f6", padx=20, pady=20, relief=RIDGE, bd=1)
    left.pack(side=LEFT, fill=Y)

    Label(left, text="Academic Filters",
          font=("Segoe UI", 15, "bold"),
          bg="#f3f4f6").pack(pady=10)

    Label(left, text="Year", bg="#f3f4f6").pack(anchor="w")
    year_cb = ttk.Combobox(left, values=[1, 2, 3, 4], state="readonly", width=18)
    year_cb.pack(pady=5)

    Label(left, text="Semester", bg="#f3f4f6").pack(anchor="w")
    sem_cb = ttk.Combobox(left, state="readonly", width=18)
    sem_cb.pack(pady=5)

    Label(left, text="Subject", bg="#f3f4f6").pack(anchor="w")
    subject_cb = ttk.Combobox(
        left,
        values=[f"Subject {i}" for i in range(1, 6)],
        state="readonly",
        width=18
    )
    subject_cb.pack(pady=5)

    ttk.Separator(left).pack(fill=X, pady=15)

    Label(left, text="Students",
          font=("Segoe UI", 14, "bold"),
          bg="#f3f4f6").pack(pady=10)

    student_table = ttk.Treeview(
        left,
        columns=("adm", "name"),
        show="headings",
        height=15
    )
    student_table.heading("adm", text="Admission No")
    student_table.heading("name", text="Name")
    student_table.pack()

    # ================= RIGHT PANEL =================
    right = Frame(body, bg="#f4f6f8", padx=30)
    right.pack(side=LEFT, fill=BOTH, expand=True)

    info = StringVar()
    Label(right, textvariable=info,
          font=("Segoe UI", 13),
          bg="#f4f6f8").pack(pady=5)

    semester_percent = StringVar(value="Semester Percentage: --")

    Label(
        right,
        textvariable=semester_percent,
        font=("Segoe UI", 16, "bold"),
        fg="#2563eb",
        bg="#f4f6f8"
    ).pack(pady=10)

    # ================= FORM =================
    form = Frame(right, bg="white", padx=25, pady=25, relief=RIDGE, bd=1)
    form.pack(pady=20)

    Label(form, text="Unit 1 ( /50 )", bg="white").grid(row=0, column=0, pady=6)
    Label(form, text="Unit 2 ( /50 )", bg="white").grid(row=1, column=0, pady=6)
    Label(form, text="Final ( /100 )", bg="white").grid(row=2, column=0, pady=6)

    u1 = Entry(form, width=12)
    u2 = Entry(form, width=12)
    final = Entry(form, width=12)

    u1.grid(row=0, column=1, padx=10)
    u2.grid(row=1, column=1, padx=10)
    final.grid(row=2, column=1, padx=10)

    # ================= BUTTONS =================
    Button(
        right, text="Save / Update",
        bg="#2563eb", fg="white",
        font=("Segoe UI", 11, "bold"),
        width=18, relief=FLAT,
        command=lambda: save_marks()
    ).pack(pady=5)

    Button(
        right, text="Delete Marks",
        bg="#dc2626", fg="white",
        font=("Segoe UI", 11, "bold"),
        width=18, relief=FLAT,
        command=lambda: delete_marks()
    ).pack(pady=5)

    ttk.Separator(right).pack(fill=X, pady=20)

    # ================= SAVED MARKS TABLE =================
    Label(right, text="Saved Marks",
          font=("Segoe UI", 15, "bold"),
          bg="#f4f6f8").pack(pady=10)

    marks_card = Frame(right, bg="white", padx=15, pady=15, relief=RIDGE, bd=1)
    marks_card.pack(fill=X)

    marks_table = ttk.Treeview(
        marks_card,
        columns=("subject", "u1", "u2", "final"),
        show="headings",
        height=8
    )

    for c in ("subject", "u1", "u2", "final"):
        marks_table.heading(c, text=c.upper())
        marks_table.column(c, anchor="center", width=140)

    marks_table.pack(fill=X)

    # ================= STATE =================
    selected = {"adm": None}

    # ================= HELPERS =================
    def valid(val, maxv):
        try:
            v = float(val)
            if 0 <= v <= maxv:
                return round(v, 2)
        except:
            pass
        return None

    def subject_percent(a, b, c):
        return ((a + b + c) / 200) * 100

    # ================= LOGIC =================
    def update_semesters(event):
        sem_cb["values"] = {
            1: [1, 2],
            2: [3, 4],
            3: [5, 6],
            4: [7, 8]
        }[int(year_cb.get())]

    def load_students():
        student_table.delete(*student_table.get_children())
        for adm, name in get_students_by_year(int(year_cb.get())):
            student_table.insert("", END, values=(adm, name))

    def load_saved_marks(adm):
        marks_table.delete(*marks_table.get_children())
        rows = get_marks_for_student(adm, int(sem_cb.get()))

        for s, a, b, c in rows:
            marks_table.insert("", END, values=(s, a, b, c))

        if len(rows) == 5:
            total = sum(subject_percent(a, b, c) for _, a, b, c in rows)
            semester_percent.set(f"Semester Percentage: {round(total / 5, 2)}%")
        else:
            semester_percent.set("Semester Percentage: -- (Add all 5 subjects)")

    def select_student(event):
        sel = student_table.focus()
        if not sel:
            return
        adm, name = student_table.item(sel)["values"]
        selected["adm"] = adm
        info.set(f"{name}  |  Admission No: {adm}")
        load_saved_marks(adm)

    def select_mark(event):
        sel = marks_table.focus()
        if not sel:
            return
        s, a, b, c = marks_table.item(sel)["values"]
        subject_cb.set(s)
        u1.delete(0, END)
        u2.delete(0, END)
        final.delete(0, END)
        u1.insert(0, a)
        u2.insert(0, b)
        final.insert(0, c)

    def save_marks():
        if not selected["adm"]:
            messagebox.showerror("Error", "Select a student")
            return

        a = valid(u1.get(), 50)
        b = valid(u2.get(), 50)
        c = valid(final.get(), 100)

        if None in (a, b, c):
            messagebox.showerror(
                "Invalid Marks",
                "Unit 1 & 2: 0–50\nFinal: 0–100\nUp to 2 decimals"
            )
            return

        save_mark(
            selected["adm"],
            subject_cb.get(),
            int(sem_cb.get()),
            a, b, c
        )

        load_saved_marks(selected["adm"])

    def delete_marks():
        if not selected["adm"]:
            return
        delete_mark(
            selected["adm"],
            subject_cb.get(),
            int(sem_cb.get())
        )
        load_saved_marks(selected["adm"])

    # ================= EVENTS =================
    year_cb.bind("<<ComboboxSelected>>", update_semesters)
    sem_cb.bind("<<ComboboxSelected>>", lambda e: load_students())
    student_table.bind("<<TreeviewSelect>>", select_student)
    marks_table.bind("<<TreeviewSelect>>", select_mark)
