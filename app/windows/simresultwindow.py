from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QWidget

from app.ui_generated.ui_sim_result import Ui_MainWindow
from controller.abstract import AbstractController

class SimResultWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._controller: AbstractController | None = None

    def set_controller(self, controller):
        self._controller = controller

    @property
    def controller(self):
        if self._controller is not None:
            return self._controller
        raise Exception("Controller richiesto ma non ancora impostato")

    @Slot()
    def handle_rem_item(self):
        self.controller.handleRemoveItem()

    def closeEvent(self, event, /):
        if self._controller is not None:
            self._controller.handleClose(event)

