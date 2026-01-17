import sqlite3

DB_NAME = "college.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    con = get_connection()
    cur = con.cursor()

    # ---------- USERS ----------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    # ---------- STUDENTS ----------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        admission_no TEXT PRIMARY KEY,
        name TEXT,
        gender TEXT,
        address TEXT,
        phone TEXT,
        email TEXT,
        year INTEGER,
        section TEXT
    )
    """)

    # ---------- MARKS (FIXED & SUBJECT-WISE) ----------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS marks (
        admission_no TEXT,
        subject TEXT,
        semester INTEGER,
        unit1 INTEGER,
        unit2 INTEGER,
        final INTEGER,
        PRIMARY KEY (admission_no, subject, semester)
    )
    """)

    # ---------- DEFAULT ADMIN ----------
    cur.execute("SELECT * FROM users WHERE username='admin'")
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO users VALUES (NULL, ?, ?, ?)",
            ("admin", "admin123", "admin")
        )

    con.commit()
    con.close()
