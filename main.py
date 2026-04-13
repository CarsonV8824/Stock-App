import sys, os
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

from gui.mainWindow import MainWindow

file_path = os.path.join(os.path.dirname(__file__), "assets", "styles.css")
with open(file_path, "r") as f:
    file_path = f.read()

def main():
   
    app = QApplication(sys.argv)
    app.setStyleSheet(file_path)

    window = MainWindow()

    window.show()

    sys.exit(app.exec())    
    
if __name__ == "__main__":
    main()