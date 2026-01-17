from db import get_connection

def add_subject(year, semester, subject_name):
    con = get_connection()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO subjects (year, semester, subject_name) VALUES (?,?,?)",
        (year, semester, subject_name)
    )
    con.commit()
    con.close()

def get_subjects(year, semester):
    con = get_connection()
    cur = con.cursor()
    cur.execute(
        "SELECT id, subject_name FROM subjects WHERE year=? AND semester=?",
        (year, semester)
    )
    rows = cur.fetchall()
    con.close()
    return rows