import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QLabel
from PySide6.QtCore import Qt

class Home(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        text = QLabel(self.get_html())
        text.setAlignment(Qt.AlignCenter & Qt.AlignTop)

        layout.addWidget(text)

    def get_html(self):
        file_path = os.path.join(os.path.dirname(__file__), "home.html")
        with open(file_path, "r") as f:
            return ''.join(line for line in f)