from app.dialogs.employee_hire_dialog import EmployeeHireDialog
from app.windows.investsimwindow import InvestSimWindow
from controller.abstract import AbstractController
from model.invest_proj_model import InvestmentProjModel
from model.main_model import MainModel


class InvestProjectController(AbstractController[InvestSimWindow, InvestmentProjModel, MainModel]):
    def handleClose(self, event):
        event.accept()

    def init(self):
        super().init()
        self.view.setWindowTitle("Nuovo progetto di investimento")
        print(self.parent_model.company_data.available_years)

    def handleItemAdd(self):
        dialog = EmployeeHireDialog()
        dialog.show()
        self.set_internal_pointer("dialog", dialog)