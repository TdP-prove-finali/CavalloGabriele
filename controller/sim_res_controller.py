from dataclasses import asdict

from PySide6.QtWidgets import QHeaderView

from app.charts.credit_an import add_financial_evolution_chart_to_tab
from app.charts.financial_ce import create_financial_chart, add_financial_chart_to_tab
from app.charts.patrim_evol import add_patrimonial_charts_to_tab
from app.widget.resizable_vert_header import ResizableVerticalHeader
from app.windows.simresultwindow import SimResultWindow
from controller.abstract import AbstractController
from dao.translations.translation_dao import TranslationDAO
from dao.util import BalanceLocation
from model.abstract_sec_model import AbstractSectionTableModel
from model.balance_snap import BalanceSnaphot
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
        self.loadEvolPatrimCharts()

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
        self.loadIndicesTable()

    def loadEvolPatrimCharts(self):
        bal: BalanceSnaphot = self.model.balance

        add_patrimonial_charts_to_tab(
            tab=self.view.ui.struttura_sp_tab,
            attivo={
                "immobilizzazioni": bal.get_field_data("totale_immobilizzazioni_sepind_di_quelle_conc_in_loc_finanz", BalanceLocation.SP_ATTIVO),
                "rimanenze": bal.get_field_data("totale_rimanenze", BalanceLocation.SP_ATTIVO),
                "crediti": bal.get_field_data("totale_crediti", BalanceLocation.SP_ATTIVO),
                "attivita_finanziarie": bal.get_field_data("totale_attivita_finanziarie", BalanceLocation.SP_ATTIVO),
                "disponibilita_liquide": bal.get_field_data("tot_dispon_liquide", BalanceLocation.SP_ATTIVO),
            },
            passivo={
                "patrimonio_netto": bal.get_field_data("totale_fondi_rischi", BalanceLocation.SP_PASSIVO_PATRIM),
                "fondi_rischi_tfr": bal.aggregate_fields(["totale_fondi_rischi", "trattamento_di_fine_rapporto"], [BalanceLocation.SP_PASSIVO_PATRIM, BalanceLocation.SP_PASSIVO_PATRIM]),
                "altre_passivita": bal.get_field_data("ratei_e_risconti", BalanceLocation.SP_PASSIVO_DEBITI),
                "debiti_breve_termine": bal.get_debit_entro_data(),
                "debiti_lungo_termine": bal.get_debit_oltre_data()
            },
            years=bal.get_field_data("data", BalanceLocation.CE)
        )

        add_financial_evolution_chart_to_tab(
            tab=self.view.ui.creditTab,
            years=self.model.balance.get_field_data("data", BalanceLocation.CE),
            series_data={
                "Crediti entro": bal.get_cred_entro_data(),
                "Credito oltre": bal.get_cred_oltre_data()
            },
            title="Evoluzione dei crediti"
        )

        add_financial_evolution_chart_to_tab(
            tab=self.view.ui.debitTab,
            years=self.model.balance.get_field_data("data", BalanceLocation.CE),
            series_data={
                "Debiti a breve termine": bal.get_debit_entro_data(),
                "Debiti a lungo termine": bal.get_debit_oltre_data()
            },
            title="Evoluzione dei debiti"
        )

    def loadIndicesTable(self):
        wid = self.view.ui.indicesTableView
        d = asdict(self.model.indices)
        d.pop("years")
        wid.setModel(AbstractSectionTableModel(
            data=d,
            translations={
                "roi": "ROI",
                "roe": "ROE",
                "equity_ratio": "Equity Ratio",
                "asset_structure_ratio": "Indice di Rigidità degli Impieghi",
                "current_ratio": "Current Ratio",
                "ros": "ROS"
            },
            h_titles=self.model.indices.years
        )
        )
        wid.setVerticalHeader(ResizableVerticalHeader(wid))