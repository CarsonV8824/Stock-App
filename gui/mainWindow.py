import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QHBoxLayout

from gui.stack_widgets.home import Home
from gui.stack_widgets.predict import Predict
from gui.side.button_control import ButtonControl

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        main_layout = QHBoxLayout()
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        self.setWindowTitle("Stock App")

        side_control = ButtonControl()
        main_layout.addWidget(side_control)

        stack = QStackedWidget()
        main_layout.addWidget(stack)

        home = Home()
        stack.addWidget(home)

        predict = Predict()
        stack.addWidget(predict)

        side_control.home_clicked.connect(lambda: stack.setCurrentIndex(0))
        side_control.predict_clicked.connect(lambda: stack.setCurrentIndex(1))

        
