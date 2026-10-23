from PySide6 import QtCore, QtGui
from PySide6.QtCore import Qt

from config.paths import project_rooted
from model.investment_item import AbstractInvestmentItem

tick = QtGui.QImage(project_rooted("app") / "resources" / "employee-salary-business-svgrepo-com.png")

class ItemListModel(QtCore.QAbstractListModel):
    def __init__(self, *args, list_data: list[AbstractInvestmentItem], **kwargs):
        super().__init__(*args, **kwargs)
        self.list_data = list_data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            # See below for the data structure.
            item = self.list_data[index.row()]
            return f"{item.title}, {item.role}"
        elif role == Qt.ItemDataRole.DecorationRole:
            item = self.list_data[index.row()]
            if item.type == "employee-hire":
                return tick

        return None

    def add_item(self, item):
        self.list_data.append(item)

    def rowCount(self, index):
        return len(self.list_data)