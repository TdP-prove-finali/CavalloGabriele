from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QDialog, QMessageBox

from app.ui_generated.ui_asset_invest import Ui_Dialog
from dao.util import check_empty, parse
from model.investment_item import AssetInvestment


class AssetDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.__item__: AssetInvestment | None = None
        regex = QRegularExpression(r"-?\d+(?:[.,]\d+)?")
        self.ui.totalCostEdit.setValidator(QRegularExpressionValidator(regex, self.ui.totalCostEdit))
        self.ui.maintenanceCostEdit.setValidator(QRegularExpressionValidator(regex, self.ui.maintenanceCostEdit))

    def accept(self, /):
        print("Accept")
        t = self.ui.operationTitleEdit.text()
        c_l = self.ui.totalCostEdit.text()
        s = self.ui.durationSpinBox.text()
        o = self.ui.maintenanceCostEdit.text()
        r = self.ui.assetTypeCombo.currentIndex()
        print(r)

        if check_empty(t) or check_empty(c_l) or check_empty(r):
            msgBox = QMessageBox()
            msgBox.setText("Inserisci tutti i parametri obbligatori")
            msgBox.setIcon(QMessageBox.Icon.Warning)
            msgBox.exec()
            return

        self.__item__ = AssetInvestment(
            title=t,
            id=1,
            total_cost=parse(c_l),
            duration_years=parse(s),
            maintenance_cost=parse(o),
            asset_type=r
        )
        super().accept()

    @property
    def item(self):
        return self.__item__