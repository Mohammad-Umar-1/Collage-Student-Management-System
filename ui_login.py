from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QFrame, QMessageBox
)
from PyQt5.QtCore import Qt
from auth import login


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.dashboard = None  # keep ref so it isn't garbage collected

        self.setWindowTitle("College Student Management System")
        self.showMaximized()
        self.setStyleSheet("background-color: #f4f6f8;")

        outer = QVBoxLayout(self)
        outer.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setStyleSheet("background-color: white; border: 1px solid #d1d5db;")
        card.setFixedWidth(380)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(45, 45, 45, 45)

        title = QLabel("COLLEGE CMS")
        title.setStyleSheet("font-size: 24pt; font-weight: bold; color: #111827;")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        subtitle = QLabel("Login to your account")
        subtitle.setStyleSheet("color: #6b7280;")
        subtitle.setAlignment(Qt.AlignCenter)
        card_layout.addSpacing(5)
        card_layout.addWidget(subtitle)
        card_layout.addSpacing(20)

        card_layout.addWidget(QLabel("Username"))
        self.username = QLineEdit()
        self.username.setFocus()
        card_layout.addWidget(self.username)

        card_layout.addWidget(QLabel("Password"))
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        card_layout.addWidget(self.password)
        card_layout.addSpacing(15)

        login_btn = QPushButton("Login")
        login_btn.setStyleSheet(
            "background-color: #2563eb; color: white; font-weight: bold; padding: 10px;"
        )
        login_btn.clicked.connect(self.handle_login)
        card_layout.addWidget(login_btn)

        exit_btn = QPushButton("Exit")
        exit_btn.setStyleSheet(
            "background-color: #dc2626; color: white; font-weight: bold; padding: 10px;"
        )
        exit_btn.clicked.connect(self.exit_app)
        card_layout.addWidget(exit_btn)

        outer.addWidget(card, alignment=Qt.AlignCenter)

        self.password.returnPressed.connect(self.handle_login)
        self.username.returnPressed.connect(self.handle_login)

    def handle_login(self):
        from ui_dashboard import DashboardWindow  # avoid circular import

        role = login(self.username.text(), self.password.text())
        if role:
            self.hide()
            self.dashboard = DashboardWindow(role, self)
            self.dashboard.show()
        else:
            QMessageBox.critical(self, "Login Failed", "Invalid credentials")

    def exit_app(self):
        reply = QMessageBox.question(
            self, "Exit", "Are you sure you want to exit the application?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.close()

    def show_login_again(self):
        self.showMaximized()
        self.raise_()
        self.activateWindow()