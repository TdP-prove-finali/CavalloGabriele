import random

from PySide6.QtCore import QThread, Slot, Qt
from PySide6.QtWidgets import QDialog, QApplication, QMessageBox, QMenu
from app.dialogs.asset_dialog import AssetDialog
from app.dialogs.employee_hire_dialog import EmployeeHireDialog
from app.dialogs.funding_dialog import FundingDialog
from app.dialogs.op_improvement_dialog import OperativeImprovementDialog
from app.windows.investsimwindow import InvestSimWindow
from controller.abstract import AbstractController
from controller.simulation_controller import SimulationWorker
from dao.simulation.simulation_dao import SimulationDAO
from dao.util import format_number, parse
from model.invest_proj_model import InvestmentProjModel
from model.investment_item import InvestmentProject
from model.item_list_model import ItemListModel
from model.main_model import MainModel
from model.raw_company_data import BalanceSnaphot
from model.sim_output import SimulationOutput
from model.sim_state import GlobalParameters, SimulationState, SimulationCompleteModel

class InvestProjectController(AbstractController[InvestSimWindow, InvestmentProjModel, MainModel]):
    def handleClose(self, event):
        event.accept()

    def __init__(self, model, view, app, parent):
        super().__init__(model, view, app, parent)
        self.thread = None
        self.worker = None

    def init(self):
        self.view.setWindowTitle("Nuovo progetto di investimento")
        model = ItemListModel(list_data = [])
        self.set_internal_pointer("model", model)
        self.view.ui.companyNameEdit.setText(self.parent_model.company_data.company_name)
        self.view.ui.lastAvYearsLabel.setText(str(self.parent_model.company_data.available_years))
        self.view.ui.simStatusBar.setVisible(False)
        self.view.ui.stopSimBtn.setVisible(False)
        self.view.ui.projectComponentsListView.setModel(model)
        self.view.ui.startSimBtn.clicked.connect(self.run_simulation)

        menu = QMenu(self.view.ui.newComponentBtn)
        action1 = menu.addAction("Assunzione dipendente")
        action2 = menu.addAction("Acquisto cespiti")
        action3 = menu.addAction("Finanziamento")
        action4 = menu.addAction("Efficientamento operazioni")
        action1.triggered.connect(self.handleCreateEmployee)
        action2.triggered.connect(self.handleCreateCespiti)
        action3.triggered.connect(self.handleCreateFinancial)
        action4.triggered.connect(self.handleCreateEffic)

        v = self.parent_model.company_data.stato_patrimoniale["subsections"]["attivo"]["civ_tot_dispon_liquide"][0] * 1.00
        if "migl" in self.parent_model.company_data.stato_patrimoniale["moneta"][0]:
            v = v * 1000
        self.view.ui.liquidAvailabilityLabel.setText(format_number(v) + " €")
        self.__update_stats()

        self.view.ui.newComponentBtn.setMenu(menu)
        super().init()

    @Slot()
    def handleCreateEmployee(self):
        dialog = EmployeeHireDialog()
        self.set_internal_pointer("dialog", dialog)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            self.__append_component(dialog.item)

    def __append_component(self, component):
        self.model.components.append(component)
        self.view.ui.projectComponentsListView.model().add_item(component)
        self.view.ui.projectComponentsListView.model().layoutChanged.emit()
        self.__update_stats()

    def __update_stats(self):
        e = InvestmentProject.total_expenditure(self.model.components)
        f = InvestmentProject.total_funding_request(self.model.components)

        self.view.ui.totalEsbLabel.setText(format_number(e) + "€")
        self.view.ui.totalFundingLabel.setText(format_number(f) + "€")


    @Slot()
    def handleCreateCespiti(self):
        dialog = AssetDialog()
        self.set_internal_pointer("dialog", dialog)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            self.__append_component(dialog.item)

    @Slot()
    def handleCreateFinancial(self):
        dialog = FundingDialog()
        self.set_internal_pointer("dialog", dialog)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            self.__append_component(dialog.item)

    @Slot()
    def handleCreateEffic(self):
        dialog = OperativeImprovementDialog()
        self.set_internal_pointer("dialog", dialog)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            self.__append_component(dialog.item)

    def handleRemoveItem(self):
        r = self.view.ui.projectComponentsListView.selectedIndexes()
        if len(r) > 0:
            self.model.components.remove(self.model.components[r[0].row()])
            model: ItemListModel = self.view.ui.projectComponentsListView.model()
            model.remove_item_by_index(r[0].row())
            model.layoutChanged.emit()

        self.__update_stats()

    @Slot()
    def run_simulation(self):
        """
        Avvia la simulazione, lanciandola su un thread separato per permettere l'aggiornamento
        della UI senza blocchi (può essere anche molto pesante).
        L'esecuzione è controllata da SimulationWorker, classe che ne gestisce l'esecuzione e comunica al thread principale
        con dei segnali, ricevuti dagli appositi slot in questo controller.
        :return:
        """
        if self.thread is not None:
            return

        params = GlobalParameters(
            selected_company=self.parent_model.company_data.fiscal_code,
            number_of_years=parse(self.view.ui.numberOfYears.text()),
            initial_year=parse(self.view.ui.startingYearEdit.text()),
            organic_growth=parse(self.view.ui.organicGrowthSpin.text()),
            last_available_years=self.parent_model.company_data.available_years,
            sim_id=SimulationDAO.create_sim_id()
        )

        print("Avvio thread")
        self.view.ui.simStatusBar.setValue(0)
        self.view.ui.simStatusBar.setVisible(True)
        thread = QThread(None)
        worker = SimulationWorker(SimulationCompleteModel(
            SimulationState(
                self.parent_model.company_data,
                params
            ),
            InvestmentProject(
                self.view.ui.projectTitleLineEdit.text(),
                self.view.ui.projectDescription.toHtml(),
                [],
                items=self.model.components
            )
        ),)
        self.thread = thread
        self.worker = worker
        worker.moveToThread(thread)
        thread.started.connect(worker.start)
        worker.progress.connect(self.on_progress, Qt.ConnectionType.QueuedConnection)
        worker.finished.connect(self.on_finished , Qt.ConnectionType.QueuedConnection)
        worker.error.connect(self.on_error, Qt.ConnectionType.QueuedConnection)
        worker.finished.connect(thread.quit)
        worker.error.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        worker.error.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater, Qt.ConnectionType.QueuedConnection)
        thread.finished.connect(self.on_thread_finished, Qt.ConnectionType.QueuedConnection)
        thread.start()

    def stop(self) -> None:
        """Richiede l'arresto della simulazione."""

        if self.worker is not None:
            self.worker.request_stop()

    @Slot(float)
    def on_progress(self, progress: float) -> None:
        assert (
                QThread.currentThread()
                == QApplication.instance().thread()
        ), "Progress bar aggiornata fuori dal thread principale"

        self.view.ui.simStatusBar.setValue(int(progress*100))
        print("In progress "+ str(progress))

    @Slot(object)
    def on_finished(self, results: SimulationOutput) -> None:
        """
        Segnale inviato quando la simulazione è terminata.
        Contiene l'ultimo snapshot di bilancio generato
        :param results:
        :return:
        """
        print(results)
        print("Finito")
        self.view.ui.simStatusBar.setValue(100)

    @Slot(str)
    def on_error(self, error: str) -> None:
        msgBox = QMessageBox()
        msgBox.setText("Errore durante la simulazione")
        msgBox.setInformativeText(error)
        msgBox.setIcon(QMessageBox.Icon.Critical)
        msgBox.show()
        print("Errore durante la simulazione " + error)

    @Slot()
    def on_thread_finished(self) -> None:
        self.thread = None
        self.worker = None