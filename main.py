import sys

from PySide6.QtWidgets import QApplication

from app.windows.mainwindow import MainWindow

def calcolo_esempio(a, b):
    return a / b

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
