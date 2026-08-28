from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QTableWidget, QTableWidgetItem, QMessageBox, QScrollArea,
    QHeaderView
)
from PyQt5.QtCore import Qt
from db import get_connection
from auth import create_user


class UserManagementWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_id = None
        self.setWindowTitle("Teacher Account Management")
        self.showMaximized()
        self.setStyleSheet("background-color: #f4f6f8;")

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

        page = QWidget()
        scroll.setWidget(page)
        layout = QVBoxLayout(page)
        layout.setContentsMargins(60, 20, 60, 20)

        header = QLabel("Teacher Account Management")
        header.setStyleSheet("font-size: 22pt; font-weight: bold; color: #111827;")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        sub = QLabel("Create, update, and remove teacher login access")
        sub.setStyleSheet("font-size: 11pt; color: #6b7280;")
        sub.setAlignment(Qt.AlignCenter)
        layout.addWidget(sub)

        container = QHBoxLayout()
        layout.addLayout(container)

        # ================= LEFT CARD =================
        left = QFrame()
        left.setStyleSheet("background-color: white; border: 1px solid #d1d5db;")
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(30, 30, 30, 30)

        left_title = QLabel("Create / Update Teacher")
        left_title.setStyleSheet("font-size: 16pt; font-weight: bold;")
        left_layout.addWidget(left_title)

        left_layout.addWidget(QLabel("Username"))
        self.username = QLineEdit()
        left_layout.addWidget(self.username)

        left_layout.addWidget(QLabel("Password"))
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        left_layout.addWidget(self.password)

        create_btn = QPushButton("Create Teacher")
        create_btn.setStyleSheet("background-color: #16a34a; color: white; font-weight: bold;")
        create_btn.clicked.connect(self.create_teacher)
        left_layout.addWidget(create_btn)

        update_btn = QPushButton("Update Password")
        update_btn.setStyleSheet("background-color: #2563eb; color: white; font-weight: bold;")
        update_btn.clicked.connect(self.update_teacher)
        left_layout.addWidget(update_btn)

        left_layout.addStretch()
        container.addWidget(left)

        # ================= RIGHT CARD =================
        right = QFrame()
        right.setStyleSheet("background-color: white; border: 1px solid #d1d5db;")
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(30, 30, 30, 30)

        right_title = QLabel("Existing Teachers")
        right_title.setStyleSheet("font-size: 16pt; font-weight: bold;")
        right_layout.addWidget(right_title)

        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["ID", "USERNAME"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.itemSelectionChanged.connect(self.on_select)
        right_layout.addWidget(self.table)

        delete_btn = QPushButton("Delete Selected Teacher")
        delete_btn.setStyleSheet("background-color: #dc2626; color: white; font-weight: bold;")
        delete_btn.clicked.connect(self.delete_teacher)
        right_layout.addWidget(delete_btn)

        container.addWidget(right, stretch=1)

        self.load_teachers()

    def clear_form(self):
        self.username.clear()
        self.password.clear()
        self.selected_id = None

    def create_teacher(self):
        if not self.username.text() or not self.password.text():
            QMessageBox.critical(self, "Error", "All fields required")
            return

        if create_user(self.username.text(), self.password.text(), "teacher"):
            QMessageBox.information(self, "Success", "Teacher created")
            self.clear_form()
            self.load_teachers()
        else:
            QMessageBox.critical(self, "Error", "Username already exists")

    def update_teacher(self):
        if not self.selected_id:
            QMessageBox.critical(self, "Error", "Select a teacher to update")
            return

        if not self.password.text():
            QMessageBox.critical(self, "Error", "Enter new password")
            return

        con = get_connection()
        cur = con.cursor()
        cur.execute(
            "UPDATE users SET password=? WHERE id=?",
            (self.password.text(), self.selected_id)
        )
        con.commit()
        con.close()

        QMessageBox.information(self, "Updated", "Password updated")
        self.clear_form()
        self.load_teachers()

    def load_teachers(self):
        self.table.setRowCount(0)
        con = get_connection()
        cur = con.cursor()
        cur.execute("SELECT id, username FROM users WHERE role='teacher'")
        for row in cur.fetchall():
            r = self.table.rowCount()
            self.table.insertRow(r)
            for c, val in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(val)))
        con.close()

    def on_select(self):
        row = self.table.currentRow()
        if row < 0:
            return
        uid = self.table.item(row, 0).text()
        uname = self.table.item(row, 1).text()
        self.selected_id = uid
        self.username.setText(uname)
        self.password.clear()

    def delete_teacher(self):
        if not self.selected_id:
            QMessageBox.critical(self, "Error", "Select a teacher to delete")
            return

        reply = QMessageBox.question(
            self, "Confirm", "Delete this teacher account?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        con = get_connection()
        cur = con.cursor()
        cur.execute("DELETE FROM users WHERE id=?", (self.selected_id,))
        con.commit()
        con.close()

        QMessageBox.information(self, "Deleted", "Teacher deleted")
        self.clear_form()
        self.load_teachers()