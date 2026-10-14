from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtGui import QColor, QFont

from dao.util import is_number, format_number
from model.section import SPSection


class SPTableModel(QAbstractTableModel):
    def __init__(self, data: SPSection, translations: dict):
        QAbstractTableModel.__init__(self)
        self.row_count = len(data.patrimonio_netto.keys()) + len(data.debiti.keys()) + len(data.attivo) + 2
        self.column_count = len(data.context["data"])
        self._data = data
        self._translations = translations

    def rowCount(self, parent=QModelIndex()):
        return self.row_count

    def columnCount(self, parent=QModelIndex()):
        return self.column_count

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        # TODO: Gestire altezza righe e word-wrap
        # TODO: Finire implementazione
        # Per ogni sotto-sezione, mettere intestazione con colore diverso e contenuto della riga vuoto
        column = index.column()
        row = index.row()
        d = None

        if role == Qt.ItemDataRole.DisplayRole:
            field_name = None
            if row == 0:
                return None
            elif row <= self._data.count_attivo_fields:
                field_name = self._data.get_attivo_key(row - 1)
                if field_name == "subsections":
                    return None
                d = self._data.attivo[field_name][column]
            elif row == self._data.count_attivo_fields:     # Totale attivo
                return None
            elif row == self._data.count_attivo_fields + 1:      # Inizio del passivo
                return None
            elif self._data.count_attivo_fields + 1 < row <= self._data.count_attivo_fields + self._data.count_patrimon_fields + 1:
                field_name = self._data.get_patrimn_key(row - self._data.count_attivo_fields - 2)
                d = self._data.patrimonio_netto[field_name][column]
            elif self._data.count_attivo_fields + self._data.count_patrimon_fields < row <= self._data.count_attivo_fields + self._data.count_patrimon_fields + self._data.count_debiti_fields + 1:
                field_name = self._data.get_debiti_key(row - self._data.count_attivo_fields - 2 - self._data.count_patrimon_fields)
                d = self._data.debiti[field_name][column]
            if d is not None:
                if is_number(d):
                    return format_number(d)
                return d
            else:
                return "n.d."
        elif (role != Qt.ItemDataRole.DisplayRole and row == 0 or
              row == self._data.count_attivo_fields):
            return self.getSectionHeadData(role)
        elif role == Qt.ItemDataRole.BackgroundRole:
            return QColor(Qt.GlobalColor.darkGray)
        elif role == Qt.ItemDataRole.FontRole:
            return QColor(Qt.GlobalColor.white)
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignRight

        return None

    def headerData(self, section, orientation, role):
        # TODO: Header con le sotto-sezioni dello SP
        # TODO: Utilizzare il TooltipRole per mostrare un tooltip delle sezioni più importanti
        # Ad esempio con lista hard-coded di descrizioni complete sulle cose più dettagliate
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return "Anno " + str(2026 - section - 1)
            elif orientation == Qt.Orientation.Vertical:
                if section == 0:
                    return "Attivo"
                elif section <= self._data.count_attivo_fields:
                    field_name = self._data.get_attivo_key(section - 1)
                    if self._translations.get(field_name) is not None:
                        return self._translations[field_name].strip()
                    else:
                        return field_name
                elif section == self._data.count_attivo_fields + 1:
                    return "Passivo"
                elif self._data.count_attivo_fields + 1 < section <= self._data.count_attivo_fields + self._data.count_patrimon_fields + 1:
                    field_name = self._data.get_patrimn_key(section - self._data.count_attivo_fields - 2)
                    if self._translations.get(field_name) is not None:
                        return self._translations[field_name]
                    else:
                        return field_name
                elif self._data.count_attivo_fields + self._data.count_patrimon_fields < section <= self._data.count_attivo_fields + self._data.count_patrimon_fields + self._data.count_debiti_fields + 1:
                    field_name = self._data.get_debiti_key(
                        section - self._data.count_attivo_fields - 2 - self._data.count_patrimon_fields)
                    if self._translations.get(field_name) is not None:
                        return self._translations[field_name]
                    else:
                        return field_name


        elif (role != Qt.ItemDataRole.DisplayRole and (section == 0 or
              section == self._data.count_attivo_fields) or section == (self._data.count_attivo_fields + 1)):
            return self.getSectionHeadData(role)


    def getSectionHeadData(self, role):
        if role == Qt.ItemDataRole.BackgroundRole:
            return QColor(Qt.GlobalColor.darkBlue)
        elif role == Qt.ItemDataRole.FontRole:
            return QFont("Helvetica", 14, QFont.Bold)
        elif role == Qt.ItemDataRole.ForegroundRole:
            return QColor(Qt.GlobalColor.white)
        else:
            return None