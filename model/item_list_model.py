from PySide6 import QtCore, QtGui
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPainter, QColor
from config.paths import project_rooted
from dao.util import format_number
from model.investment_item import AbstractInvestmentItem, EmployeeHireInvestment, FundingInvestment, FundingType, \
    AssetInvestment, AssetType, ProductivityImprovementInvestment


def prepare_icon(path):
    icon = QtGui.QImage(path)
    icon = icon.scaled(
        50, 60,
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation
    ).convertToFormat(QImage.Format.Format_ARGB32)

    painter = QPainter(icon)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(icon.rect(), QColor("white"))
    painter.end()
    return icon

class ItemListModel(QtCore.QAbstractListModel):
    def __init__(self, *args, list_data: list[AbstractInvestmentItem], **kwargs):
        super().__init__(*args, **kwargs)
        self.list_data = list_data
        self.tick = prepare_icon(project_rooted("app") / "resources" / "employee-salary-business-svgrepo-com.png")
        self.money = prepare_icon(project_rooted("app") / "resources" / "money.png")
        self.factory = prepare_icon(project_rooted("app") / "resources" / "factory.png")
        self.line_graph = prepare_icon(project_rooted("app") / "resources" / "line-graph.png")

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            item = self.list_data[index.row()]
            if isinstance(item, EmployeeHireInvestment):
                return f"{item.title}, {item.role}, {format_number(item.total_monthly_cost)}€"
            elif isinstance(item, FundingInvestment):
                if item.funding_type == FundingType.BANK:
                    s = "Bancario"
                else:
                    s = "Versamento capitale sociale"
                return f"{item.title}, {format_number(item.total_import)}€, {s}"
            elif isinstance(item, AssetInvestment):
                if item.asset_type == AssetType.MATERIAL:
                    s = "Materiale"
                else:
                    s = "Immateriale"
                return f"{item.title}, {format_number(item.total_cost)}€, {s}"
            elif isinstance(item, ProductivityImprovementInvestment):
                return f"Efficientamento {item.title}, {format_number(item.total_cost)}€, {item.yearly_op_cost_reduction} %"

        elif role == Qt.ItemDataRole.DecorationRole:
            item = self.list_data[index.row()]
            if item.type == "employee-hire":
                return self.tick
            elif isinstance(item, FundingInvestment):
                return self.money
            elif isinstance(item, AssetInvestment):
                return self.factory
            elif isinstance(item, ProductivityImprovementInvestment):
                return self.line_graph


        return None

    def remove_item_by_index(self, index):
        self.list_data.remove(self.list_data[index])

    def add_item(self, item):
        self.list_data.append(item)

    def rowCount(self, index):
        return len(self.list_data)