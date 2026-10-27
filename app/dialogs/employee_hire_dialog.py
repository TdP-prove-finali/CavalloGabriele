from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QDialog, QMessageBox

from app.ui_generated.ui_employee_hire import Ui_Dialog
from dao.util import check_empty, check_invalid_factor, parse
from model.investment_item import EmployeeHireInvestment

class EmployeeHireDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.__item__: EmployeeHireInvestment | None = None
        regex = QRegularExpression(r"-?\d+(?:[.,]\d+)?")
        self.ui.monthlyCostEdit.setValidator(QRegularExpressionValidator(regex, self.ui.monthlyCostEdit))
        self.ui.strumentCostEdit.setValidator(QRegularExpressionValidator(regex, self.ui.strumentCostEdit))
        self.ui.onboardingCostEdit.setValidator(QRegularExpressionValidator(regex, self.ui.onboardingCostEdit))

    def accept(self, /):
        print("Accept")
        t = self.ui.operationTitleEdit.text()
        c_l = self.ui.monthlyCostEdit.text()
        s = self.ui.strumentCostEdit.text()
        o = self.ui.onboardingCostEdit.text()
        r = self.ui.roleComboBox.currentText()
        l_s = self.ui.scaleEditNum.text()
        l_f = self.ui.shapeEditNum.text()
        n_a = self.ui.averageEditNum.text()
        n_v = self.ui.varianceEditNum.text()
        sr = self.ui.stopRatioEditNum.text()
        print(r)

        if check_empty(t) or check_empty(c_l) or check_empty(o) or check_empty(r) or check_empty(l_s) or check_empty(l_f)\
                or check_empty(n_a) or check_empty(n_v):
            msgBox = QMessageBox()
            msgBox.setText("Inserisci tutti i parametri obbligatori")
            msgBox.setIcon(QMessageBox.Icon.Warning)
            msgBox.exec()
            return

        if check_invalid_factor(l_s) or check_invalid_factor(l_f) or check_invalid_factor(n_a) or check_invalid_factor(n_v):
            msgBox = QMessageBox()
            msgBox.setText("Alcuni dei parametri delle distribuzioni inseriti non sono corretti. ")
            msgBox.setInformativeText("Tutti i parametri devono essere non nulli")
            msgBox.setIcon(QMessageBox.Icon.Warning)
            msgBox.exec()
            return

        self.__item__ = EmployeeHireInvestment(
            title=t,
            id=1,
            total_monthly_cost=parse(c_l),
            onboarding_cost=parse(o),
            strumental_cost=parse(s),
            hp_lomax_scale=parse(l_s),
            hp_lomax_shape=parse(l_f),
            ttp_normal_average=parse(n_a),
            ttp_normal_variance=parse(n_v),
            stop_ratio=parse(sr),
            role=r
        )
        super().accept()

    @property
    def item(self):
        return self.__item__