from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QMessageBox
from app.ui_generated.ui_main_window import Ui_MainWindow
from controller.main_controller import MainController

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.sayHelloBtn.clicked.connect(self.on_pushBtnClick)
        self._controller: MainController = None

    @Slot()
    def on_pushBtnClick(self):
        self.controller.handleSayHelloButtonClick()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller
