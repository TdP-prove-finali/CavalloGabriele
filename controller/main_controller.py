from PySide6.QtWidgets import QMessageBox, QHeaderView

from app.widget.resizable_vert_header import ResizableVerticalHeader
from model.abstract_sec_model import AbstractSectionTableModel
from model.section import SPSection
from model.sp_table_model import SPTableModel
from app.windows.mainwindow import MainWindow
from controller.abstract import AbstractController
from dao.company_dao import CompanyDAO
from dao.translations.translation_dao import TranslationDAO
from model.main_model import MainModel


class MainController(AbstractController[MainWindow, MainModel]):

    def init(self):
        self.view.set_controller(self)
        fs_code = self.model.company_fiscal_code
        try:
            self.model._company_data = CompanyDAO.load_company(fs_code)
            self.model._translations = TranslationDAO.get_translations_for_company(self.model._company_data)
            super().init()
        except Exception as e:
            print("ERRORE: Impossibile aprire la company " + self.model.company_fiscal_code)
            print(e.__str__())
            msgBox = QMessageBox()
            msgBox.setText("Impossibile aprire l'azienda")
            msgBox.setInformativeText("Non è stato possibile caricare le informazioni dell'azienda con codice fiscale " + fs_code)
            msgBox.setIcon(QMessageBox.Icon.Critical)
            self.view.close()
            msgBox.show()
        finally:
            c = self.model.company_data
            self.view.setWindowTitle(self.model.company_data.company_name)
            self.view.ui.companyNameLabel.setText(c.company_name)
            self.view.ui.fiscalCodeLabel.setText(c.fiscal_code)
            self.view.ui.cciaaNumberLabel.setText(str(c.general_info["numero_cciaa"]))
            self.view.ui.descriptionLabel.setText(c.overview_completa["overview"])
            self.view.ui.legalFormLabel.setText(c.informazioni_commerciali_e_legali["forma_giuridica"])
            self.view.ui.lastBalanceDateLabel.setText(str(
                c.informazioni_commerciali_e_legali["data_di_chiusura_ultimo_bilancio"]))
            self.view.ui.legalAddressLabel.setText(c.anagrafica["indirizzo_sede_legale"])
            self.view.ui.operatingMarketLabel.setText(c.gruppo_dei_pari["descrizione"])
            self.view.ui.numberOfYearsLabel.setText(str(c.informazioni_commerciali_e_legali["numero_di_anni_disponibili"]))
            self.loadSummaryInfoTable()
            self.loadCETView()
            self.loadSPTView()

    def loadSPTView(self):
        c = self.model.company_data
        tr = self.model.translations
        data_model = SPTableModel(
            SPSection.fromSection(c.stato_patrimoniale), tr
        )
        self.view.ui.statoPatrimTView.setModel(data_model)
        self.view.ui.statoPatrimTView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header = ResizableVerticalHeader(self.view.ui.statoPatrimTView)
        self.view.ui.statoPatrimTView.setVerticalHeader(header)
        header.setVisible(True)

    def loadCETView(self):
        c = self.model.company_data
        tr = self.model.translations
        data_model = AbstractSectionTableModel(
            c.conto_economico, tr
        )
        self.view.ui.contoEconomicoTView.setModel(data_model)
        self.view.ui.contoEconomicoTView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header = ResizableVerticalHeader(self.view.ui.contoEconomicoTView)
        self.view.ui.contoEconomicoTView.setVerticalHeader(header)

    def loadSummaryInfoTable(self):
        c = self.model.company_data
        tr = self.model.translations
        data_model = AbstractSectionTableModel(
            c.profilo_finanziario, tr, max_column_count=2
        )
        self.view.ui.summaryTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header = self.view.ui.summaryTableView.verticalHeader()
        header.setMinimumWidth(40)
        header.setMaximumWidth(150)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.view.ui.summaryTableView.setModel(data_model)


    def handleClose(self, event):
        self.view.close()