from PySide6.QtWidgets import QDialog
from app.dialogs.employee_hire_dialog import EmployeeHireDialog
from app.windows.investsimwindow import InvestSimWindow
from controller.abstract import AbstractController
from model.invest_proj_model import InvestmentProjModel
from model.item_list_model import ItemListModel
from model.main_model import MainModel


class InvestProjectController(AbstractController[InvestSimWindow, InvestmentProjModel, MainModel]):
    def handleClose(self, event):
        event.accept()

    def init(self):
        super().init()
        self.view.setWindowTitle("Nuovo progetto di investimento")
        print(self.parent_model.company_data.available_years)
        model = ItemListModel(list_data = [])
        self.set_internal_pointer("model", model)
        self.view.ui.projectComponentsListView.setModel(model)

    def handleItemAdd(self):
        dialog = EmployeeHireDialog()
        self.set_internal_pointer("dialog", dialog)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            self.model.components.append(dialog.item)
            self.view.ui.projectComponentsListView.model().add_item(dialog.item)
            self.view.ui.projectComponentsListView.model().layoutChanged.emit()

