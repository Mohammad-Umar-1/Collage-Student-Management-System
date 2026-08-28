# PyQt5 global stylesheet (QSS) replacing ttk.Style theme
APP_STYLESHEET = """
QWidget {
    font-family: 'Segoe UI';
    font-size: 11pt;
}
QPushButton {
    padding: 8px;
    font-size: 11pt;
}
QTableWidget {
    font-size: 10pt;
    gridline-color: #e5e7eb;
}
QHeaderView::section {
    font-weight: bold;
    font-size: 11pt;
    padding: 6px;
}
QTableWidget::item {
    padding: 4px;
}
"""


def apply_style(app):
    # app = QApplication instance
    app.setStyleSheet(APP_STYLESHEET)
