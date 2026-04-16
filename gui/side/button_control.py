import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QComboBox
from PySide6.QtCore import Signal

class ButtonControl(QWidget):
    # Define signals for each button
    home_clicked = Signal()
    predict_clicked = Signal()
    
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        home = QPushButton("Home")
        home.clicked.connect(self.home_clicked.emit)
        layout.addWidget(home)

        predict = QPushButton("Predict")
        predict.clicked.connect(self.predict_clicked.emit)
        layout.addWidget(predict)