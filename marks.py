from db import get_connection


def get_students_by_year(year):
    con = get_connection()
    cur = con.cursor()
    cur.execute(
        "SELECT admission_no, name FROM students WHERE year=?",
        (year,)
    )
    data = cur.fetchall()
    con.close()
    return data


def get_mark(adm, subject, sem):
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        SELECT unit1, unit2, final
        FROM marks
        WHERE admission_no=? AND subject=? AND semester=?
    """, (adm, subject, sem))
    row = cur.fetchone()
    con.close()
    return row


def save_mark(adm, subject, sem, u1, u2, final):
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        INSERT INTO marks(admission_no, subject, semester, unit1, unit2, final)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(admission_no, subject, semester)
        DO UPDATE SET
            unit1=excluded.unit1,
            unit2=excluded.unit2,
            final=excluded.final
    """, (adm, subject, sem, u1, u2, final))
    con.commit()
    con.close()


def delete_mark(adm, subject, sem):
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        DELETE FROM marks
        WHERE admission_no=? AND subject=? AND semester=?
    """, (adm, subject, sem))
    con.commit()
    con.close()
def get_marks_for_student(adm, sem):
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        SELECT subject, unit1, unit2, final
        FROM marks
        WHERE admission_no=? AND semester=?
    """, (adm, sem))
    data = cur.fetchall()
    con.close()
    return data
