from PySide6.QtCore import Slot
from PySide6.QtWidgets import QDialog

from app.ui_generated.ui_balance_detail_dialog import Ui_Dialog

class BalanceDetailDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self._controller = None
        self.ui.numberOfYearsCombo.currentIndexChanged.connect(self.handleYearsChange)

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    @Slot()
    def handleYearsChange(self, event):
        if self.controller is not None:
            self.controller.handleYearsChange(event)