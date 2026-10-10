from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow
from app.ui_generated.ui_main_window import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.sayHelloBtn.clicked.connect(self.on_pushBtnClick)
        self.ui.actionImportazione.triggered.connect(self.on_import_trigger)
        self._controller = None

    @Slot()
    def on_import_trigger(self):
        self.controller.handleImportDialog()

    @Slot()
    def on_pushBtnClick(self):
        self.controller.handleSayHelloButtonClick()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def closeEvent(self, event, /):
        if self._controller is not None:
            self._controller.handleClose(event)