import sys
from PyQt5.QtWidgets import QApplication
from db import init_db
from ui_style import apply_style
from ui_login import LoginWindow


def main():
    app = QApplication(sys.argv)
    apply_style(app)

    init_db()  # tables + default admin

    login_win = LoginWindow()
    login_win.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()