import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

from gui.mainWindow import MainWindow

def main():
    # 1. Create the application instance
    app = QApplication(sys.argv)

    window = MainWindow()

    # 4. Show the window
    window.show()

    # 5. Start the event loop
    app.exec()
    

if __name__ == "__main__":
    main()