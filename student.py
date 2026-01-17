from db import get_connection


def add_student(adm, name, gender, year, section, phone, email, address):
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        INSERT INTO students
        (admission_no, name, gender, year, section, phone, email, address)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (adm, name, gender, year, section, phone, email, address))
    con.commit()
    con.close()


def update_student(adm, name, gender, year, section, phone, email, address):
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        UPDATE students SET
            name=?, gender=?, year=?, section=?, phone=?, email=?, address=?
        WHERE admission_no=?
    """, (name, gender, year, section, phone, email, address, adm))
    con.commit()
    con.close()


def delete_student(adm):
    con = get_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM students WHERE admission_no=?", (adm,))
    con.commit()
    con.close()


def get_all_students():
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        SELECT admission_no, name, gender, year, section, phone, email, address
        FROM students
        ORDER BY year, section
    """)
    rows = cur.fetchall()
    con.close()
    return rows
