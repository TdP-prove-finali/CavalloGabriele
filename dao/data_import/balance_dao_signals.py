from PySide6.QtCore import QObject, Signal

from model.RawCompanyData import RawCompanyData


class BalanceImporterSignals(QObject):
    finished = Signal(int)
    error = Signal(tuple)
    result = Signal(RawCompanyData)
    progress = Signal(tuple)
