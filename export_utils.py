import pandas as pd
from tkinter import filedialog
from db import get_connection
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


# ================= DATA FETCH =================

def get_students_year(year):
    con = get_connection()
    df = pd.read_sql(
        "SELECT admission_no, name, gender, year, section, phone, email, address "
        "FROM students WHERE year=?",
        con,
        params=(year,)
    )
    con.close()
    return df


def get_students_with_marks(year):
    con = get_connection()
    query = """
    SELECT
        s.admission_no,
        s.name,
        s.year,
        s.section,
        m.semester,
        m.subject,
        m.unit1,
        m.unit2,
        m.final
    FROM students s
    LEFT JOIN marks m ON s.admission_no = m.admission_no
    WHERE s.year=?
    ORDER BY s.admission_no, m.semester, m.subject
    """
    df = pd.read_sql(query, con, params=(year,))
    con.close()
    return df


# ================= EXPORT HELPERS =================

def export_excel(df, default_name):
    path = filedialog.asksaveasfilename(
        title="Save Excel File",
        defaultextension=".xlsx",
        initialfile=default_name,
        filetypes=[("Excel Files", "*.xlsx")]
    )
    if not path:
        return
    df.to_excel(path, index=False)


def export_pdf(df, default_name, title):
    path = filedialog.asksaveasfilename(
        title="Save PDF File",
        defaultextension=".pdf",
        initialfile=default_name,
        filetypes=[("PDF Files", "*.pdf")]
    )
    if not path:
        return

    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, height - 40, title)

    y = height - 80
    c.setFont("Helvetica", 9)

    for _, row in df.iterrows():
        line = " | ".join(str(v) for v in row.values)
        if y < 40:
            c.showPage()
            y = height - 40
            c.setFont("Helvetica", 9)
        c.drawString(40, y, line[:120])
        y -= 14

    c.save()

def get_student_semester_marks(adm, semester):
    con = get_connection()
    query = """
    SELECT
        subject,
        unit1,
        unit2,
        final,
        ROUND(((unit1 + unit2 + final) / 200.0) * 100, 2) AS percentage
    FROM marks
    WHERE admission_no=? AND semester=?
    ORDER BY subject
    """
    df = pd.read_sql(query, con, params=(adm, semester))
    con.close()
    return df
