from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QVBoxLayout,
    QHBoxLayout, QFormLayout, QFrame, QTableWidget, QTableWidgetItem,
    QMessageBox, QScrollArea, QHeaderView
)
from PyQt5.QtCore import Qt
from marks import (
    get_students_by_year,
    get_marks_for_student,
    save_mark,
    delete_mark
)

SEM_MAP = {1: [1, 2], 2: [3, 4], 3: [5, 6], 4: [7, 8]}


class MarksWindow(QWidget):
    def __init__(self, role):
        super().__init__()
        self.role = role
        self.selected_adm = None
        self.setWindowTitle("Marks Management")
        self.showMaximized()

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

        page = QWidget()
        scroll.setWidget(page)
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 20, 30, 20)

        header = QLabel("Marks Management")
        header.setStyleSheet("font-size: 22pt; font-weight: bold;")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        body = QHBoxLayout()
        layout.addLayout(body)

        # ================= LEFT PANEL =================
        left = QFrame()
        left.setStyleSheet("background-color: #f3f4f6; border: 1px solid #d1d5db;")
        left.setFixedWidth(300)
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(20, 20, 20, 20)

        left_layout.addWidget(self._section_title("Academic Filters"))

        left_layout.addWidget(QLabel("Year"))
        self.year_cb = QComboBox()
        self.year_cb.addItems(["", "1", "2", "3", "4"])
        self.year_cb.currentTextChanged.connect(self.update_semesters)
        left_layout.addWidget(self.year_cb)

        left_layout.addWidget(QLabel("Semester"))
        self.sem_cb = QComboBox()
        self.sem_cb.currentTextChanged.connect(self.load_students)
        left_layout.addWidget(self.sem_cb)

        left_layout.addWidget(QLabel("Subject"))
        self.subject_cb = QComboBox()
        self.subject_cb.addItems([f"Subject {i}" for i in range(1, 6)])
        left_layout.addWidget(self.subject_cb)

        left_layout.addWidget(self._section_title("Students"))

        self.student_table = QTableWidget(0, 2)
        self.student_table.setHorizontalHeaderLabels(["Admission No", "Name"])
        self.student_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.student_table.itemSelectionChanged.connect(self.select_student)
        left_layout.addWidget(self.student_table)

        body.addWidget(left)

        # ================= RIGHT PANEL =================
        right = QVBoxLayout()
        body.addLayout(right, stretch=1)

        self.info_label = QLabel("")
        self.info_label.setStyleSheet("font-size: 13pt;")
        self.info_label.setAlignment(Qt.AlignCenter)
        right.addWidget(self.info_label)

        self.percent_label = QLabel("Semester Percentage: --")
        self.percent_label.setStyleSheet("font-size: 16pt; font-weight: bold; color: #2563eb;")
        self.percent_label.setAlignment(Qt.AlignCenter)
        right.addWidget(self.percent_label)

        # ---- FORM ----
        form_frame = QFrame()
        form_frame.setStyleSheet("background-color: white; border: 1px solid #d1d5db;")
        form_layout = QFormLayout(form_frame)
        form_layout.setContentsMargins(25, 25, 25, 25)

        self.u1 = QLineEdit()
        self.u2 = QLineEdit()
        self.final = QLineEdit()
        form_layout.addRow("Unit 1 ( /50 )", self.u1)
        form_layout.addRow("Unit 2 ( /50 )", self.u2)
        form_layout.addRow("Final ( /100 )", self.final)
        right.addWidget(form_frame, alignment=Qt.AlignHCenter)

        # ---- BUTTONS ----
        save_btn = QPushButton("Save / Update")
        save_btn.setStyleSheet("background-color: #2563eb; color: white; font-weight: bold;")
        save_btn.clicked.connect(self.save_marks)
        right.addWidget(save_btn, alignment=Qt.AlignHCenter)

        del_btn = QPushButton("Delete Marks")
        del_btn.setStyleSheet("background-color: #dc2626; color: white; font-weight: bold;")
        del_btn.clicked.connect(self.delete_marks)
        right.addWidget(del_btn, alignment=Qt.AlignHCenter)

        right.addWidget(self._section_title("Saved Marks"))

        marks_card = QFrame()
        marks_card.setStyleSheet("background-color: white; border: 1px solid #d1d5db;")
        marks_card_layout = QVBoxLayout(marks_card)

        self.marks_table = QTableWidget(0, 4)
        self.marks_table.setHorizontalHeaderLabels(["SUBJECT", "U1", "U2", "FINAL"])
        self.marks_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.marks_table.itemSelectionChanged.connect(self.select_mark)
        marks_card_layout.addWidget(self.marks_table)

        right.addWidget(marks_card)

    def _section_title(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet("font-size: 14pt; font-weight: bold;")
        lbl.setAlignment(Qt.AlignCenter)
        return lbl

    # ---------- HELPERS ----------
    def valid(self, val, maxv):
        try:
            v = float(val)
            if 0 <= v <= maxv:
                return round(v, 2)
        except (TypeError, ValueError):
            pass
        return None

    def subject_percent(self, a, b, c):
        return ((a + b + c) / 200) * 100

    # ---------- LOGIC ----------
    def update_semesters(self, year_text):
        self.sem_cb.blockSignals(True)
        self.sem_cb.clear()
        if year_text:
            self.sem_cb.addItems([str(s) for s in SEM_MAP[int(year_text)]])
        self.sem_cb.blockSignals(False)

    def load_students(self, sem_text=None):
        self.student_table.setRowCount(0)
        if not self.year_cb.currentText():
            return
        for adm, name in get_students_by_year(int(self.year_cb.currentText())):
            r = self.student_table.rowCount()
            self.student_table.insertRow(r)
            self.student_table.setItem(r, 0, QTableWidgetItem(str(adm)))
            self.student_table.setItem(r, 1, QTableWidgetItem(str(name)))

    def load_saved_marks(self, adm):
        self.marks_table.setRowCount(0)
        if not self.sem_cb.currentText():
            return
        rows = get_marks_for_student(adm, int(self.sem_cb.currentText()))

        for s, a, b, c in rows:
            r = self.marks_table.rowCount()
            self.marks_table.insertRow(r)
            for col, val in enumerate((s, a, b, c)):
                self.marks_table.setItem(r, col, QTableWidgetItem(str(val)))

        if len(rows) == 5:
            total = sum(self.subject_percent(a, b, c) for _, a, b, c in rows)
            self.percent_label.setText(f"Semester Percentage: {round(total / 5, 2)}%")
        else:
            self.percent_label.setText("Semester Percentage: -- (Add all 5 subjects)")

    def select_student(self):
        row = self.student_table.currentRow()
        if row < 0:
            return
        adm = self.student_table.item(row, 0).text()
        name = self.student_table.item(row, 1).text()
        self.selected_adm = adm
        self.info_label.setText(f"{name}  |  Admission No: {adm}")
        self.load_saved_marks(adm)

    def select_mark(self):
        row = self.marks_table.currentRow()
        if row < 0:
            return
        s = self.marks_table.item(row, 0).text()
        a = self.marks_table.item(row, 1).text()
        b = self.marks_table.item(row, 2).text()
        c = self.marks_table.item(row, 3).text()
        idx = self.subject_cb.findText(s)
        if idx >= 0:
            self.subject_cb.setCurrentIndex(idx)
        self.u1.setText(a)
        self.u2.setText(b)
        self.final.setText(c)

    def save_marks(self):
        if not self.selected_adm:
            QMessageBox.critical(self, "Error", "Select a student")
            return

        a = self.valid(self.u1.text(), 50)
        b = self.valid(self.u2.text(), 50)
        c = self.valid(self.final.text(), 100)

        if None in (a, b, c):
            QMessageBox.critical(
                self, "Invalid Marks",
                "Unit 1 & 2: 0-50\nFinal: 0-100\nUp to 2 decimals"
            )
            return

        save_mark(
            self.selected_adm,
            self.subject_cb.currentText(),
            int(self.sem_cb.currentText()),
            a, b, c
        )

        self.load_saved_marks(self.selected_adm)

    def delete_marks(self):
        if not self.selected_adm:
            return
        delete_mark(
            self.selected_adm,
            self.subject_cb.currentText(),
            int(self.sem_cb.currentText())
        )
        self.load_saved_marks(self.selected_adm)