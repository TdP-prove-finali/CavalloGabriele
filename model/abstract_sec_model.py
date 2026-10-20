from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtGui import QColor

from dao.util import format_number, is_number

class AbstractSectionTableModel(QAbstractTableModel):
    """
    Rappresenta un generico modello da utilizzare per intabellare una section,
    organizzata come dizionario chiave-valore e con le traduzioni delle chiavi in un altro dizionario
    """
    def __init__(self, data: dict, translations: dict[str, str], max_row_count = None, max_column_count = None):
        QAbstractTableModel.__init__(self)
        if max_row_count is None:
            self.row_count = len(data.keys())
        else:
            self.row_count = max_row_count
            self.__max_row_count__ = max_row_count

        self._data = data
        self._translations = translations

        if max_column_count is None:
            self.column_count = len(data["data"])
        else:
            self.column_count = max_column_count
            self.__max_col_count__ = max_column_count

    def rowCount(self, parent=QModelIndex()):
        return self.row_count

    def columnCount(self, parent=QModelIndex()):
        return self.column_count

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        column = index.column()
        row = index.row()
        keys = list(self._data.keys())

        if role == Qt.ItemDataRole.DisplayRole:
            field_name = keys[row]
            d= self._data[field_name][column]
            if d is not None:
                if is_number(d):
                    return format_number(d)
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
            return "Anno " + str(2026 - section - 1)
        elif orientation == Qt.Orientation.Vertical:
            field_name = keys[section]

            if self._translations.get(field_name) is not None:
                return self._translations[field_name].strip()
            else:
                return field_name