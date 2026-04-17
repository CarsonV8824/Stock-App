import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QComboBox, QHBoxLayout
from PySide6.QtCore import Signal

class ButtonControl(QWidget):
    # Define signals for each button
    home_clicked = Signal()
    predict_clicked = Signal()
    graph_clicked = Signal()
    
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        self.setLayout(layout)

        home = QPushButton("Home")
        home.clicked.connect(self.home_clicked.emit)
        layout.addWidget(home)

        graph = QPushButton("Graph")
        graph.clicked.connect(self.graph_clicked.emit)
        layout.addWidget(graph)

        predict = QPushButton("Predict")
        predict.clicked.connect(self.predict_clicked.emit)
        layout.addWidget(predict)