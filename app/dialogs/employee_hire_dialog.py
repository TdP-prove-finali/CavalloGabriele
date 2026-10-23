from PySide6.QtWidgets import QDialog

from app.ui_generated.ui_employee_hire import Ui_Dialog
from model.investment_item import EmployeeHireInvestment


class EmployeeHireDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.item: EmployeeHireInvestment | None = None