from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtGui import QColor, QFont

from dao.util import is_number, format_number
from model.section import SPSection


class SPTableModel(QAbstractTableModel):
    def __init__(self, data: SPSection, translations: dict, max_columns = None):
        QAbstractTableModel.__init__(self)
        self.row_count = len(data.patrimonio_netto.keys()) + len(data.debiti.keys()) + len(data.attivo) + 2
        if max_columns is None:
            self.column_count = len(data.context["data"])
        else:
            self.column_count = max_columns

        self._data = data
        self._translations = translations

    def rowCount(self, parent=QModelIndex()):
        return self.row_count

    def columnCount(self, parent=QModelIndex()):
        return self.column_count

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        column = index.column()
        row = index.row()
        d = None
        field_name = None

        if row == 0 and role == Qt.ItemDataRole.DisplayRole:
            field_name = "Attivo"
            d = None
        elif row <= self._data.count_attivo_fields:
            field_name = self._data.get_attivo_key(row - 1)
            if role == Qt.ItemDataRole.DisplayRole:
                d = self._data.attivo[field_name][column]
        elif row == self._data.count_attivo_fields:     # Totale attivo
            pass
        elif row == self._data.count_attivo_fields + 1:      # Inizio del passivo
            pass
        elif self._data.count_attivo_fields + 1 < row <= self._data.count_attivo_fields + self._data.count_patrimon_fields + 1:
            field_name = self._data.get_patrimn_key(row - self._data.count_attivo_fields - 2)
            if role == Qt.ItemDataRole.DisplayRole:
                d = self._data.patrimonio_netto[field_name][column]
        elif self._data.count_attivo_fields + self._data.count_patrimon_fields < row <= self._data.count_attivo_fields + self._data.count_patrimon_fields + self._data.count_debiti_fields + 1:
            field_name = self._data.get_debiti_key(row - self._data.count_attivo_fields - 2 - self._data.count_patrimon_fields)
            if role == Qt.ItemDataRole.DisplayRole:
                d = self._data.debiti[field_name][column]

        if role == Qt.ItemDataRole.DisplayRole:
            return self.__prepare_data__(d)
        elif field_name is not None and field_name.find("totale") > -1:
            return self.getSectionHeadData(role)
        elif role == Qt.ItemDataRole.BackgroundRole:
            return QColor(Qt.GlobalColor.darkGray)
        elif role == Qt.ItemDataRole.FontRole:
            return QColor(Qt.GlobalColor.white)
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignRight

        return None

    def __prepare_data__(self, d):
        if d is not None:
            if is_number(d):
                return format_number(d)
            return d
        else:
            return "n.d."

    def headerData(self, section, orientation, role):
        # TODO: Header con le sotto-sezioni dello SP
        # TODO: Utilizzare il TooltipRole per mostrare un tooltip delle sezioni più importanti
        # Ad esempio con lista hard-coded di descrizioni complete sulle cose più dettagliate
        if orientation == Qt.Orientation.Horizontal:
            if role == Qt.ItemDataRole.DisplayRole:
                return "Anno " + str(2026 - section - 1)
            else:
                return None
        elif orientation == Qt.Orientation.Vertical:
            field_name = None
            if section == 0:
                if role == Qt.ItemDataRole.DisplayRole:
                    return "Attivo"
            elif section <= self._data.count_attivo_fields:
                field_name = self._data.get_attivo_key(section - 1)
            elif section == self._data.count_attivo_fields + 1:
                if role == Qt.ItemDataRole.DisplayRole:
                    return "Passivo"
            elif self._data.count_attivo_fields + 1 < section <= self._data.count_attivo_fields + self._data.count_patrimon_fields + 1:
                field_name = self._data.get_patrimn_key(section - self._data.count_attivo_fields - 2)
            elif self._data.count_attivo_fields + self._data.count_patrimon_fields < section <= self._data.count_attivo_fields + self._data.count_patrimon_fields + self._data.count_debiti_fields + 1:
                field_name = self._data.get_debiti_key(
                    section - self._data.count_attivo_fields - 2 - self._data.count_patrimon_fields)

            if role == Qt.ItemDataRole.DisplayRole:
                return self.__get_translation_for__(field_name)

            elif role != Qt.ItemDataRole.DisplayRole and field_name is not None and (field_name.find("totale") != -1 or section == 0):
                return self.getSectionHeadData(role)

        return None

    def __get_translation_for__(self, f_name):
        if self._translations.get(f_name) is not None:
            return self._translations[f_name].strip()
        else:
            return f_name

    def getSectionHeadData(self, role):
        if role == Qt.ItemDataRole.BackgroundRole:
            return QColor(Qt.GlobalColor.darkBlue)
        elif role == Qt.ItemDataRole.FontRole:
            return QFont("Helvetica", 14, QFont.Bold)
        elif role == Qt.ItemDataRole.ForegroundRole:
            return QColor(Qt.GlobalColor.white)
        else:
            return None