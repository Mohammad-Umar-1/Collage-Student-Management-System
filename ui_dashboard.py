from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QMessageBox
)
from PyQt5.QtCore import Qt

BG_APP = "#f4f6f8"
BG_SIDEBAR = "#111827"
BG_SIDEBAR_BTN = "#1f2937"
BG_SIDEBAR_BTN_HOVER = "#374151"
ACCENT = "#2563eb"


class DashboardWindow(QWidget):
    def __init__(self, role, login_window):
        super().__init__()
        self.role = role
        self.login_window = login_window
        self.child_windows = []  # keep refs to opened sub-windows

        self.setWindowTitle("College Management System")
        self.showMaximized()
        self.setStyleSheet(f"background-color: {BG_APP};")

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ================= SIDEBAR =================
        sidebar = QFrame()
        sidebar.setFixedWidth(260)
        sidebar.setStyleSheet(f"background-color: {BG_SIDEBAR};")
        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(15, 30, 15, 20)

        logo = QLabel("COLLEGE CMS")
        logo.setStyleSheet("color: white; font-size: 20pt; font-weight: bold;")
        logo.setAlignment(Qt.AlignCenter)
        side_layout.addWidget(logo)

        user_label = QLabel(f"Logged in as: {role.capitalize()}")
        user_label.setStyleSheet("color: #9ca3af; font-size: 10pt;")
        user_label.setAlignment(Qt.AlignCenter)
        side_layout.addWidget(user_label)
        side_layout.addSpacing(20)

        if role == "admin":
            side_layout.addWidget(self._nav_button("Students", self.open_students))
            side_layout.addWidget(self._nav_button("Teachers / Users", self.open_user_management))

        side_layout.addWidget(self._nav_button("Marks", self.open_marks))

        side_layout.addStretch()

        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet(
            "background-color: #dc2626; color: white; font-weight: bold; padding: 10px;"
        )
        logout_btn.clicked.connect(self.logout)
        side_layout.addWidget(logout_btn)

        root.addWidget(sidebar)

        # ================= MAIN CONTENT =================
        content = QFrame()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(50, 40, 50, 40)
        content_layout.setAlignment(Qt.AlignTop)

        welcome_card = QFrame()
        welcome_card.setStyleSheet("background-color: white; border: 1px solid #d1d5db;")
        wc_layout = QVBoxLayout(welcome_card)
        wc_layout.setContentsMargins(40, 30, 40, 30)

        welcome_title = QLabel(f"Welcome, {role.capitalize()}")
        welcome_title.setStyleSheet("font-size: 26pt; font-weight: bold; color: #111827;")
        wc_layout.addWidget(welcome_title)

        welcome_sub = QLabel("Use the menu on the left to manage students, users, and marks.")
        welcome_sub.setStyleSheet("font-size: 12pt; color: #6b7280;")
        wc_layout.addWidget(welcome_sub)

        content_layout.addWidget(welcome_card, alignment=Qt.AlignLeft)
        root.addWidget(content, stretch=1)

    def _nav_button(self, text, handler):
        btn = QPushButton(text)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {BG_SIDEBAR_BTN};
                color: white;
                text-align: left;
                padding: 12px 20px;
                font-size: 11pt;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {BG_SIDEBAR_BTN_HOVER};
            }}
        """)
        btn.clicked.connect(handler)
        return btn

    def open_students(self):
        from ui_student import StudentWindow
        w = StudentWindow(self.role)
        w.show()
        self.child_windows.append(w)

    def open_marks(self):
        from ui_marks import MarksWindow
        w = MarksWindow(self.role)
        w.show()
        self.child_windows.append(w)

    def open_user_management(self):
        from ui_admin_users import UserManagementWindow
        w = UserManagementWindow()
        w.show()
        self.child_windows.append(w)

    def logout(self):
        reply = QMessageBox.question(
            self, "Logout", "Do you want to logout?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.close()
            self.login_window.show_login_again()