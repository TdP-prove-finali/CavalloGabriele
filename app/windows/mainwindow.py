from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QWidget
from app.ui_generated.ui_main_window import Ui_MainWindow
from controller.abstract import AbstractController


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._controller: AbstractController | None = None
        self.__connstat_widget__ = None
        self.__datastat_widget__ = None
        self.ui.expandBalanceButton.clicked.connect(self.handleExpandBalance)

    @Slot()
    def handleExpandBalance(self):
        self.controller.handleExpandBalance()

    def set_controller(self, controller):
        self._controller = controller

    @property
    def controller(self):
        if self._controller is not None:
            return self._controller
        raise Exception("Controller richiesto ma non ancora impostato")

    def closeEvent(self, event, /):
        if self._controller is not None:
            self._controller.handleClose(event)