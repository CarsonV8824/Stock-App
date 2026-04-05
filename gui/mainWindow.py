import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)