import sys
from typing import Any

import PySide6
from PySide6.QtCore import QThread, Slot
from PySide6.QtGui import QCloseEvent, QPixmap, Qt
from PySide6.QtWidgets import *
from pymongo.errors import ConnectionFailure

from app.dialogs.importdialog import ImportDialog
from app.windows.mainwindow import MainWindow
from app.windows.startupwindow import StartupWindow
from config.paths import project_rooted
from controller.abstract import AbstractController
from controller.main_controller import MainController
from dao.data_import.company_import_dao import CompanyImportDAO
from dao.company_dao import CompanyDAO
from dao.mongodb_connector import MongoDBConnector
from model.main_model import MainModel
from model.raw_company_data import CompanyData


class StartupController(AbstractController[StartupWindow, Any, None]):
    """Controller per gestire la finestra di avvio dell'applicazione.
    """
    def __init__(self, model, view, app):
        super().__init__(model, view, app)
        self.number = 20
        self._main_win_controller: MainController | None = None
        self.thread_ptr = None
        self.worker = None

    def init(self):
        self.__resize_logo__()

        pixMap = QPixmap((project_rooted("app") / "resources" / "business_scenario_lab_icon.png").__str__())
        self._view.ui.centralwidget.setWindowIcon(
            pixMap.scaled(
                50,
                50,
                PySide6.QtCore.Qt.AspectRatioMode.KeepAspectRatio
            )
        )
        self._view.ui.importStatusBar.setVisible(False)
        self._view.ui.importProgressLabel.setVisible(False)
        self.dbconnectionTest()
        self.checkDataImport()
        self.__load_dd_options__()

    def __load_dd_options__(self):
        briefs = CompanyDAO.find_all_companies(sorted=True)
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
            # Nota: il msgbox non deve essere bloccante perchè altrimenti non viene terminato l'init e causa problemi con l'avvio del thread
            msgBox = QMessageBox()
            msgBox.setText("Dati non ancora importati")
            msgBox.setIcon(QMessageBox.Icon.Warning)
            msgBox.setInformativeText("I dati devono essere importati nel database locale per essere utilizzati e fare simulazioni. ")
            importButton = msgBox.addButton("Importa dati", QMessageBox.ButtonRole.ActionRole)
            msgBox.buttonClicked.connect(
                lambda button: (
                    self.handleImportDialog()
                    if button == importButton
                    else None
                )
            )
            msgBox.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
            msgBox.show()
            self.set_internal_pointer("msg-box", msgBox)
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
            self._main_win_controller = MainController(
                model=MainModel(fiscal_code),
                view=MainWindow(),
                app=self.app
            )
        else:
            msgBox = QMessageBox()
            msgBox.setText("Nessuna azienda selezionata")
            msgBox.setInformativeText("Non hai selezionato nessuna azienda da aprire. Selezionane una e riprova. ")
            msgBox.setIcon(QMessageBox.Icon.Warning)
            msgBox.exec()

    def __handleImportData__(self, path: str) -> None:
        if not path:
            QMessageBox.critical(
                self._view,
                "Nessun file selezionato",
                "Non hai selezionato nessun file da importare."
            )
            return

        if self.thread_ptr is not None:
            QMessageBox.warning(self._view,"Importazione in corso","Non puoi avviare una nuova importazione mentre una è già in corso. ")
            return

        self._view.ui.importStatusBar.setVisible(True)
        self._view.ui.importProgressLabel.setVisible(True)
        self._view.ui.importStatusBar.setValue(0)

        thread = QThread()
        worker = CompanyImportDAO(path)
        self.thread_ptr = thread
        self.worker = worker
        worker.moveToThread(thread)
        thread.started.connect(worker.start)
        worker.progress.connect(self.on_progress,Qt.ConnectionType.QueuedConnection)
        worker.finished.connect(self.on_finish,Qt.ConnectionType.QueuedConnection)
        worker.error.connect(self.on_error,Qt.ConnectionType.QueuedConnection)
        worker.finished.connect(thread.quit)
        worker.error.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        worker.error.connect(worker.deleteLater)
        thread.finished.connect(self.on_thread_finished,Qt.ConnectionType.QueuedConnection)
        thread.start()

    @Slot(int)
    def on_progress(self, value):
        print(value)
        self._view.ui.importStatusBar.setValue(value)

    @Slot()
    def on_finish(self, result: list[CompanyData]):
        self.__load_dd_options__()
        msgBox = QMessageBox(self._view)
        msgBox.setText(f"{len(result)} nuove aziende caricate correttamente. ")
        msgBox.setInformativeText(
            "Il caricamento dei dati dal file ha avuto successo. ")
        msgBox.setIcon(QMessageBox.Icon.Information)
        msgBox.exec()

    @Slot(str)
    def on_error(self, error: str) -> None:
        msgBox = QMessageBox()
        msgBox.setText("Errore durante l'importazione dei dati")
        msgBox.setInformativeText(error)
        msgBox.setIcon(QMessageBox.Icon.Critical)
        msgBox.show()
        self.set_internal_pointer("msg-box", msgBox)
        print("Errore durante l'import dei dati " + error)

    @Slot()
    def on_thread_finished(self) -> None:
        thread = self.sender()
        if thread is None:
            return
        if thread is not self.thread_ptr:
            return
        self.thread_ptr = None
        self.worker = None
        thread.deleteLater()