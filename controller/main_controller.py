import sys
from pathlib import Path

import PySide6
from PySide6.QtGui import QCloseEvent, QPixmap
from PySide6.QtWidgets import *
from pymongo.errors import ConnectionFailure

from app.dialogs.importdialog import ImportDialog
from app.windows.mainwindow import MainWindow
from app.windows.startupwindow import StartupWindow
from config.paths import project_rooted
from dao.data_import.company_import_dao import CompanyImportDAO
from dao.company_dao import CompanyDAO
from dao.mongodb_connector import MongoDBConnector


class MainController:
    def __init__(self, model, view: StartupWindow, app):
        self._model = model
        self._view: StartupWindow = view
        self._app = app
        self._main_window = None

        # Codice da eseguire all'avvio dell'applicazione
        self.__startup__code()

    def __startup__code(self):
        self.__resize_logo__()

        pixMap = QPixmap((project_rooted("app") / "resources" / "business_scenario_lab_icon.png").__str__())
        self._view.ui.centralwidget.setWindowIcon(
            pixMap.scaled(
                50,
                50,
                PySide6.QtCore.Qt.AspectRatioMode.KeepAspectRatio
            )
        )
        self.dbconnectionTest()
        self.checkDataImport()
        self.__load_dd_options__()

    def __load_dd_options__(self):
        briefs = CompanyDAO.find_all_companies()
        self._view.ui.companyComboBox.clear()
        for b in briefs:
            self._view.ui.companyComboBox.addItem(b.company_name, b.fiscal_code)

    def __resize_logo__(self):
        pixMap = QPixmap((project_rooted("app") / "resources" / "business_scenario_lab_logo.png").__str__())
        self._view.ui.pictureBox.setPixmap(pixMap.scaled(
            self._view.ui.pictureBox.width(),
            self._view.ui.pictureBox.height(),
            PySide6.QtCore.Qt.AspectRatioMode.KeepAspectRatio
        ))

    def checkDataImport(self):
        """Controlla che i dati per l'applicazione siano stati correttamente importati"""
        briefs = CompanyDAO.find_all_companies()

        if len(briefs) == 0:
            # I dati devono ancora essere importati
            msgBox = QMessageBox()
            msgBox.setText("Dati non ancora importati")
            msgBox.setIcon(QMessageBox.Icon.Warning)
            msgBox.setInformativeText("I dati devono essere importati nel database locale per essere utilizzati e fare simulazioni. ")
            msgBox.addButton("Importa dati", QMessageBox.ButtonRole.ActionRole)
            msgBox.exec()

            self.handleImportDialog()
        else:
            status_bar = self._view.statusBar()
            widget = self._view.data_status_widget
            layout = widget.layout()

            if layout is None:
                layout = QHBoxLayout(widget)
            icn = QLabel()
            icn.setPixmap(QPixmap(project_rooted("app/resources/data-ok.png")).scaled(20, 20))
            layout.addWidget(icn)
            layout.addWidget(QLabel(str(len(briefs)) + " aziende importate"))
            status_bar.addPermanentWidget(widget)

    def handleImportDialog(self):
        # Mostro un messaggio e apro una finestra di importazione
        importDialog = ImportDialog()
        res = importDialog.exec()

        if res:
            selectedPath = importDialog.ui.selectedPathEdit.text()
            self.__handleImportData__(selectedPath)
            self.checkDataImport()
            self.__load_dd_options__()

    def dbconnectionTest(self):
        try:
            client = MongoDBConnector.get_client()
            MongoDBConnector.ping()
            print("Test connection OK")
            status_bar = self._view.statusBar()
            layout = QHBoxLayout(self._view.connection_status_widget)
            icn = QLabel()
            icn.setPixmap(QPixmap(project_rooted("app/resources/connected.png")).scaled(20, 20))
            layout.addWidget(icn)
            layout.addWidget(QLabel("Database connesso"))
            status_bar.addPermanentWidget(self._view.connection_status_widget)
        except ConnectionFailure:
            msgBox = QMessageBox(self._view)
            msgBox.setText("Errore durante la connessione al database")
            msgBox.setInformativeText("Non è stato possibile stabilire una connessione al database. Controlla che sia stato avviato. ")
            msgBox.setIcon(QMessageBox.Icon.Critical)
            msgBox.exec()
            self._view.close()

        except FileNotFoundError:
            msgBox = QMessageBox(self._view)
            msgBox.setText("Impossibile trovare la configurazione")
            msgBox.setInformativeText(
                "Non è stato possibile trovare il file di configurazione per connettersi al database. Controlla di averlo impostato. ")
            msgBox.setIcon(QMessageBox.Icon.Critical)
            msgBox.exec()
            self._view.close()

    def handleClose(self, event: QCloseEvent):
        MongoDBConnector.close()
        event.accept()
        sys.exit(-1)

    def handleLoadCompany(self):
        fiscal_code = self._view.ui.companyComboBox.currentData()

        if fiscal_code is not None:
            self._main_window = MainWindow(fiscal_code)
            self._main_window.show()

    def __handleImportData__(self, path):
        if path is None or path == "":
            msgBox = QMessageBox()
            msgBox.setText("Nessun file selezionato")
            msgBox.setInformativeText("Non hai selezionato nessun file da importare. ")
            msgBox.setIcon(QMessageBox.Icon.Critical)
            msgBox.exec()
            return

        try:
            c = CompanyImportDAO(path)
            c.import_single_company()
            company = c.company
            CompanyDAO.save_company(company)
            translations = c.translations

        except Exception as e:
            print("WARNING: Eccezione durante l'importazione: " + e.__str__())
            msgBox = QMessageBox(self._view)
            msgBox.setText("Impossibile caricare il file")
            msgBox.setInformativeText(
                "Non è stato possibile caricare il file che hai richiesto. Controlla che esista e che non ci siano errori di battitura. Si accettano file Excel (.xlsx). Controlla inoltre che la struttura interna rispetti quella richiesta. ")
            msgBox.setIcon(QMessageBox.Icon.Critical)
            msgBox.exec()
