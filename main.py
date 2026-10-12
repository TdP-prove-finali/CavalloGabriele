import sys

import PySide6
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication

from app.windows.mainwindow import MainWindow
from app.windows.startupwindow import StartupWindow
from config.paths import project_rooted
from controller.startup_controller import StartupController


def calcolo_esempio(a, b):
    return a / b

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pixMap = QPixmap((project_rooted("app") / "resources" / "business_scenario_lab_icon.png").__str__())
    app.setWindowIcon(
        pixMap.scaled(
            50,
            50,
            PySide6.QtCore.Qt.AspectRatioMode.KeepAspectRatio
        )
    )
    window = StartupWindow()
    window.show()
    ctrl = StartupController(None, window, app)
    window.controller = ctrl

    sys.exit(app.exec())
