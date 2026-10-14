from PySide6.QtCore import QObject, Signal

from model.raw_company_data import RawCompanyData


class BalanceImporterSignals(QObject):
    finished = Signal(int)
    error = Signal(tuple)
    result = Signal(RawCompanyData)
    progress = Signal(tuple)
