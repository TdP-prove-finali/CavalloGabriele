from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtGui import QColor

from dao.util import is_number, format_number

# TODO: Migliorare architettura con classe astratta che prende un dizionario e costruisce una tabella,
# con possibilità di specificare la quantità massima di colonne e righe da utilizzare.

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

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        # TODO: Gestire altezza righe e word-wrap
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