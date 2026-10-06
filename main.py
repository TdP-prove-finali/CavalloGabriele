import sys

from PySide6.QtWidgets import QApplication

from app.windows.mainwindow import MainWindow
from controller.main_controller import MainController


def calcolo_esempio(a, b):
    return a / b

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    ctrl = MainController(None, window)
    window.controller = ctrl

    sys.exit(app.exec())
