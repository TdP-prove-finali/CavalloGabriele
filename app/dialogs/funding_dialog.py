from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QDialog, QMessageBox

from app.ui_generated.ui_funding_invest import Ui_Dialog
from dao.util import check_empty, parse
from model.investment_item import FundingInvestment, FundingType
from model.raw_company_data import CashMeasureUnit


class FundingDialog(QDialog):
    def __init__(self, mu: CashMeasureUnit):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.__item__: FundingInvestment | None = None
        regex = QRegularExpression(r"-?\d+(?:[.,]\d+)?")
        self.ui.totalImportEdit.setValidator(QRegularExpressionValidator(regex, self.ui.totalImportEdit))
        self.mu = mu
        self.ui.cash_label.setText(self.mu.__str__())

    def accept(self, /):
        t = self.ui.operationTitleEdit.text()
        c_l = self.ui.totalImportEdit.text()
        s = self.ui.interestRateEdit.text()
        o = self.ui.durationYearsEdit.text()
        r = self.ui.typeComboBox.currentIndex()

        if check_empty(t) or check_empty(c_l) or check_empty(r):
            msgBox = QMessageBox()
            msgBox.setText("Inserisci tutti i parametri obbligatori")
            msgBox.setIcon(QMessageBox.Icon.Warning)
            msgBox.exec()
            return

        if parse(c_l) <= 0:
            msgBox = QMessageBox()
            msgBox.setText("L'importo del finanziamento deve essere > 0")
            msgBox.setIcon(QMessageBox.Icon.Critical)
            msgBox.exec()
            return

        if parse(s) < 0:
            msgBox = QMessageBox()
            msgBox.setText("Il tasso di interesse non può essere negativo")
            msgBox.setIcon(QMessageBox.Icon.Critical)
            msgBox.exec()
            return

        tp = None
        if r == 0:
            tp = FundingType.BANK
        else:
            tp = FundingType.STOCK

        self.__item__ = FundingInvestment(
            title=t,
            duration=int(o),
            interest_rate=parse(s) / 100,
            total_import=parse(c_l),
            type=tp
        )
        super().accept()

    @property
    def item(self):
        return self.__item__