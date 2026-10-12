from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QWidget
from app.ui_generated.ui_startupwindow import Ui_MainWindow

class StartupWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._controller = None
        self.__connstat_widget__ = None
        self.__datastat_widget__ = None
        self.ui.actionImportazione.triggered.connect(self.onImportTrigger)

    @Slot()
    def onImportTrigger(self):
        self.controller.handleImportDialog()

    def resizeEvent(self, event, /):
        super().resizeEvent(event)
        if self.controller is not None:
            self.controller.__resize_logo__()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def closeEvent(self, event, /):
        if self._controller is not None:
            self._controller.handleClose(event)

    @property
    def connection_status_widget(self) -> QWidget:
        if self.__connstat_widget__ is None:
            self.__connstat_widget__ = QWidget()

        return self.__connstat_widget__

    @property
    def data_status_widget(self) -> QWidget:
        if self.__datastat_widget__ is None:
            self.__datastat_widget__ = QWidget()

        return self.__datastat_widget__