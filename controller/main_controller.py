import sys
from pathlib import Path

from PySide6.QtGui import QCloseEvent, QIcon, QPixmap
from PySide6.QtWidgets import *
from pymongo.errors import ConnectionFailure

from app.dialogs.importdialog import ImportDialog
from app.windows.mainwindow import MainWindow
from config.paths import project_rooted
from dao.balance_dao import CompanyBalanceImporter
from dao.company_dao import CompanyDAO
from dao.mongodb_connector import MongoDBConnector

class MainController:
    def __init__(self, model, view: MainWindow, app):
        self._model = model
        self._view: MainWindow = view
        self._app = app

        # Codice da eseguire all'avvio dell'applicazione
        self.__startup__code()


    def __startup__code(self):
        self.dbconnectionTest()
        self.checkDataImport()

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
            # Mostro un messaggio e apro una finestra di importazione
            importDialog = ImportDialog()
            res = importDialog.exec()

            if res:
                selectedPath = importDialog.ui.selectedPathEdit.text()
                self.handleImportData(selectedPath)
                self.checkDataImport()
        else:
            status_bar = self._view.statusBar()
            widget = QWidget()
            layout = QHBoxLayout(widget)
            icn = QLabel()
            icn.setPixmap(QPixmap(project_rooted("app/resources/data-ok.png")).scaled(20, 20))
            layout.addWidget(icn)
            layout.addWidget(QLabel("Dati importati"))
            status_bar.addPermanentWidget(widget)

    def handleSayHelloButtonClick(self):
        print("Ciao " + self._view.ui.nameInput.text())
        msgBox = QMessageBox(self._view)
        msgBox.setText("Ciao " + self._view.ui.nameInput.text())
        msgBox.exec()

    def dbconnectionTest(self):
        try:
            client = MongoDBConnector.get_client()
            MongoDBConnector.ping()
            print("Test connection OK")
            status_bar = self._view.statusBar()
            widget = QWidget()
            layout = QHBoxLayout(widget)
            icn = QLabel()
            icn.setPixmap(QPixmap(project_rooted("app/resources/connected.png")).scaled(20, 20))
            layout.addWidget(icn)
            layout.addWidget(QLabel("Database connesso"))
            status_bar.addPermanentWidget(widget)
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
        print("Chiudo app")
        MongoDBConnector.close()
        event.accept()
        sys.exit(-1)

    def handleImportData(self, path):
        try:
            c = CompanyBalanceImporter(path)
            c.import_from_excel()
            company = c.company

            CompanyDAO.save_company(company)
        except:
            msgBox = QMessageBox(self._view)
            msgBox.setText("Impossibile caricare il file")
            msgBox.setInformativeText(
                "Non è stato possibile caricare il file che hai richiesto. ")
            msgBox.setIcon(QMessageBox.Icon.Critical)
            msgBox.exec()
            self._view.close()