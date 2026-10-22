from PySide6.QtWidgets import QHeaderView

from app.dialogs.balance_detail_dialog import BalanceDetailDialog
from app.widget.resizable_vert_header import ResizableVerticalHeader
from controller.abstract import AbstractController
from model.abstract_sec_model import AbstractSectionTableModel
from model.main_model import MainModel
from model.section import SPSection
from model.sp_table_model import SPTableModel

class BalanceDetailController(AbstractController[BalanceDetailDialog, MainModel, None]):

    def init(self):
        super().init()

        self.view.setWindowTitle("Dettaglio del bilancio")
        self.view.ui.companyNameLabel.setText(f"Bilancio di {self.model.company_data.company_name}")
        for y in range(1, self.model.company_data.available_years):
            self.view.ui.numberOfYearsCombo.addItem(f"{y} anni", y)

        self.loadSPTView()
        self.loadCETView()

    def handleYearsChange(self, index):
        self.view.ui.contoEconomicoTView.setModel(None)
        self.view.ui.statoPatrimTView.setModel(None)

        self.loadSPTView(index + 1)
        self.loadCETView(index + 1)
        self.view.ui.statoPatrimTView.viewport().update()
        self.view.ui.contoEconomicoTView.viewport().update()

    def loadSPTView(self, columns = None):
        c = self.model.company_data
        tr = self.model.translations
        data_model = SPTableModel(
            SPSection.fromSection(c.stato_patrimoniale), tr, max_columns=columns
        )
        self.view.ui.statoPatrimTView.setModel(data_model)
        self.view.ui.statoPatrimTView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header = ResizableVerticalHeader(self.view.ui.statoPatrimTView)
        self.view.ui.statoPatrimTView.setVerticalHeader(header)
        header.setVisible(True)

    def loadCETView(self, columns = None):
        c = self.model.company_data
        tr = self.model.translations
        data_model = AbstractSectionTableModel(
            c.conto_economico, tr, max_column_count=columns
        )
        self.view.ui.contoEconomicoTView.setModel(data_model)
        self.view.ui.contoEconomicoTView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header = ResizableVerticalHeader(self.view.ui.contoEconomicoTView)
        self.view.ui.contoEconomicoTView.setVerticalHeader(header)