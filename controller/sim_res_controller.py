from PySide6.QtWidgets import QHeaderView

from app.charts.financial_ce import create_financial_chart, add_financial_chart_to_tab
from app.widget.resizable_vert_header import ResizableVerticalHeader
from app.windows.simresultwindow import SimResultWindow
from controller.abstract import AbstractController
from dao.translations.translation_dao import TranslationDAO
from dao.util import BalanceLocation
from model.abstract_sec_model import AbstractSectionTableModel
from model.section import SPSection
from model.sim_output import SimulationOutput
from model.sp_table_model import SPTableModel


class SimResultController(AbstractController[SimResultWindow, SimulationOutput, None]):
    """Controller per gestire la finestra di avvio dell'applicazione.
    """
    def __init__(self, model: SimulationOutput, view, app):
        super().__init__(model, view, app)

    def init(self):
        c = ""
        for log in self.model.logs:
            c += f"{log}\n"

        self.view.ui.logTextBrowser.setText(c)
        self.view.ui.logTextBrowser.update()
        self.view.setWindowTitle(f"Risultato simulazione {self.model.id} ")
        add_financial_chart_to_tab(
            periods=self.model.balance.get_field_data("data", BalanceLocation.CE),
            revenues=self.model.balance.get_field_data("ricavi_vendite_e_prestazioni", BalanceLocation.CE),
            costs=self.model.balance.get_field_data("materie_prime_e_consumo", BalanceLocation.CE),
            extra_costs=self.model.balance.get_field_data("servizi", BalanceLocation.CE),
            extra_costs_name="Servizi",
            tab=self.view.ui.evoluz_ricav_tab
        )
        self.loadCETView()

    def loadCETView(self):
        sp, ce = self.model.balance.serialize()
        tr = TranslationDAO.get_translations_for_company(sp | ce)
        data_model = AbstractSectionTableModel(
            ce, tr
        )
        self.view.ui.contoEconomicoTView.setModel(data_model)
        self.view.ui.contoEconomicoTView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header = ResizableVerticalHeader(self.view.ui.contoEconomicoTView)
        self.view.ui.contoEconomicoTView.setVerticalHeader(header)

        data_model = SPTableModel(
            SPSection.fromSection(sp), tr
        )
        self.view.ui.statoPatrimTView.setModel(data_model)
        self.view.ui.statoPatrimTView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header = ResizableVerticalHeader(self.view.ui.statoPatrimTView)
        self.view.ui.statoPatrimTView.setVerticalHeader(header)
        self.view.ui.statoPatrimTView.resizeColumnsToContents()
        header.setVisible(True)