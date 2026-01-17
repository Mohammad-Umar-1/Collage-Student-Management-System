from db import get_connection


def login(username, password):
    con = get_connection()
    cur = con.cursor()
    cur.execute(
        "SELECT role FROM users WHERE username=? AND password=?",
        (username, password)
    )
    row = cur.fetchone()
    con.close()
    return row[0] if row else None


def create_user(username, password, role):
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute(
            "INSERT INTO users(username,password,role) VALUES (?,?,?)",
            (username, password, role)
        )
        con.commit()
        return True
    except:
        return False
    finally:
        con.close()
