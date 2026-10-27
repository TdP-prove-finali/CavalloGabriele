from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QDialog, QMessageBox

from app.ui_generated.ui_operativ_effic_dialog import Ui_Dialog
from dao.util import check_empty, parse
from model.investment_item import FundingInvestment, FundingType, ProductivityImprovementInvestment


class OperativeImprovementDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.__item__: ProductivityImprovementInvestment | None = None
        regex = QRegularExpression(r"-?\d+(?:[.,]\d+)?")
        self.ui.totalImportEdit.setValidator(QRegularExpressionValidator(regex, self.ui.totalImportEdit))

    def accept(self, /):
        t = self.ui.operationTitleEdit.text()
        c_l = self.ui.totalImportEdit.text()
        s = self.ui.yearlyEffectEdit.text()

        if check_empty(t) or check_empty(c_l) or check_empty(s):
            msgBox = QMessageBox()
            msgBox.setText("Inserisci tutti i parametri obbligatori")
            msgBox.setIcon(QMessageBox.Icon.Warning)
            msgBox.exec()
            return


        self.__item__ = ProductivityImprovementInvestment(
            title=t,
            id=1,
            total_cost=parse(c_l),
            yearly_op_cost_reduction=parse(s)
        )
        super().accept()

    @property
    def item(self):
        return self.__item__