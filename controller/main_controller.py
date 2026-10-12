from typing import Any

from PySide6.QtWidgets import QMessageBox

from app.windows.mainwindow import MainWindow
from controller.abstract import AbstractController
from dao.company_dao import CompanyDAO
from model.main_model import MainModel


class MainController(AbstractController[MainWindow, MainModel]):

    def init(self):
        self.view.set_controller(self)
        fs_code = self.model.company_fiscal_code
        try:
            self.model._company_data = CompanyDAO.load_company(fs_code)
            self.view.setWindowTitle(self.model.company_data.company_name)
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

    def handleClose(self, event):
        self.view.close()