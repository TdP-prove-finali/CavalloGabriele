import sys
from pathlib import Path

from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QMessageBox
from pymongo.errors import ConnectionFailure

from dao.balance_dao import CompanyBalanceImporter
from dao.company_dao import CompanyDAO
from dao.mongodb_connector import MongoDBConnector


class MainController:
    def __init__(self, model, view, app):
        self._model = model
        self._view = view
        self._app = app

        # Codice da eseguire all'avvio dell'applicazione
        self.dbconnectionTest()

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
            self.handleImportData()
        except ConnectionFailure:
            msgBox = QMessageBox(self._view)
            msgBox.setText("Errore durante la connessione al database")
            msgBox.setInformativeText("Non è stato possibile stabilire una connessione al database. Controlla che sia stato avviato. ")
            msgBox.setIcon(QMessageBox.Icon.Critical)
            msgBox.exec()
            self._view.close()

        except FileNotFoundError:
            msgBox = QMessageBox(self._view)
            msgBox.setText("Errore trovare la configurazione")
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

    def handleImportData(self):
        project_root = Path(__file__).resolve().parent.parent
        pt = project_root / "dataset" / "sample-aida-single.xlsx"
        c = CompanyBalanceImporter(pt.absolute())
        c.import_from_excel()
        company = c.company

        CompanyDAO.save_company(company)