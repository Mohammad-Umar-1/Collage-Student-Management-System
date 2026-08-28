from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QVBoxLayout,
    QHBoxLayout, QFormLayout, QFrame, QTableWidget, QTableWidgetItem,
    QMessageBox, QScrollArea, QHeaderView
)
from PyQt5.QtCore import Qt
from student import add_student, update_student, delete_student, get_all_students
from export_utils import (
    get_students_year,
    get_students_with_marks,
    export_excel,
    export_pdf
)

FIELDS = ["Admission No", "Name", "Gender", "Year", "Section", "Phone", "Email", "Address"]


class StudentWindow(QWidget):
    def __init__(self, role):
        super().__init__()
        self.role = role
        self.setWindowTitle("Student Management")
        self.showMaximized()

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

        page = QWidget()
        scroll.setWidget(page)
        layout = QVBoxLayout(page)
        layout.setContentsMargins(60, 20, 60, 20)

        # ================= HEADER =================
        header = QLabel("Student Management")
        header.setStyleSheet("font-size: 22pt; font-weight: bold;")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # ================= FORM =================
        form_frame = QFrame()
        form_frame.setStyleSheet("background-color: white; border: 1px solid #d1d5db;")
        form_layout = QFormLayout(form_frame)
        form_layout.setContentsMargins(30, 30, 30, 30)

        self.entries = {}
        for f in FIELDS:
            if f == "Gender":
                w = QComboBox()
                w.addItems(["Male", "Female"])
            elif f == "Year":
                w = QComboBox()
                w.addItems(["1", "2", "3", "4"])
            else:
                w = QLineEdit()
            form_layout.addRow(f, w)
            self.entries[f] = w

        layout.addWidget(form_frame)

        # ================= BUTTONS =================
        btns = QHBoxLayout()
        add_btn = QPushButton("Add")
        add_btn.setStyleSheet("background-color: #16a34a; color: white;")
        add_btn.clicked.connect(self.save)

        upd_btn = QPushButton("Update")
        upd_btn.setStyleSheet("background-color: #2563eb; color: white;")
        upd_btn.clicked.connect(self.update)

        del_btn = QPushButton("Delete")
        del_btn.setStyleSheet("background-color: #dc2626; color: white;")
        del_btn.clicked.connect(self.delete)

        btns.addStretch()
        btns.addWidget(add_btn)
        btns.addWidget(upd_btn)
        btns.addWidget(del_btn)
        btns.addStretch()
        layout.addLayout(btns)

        # ================= EXPORT =================
        export_frame = QFrame()
        export_frame.setStyleSheet("background-color: white; border: 1px solid #d1d5db;")
        export_layout = QVBoxLayout(export_frame)
        export_layout.setContentsMargins(20, 20, 20, 20)

        export_layout.addWidget(QLabel("<b>Export (Year-wise)</b>"))

        export_row = QHBoxLayout()
        self.year_cb = QComboBox()
        self.year_cb.addItems(["", "1", "2", "3", "4"])
        export_row.addWidget(self.year_cb)

        for text, handler in [
            ("Students → Excel", self.export_students_excel),
            ("Students → PDF", self.export_students_pdf),
            ("Marks → Excel", self.export_marks_excel),
            ("Marks → PDF", self.export_marks_pdf),
        ]:
            b = QPushButton(text)
            b.clicked.connect(handler)
            export_row.addWidget(b)

        export_layout.addLayout(export_row)
        layout.addWidget(export_frame)

        # ================= TABLE =================
        self.table = QTableWidget(0, len(FIELDS))
        self.table.setHorizontalHeaderLabels([f.upper() for f in FIELDS])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.itemSelectionChanged.connect(self.select_row)
        layout.addWidget(self.table)

        self.load_students()

    # ---------- CRUD ----------
    def save(self):
        try:
            add_student(
                self.entries["Admission No"].text(),
                self.entries["Name"].text(),
                self.entries["Gender"].currentText(),
                int(self.entries["Year"].currentText()),
                self.entries["Section"].text(),
                self.entries["Phone"].text(),
                self.entries["Email"].text(),
                self.entries["Address"].text()
            )
            self.load_students()
            self.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def update(self):
        try:
            update_student(
                self.entries["Admission No"].text(),
                self.entries["Name"].text(),
                self.entries["Gender"].currentText(),
                int(self.entries["Year"].currentText()),
                self.entries["Section"].text(),
                self.entries["Phone"].text(),
                self.entries["Email"].text(),
                self.entries["Address"].text()
            )
            self.load_students()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def delete(self):
        reply = QMessageBox.question(
            self, "Confirm", "Delete student?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            delete_student(self.entries["Admission No"].text())
            self.load_students()
            self.clear()

    # ---------- EXPORT HANDLERS ----------
    def _selected_year(self):
        year = self.year_cb.currentText()
        if not year:
            QMessageBox.critical(self, "Error", "Select year")
            return None
        return year

    def export_students_excel(self):
        year = self._selected_year()
        if not year:
            return
        df = get_students_year(year)
        export_excel(df, f"students_year_{year}", self)

    def export_students_pdf(self):
        year = self._selected_year()
        if not year:
            return
        df = get_students_year(year)
        export_pdf(df, f"students_year_{year}", "Student List", self)

    def export_marks_excel(self):
        year = self._selected_year()
        if not year:
            return
        df = get_students_with_marks(year)
        export_excel(df, f"students_marks_year_{year}", self)

    def export_marks_pdf(self):
        year = self._selected_year()
        if not year:
            return
        df = get_students_with_marks(year)
        export_pdf(df, f"students_marks_year_{year}", "Student Marks", self)

    # ---------- TABLE HELPERS ----------
    def load_students(self):
        self.table.setRowCount(0)
        for row in get_all_students():
            r = self.table.rowCount()
            self.table.insertRow(r)
            for c, val in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(val)))

    def clear(self):
        for f, w in self.entries.items():
            if isinstance(w, QComboBox):
                w.setCurrentIndex(0)
            else:
                w.clear()

    def select_row(self):
        row = self.table.currentRow()
        if row < 0:
            return
        for i, f in enumerate(FIELDS):
            val = self.table.item(row, i).text()
            w = self.entries[f]
            if isinstance(w, QComboBox):
                idx = w.findText(val)
                if idx >= 0:
                    w.setCurrentIndex(idx)
            else:
                w.setText(val)