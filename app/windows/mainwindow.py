from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QWidget
from app.ui_generated.ui_main_window import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self, company_fiscal_code: int):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._controller = None
        self.__connstat_widget__ = None
        self.__datastat_widget__ = None
        self.company_fiscal_code = company_fiscal_code

    def closeEvent(self, event, /):
        if self._controller is not None:
            self._controller.handleClose(event)