import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        self.setWindowTitle("Stock App")

        test_button = QPushButton("Test Button")    
        test_button.clicked.connect(lambda: print("Button Clicked!"))
        main_layout.addWidget(test_button)

        
