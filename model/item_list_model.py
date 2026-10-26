from PySide6 import QtCore, QtGui
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPainter, QColor

from config.paths import project_rooted
from model.investment_item import AbstractInvestmentItem


class ItemListModel(QtCore.QAbstractListModel):
    def __init__(self, *args, list_data: list[AbstractInvestmentItem], **kwargs):
        super().__init__(*args, **kwargs)
        self.list_data = list_data
        self.tick = QtGui.QImage(project_rooted("app") / "resources" / "employee-salary-business-svgrepo-com.png")
        self.tick = self.tick.scaled(
            50, 60,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ).convertToFormat(QImage.Format.Format_ARGB32)

        painter = QPainter(self.tick)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(self.tick.rect(), QColor("white"))
        painter.end()

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            item = self.list_data[index.row()]
            return f"{item.title}, {item.role}"
        elif role == Qt.ItemDataRole.DecorationRole:
            item = self.list_data[index.row()]
            if item.type == "employee-hire":
                return self.tick

        return None

    def remove_item_by_index(self, index):
        self.list_data.remove(self.list_data[index])

    def add_item(self, item):
        self.list_data.append(item)

    def rowCount(self, index):
        return len(self.list_data)