from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtGui import QColor

from dao.util import is_number


class SummaryTableModel(QAbstractTableModel):
    def __init__(self, data: dict, translations: dict):
        QAbstractTableModel.__init__(self)
        self.column_count = 2
        self.row_count = len(data.keys())
        self._data = data
        self._translations = translations

    def rowCount(self, parent=QModelIndex()):
        return self.row_count

    def columnCount(self, parent=QModelIndex()):
        return self.column_count

    def format_number(value, decimals: int = 2) -> str:
        return f"{value:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        # TODO: Formattare i numeri con i punti di separazione delle migliaia
        # TODO: Gestire altezza righe e word-wrap
        # TODO: Inserire in UI informazioni sul fatto che sono gli ultimi 2 anni
        column = index.column()
        row = index.row()
        keys = list(self._data.keys())

        if role == Qt.ItemDataRole.DisplayRole:
            field_name = keys[row]
            d= self._data[field_name][column - 1]
            if d is not None:
                return d
            else:
                return "n.d."
        elif role == Qt.ItemDataRole.BackgroundRole:
            return QColor(Qt.GlobalColor.darkGray)
        elif role == Qt.ItemDataRole.FontRole:
            return QColor(Qt.GlobalColor.white)
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignRight

        return None

    def headerData(self, section, orientation, role):
        keys = list(self._data.keys())
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        elif orientation == Qt.Orientation.Horizontal:
            return "Anno " + str(2026 - section)
        elif orientation == Qt.Orientation.Vertical:
            field_name = keys[section]

            if self._translations.get(field_name) is not None:
                return self._translations[field_name].strip()
            else:
                return field_name