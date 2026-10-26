from PySide6.QtCore import QThread, Slot
from PySide6.QtWidgets import QDialog
from app.dialogs.employee_hire_dialog import EmployeeHireDialog
from app.windows.investsimwindow import InvestSimWindow
from controller.abstract import AbstractController
from controller.simulation_controller import SimulationWorker
from model.invest_proj_model import InvestmentProjModel
from model.investment_item import InvestmentProject
from model.item_list_model import ItemListModel
from model.main_model import MainModel
from model.sim_state import GlobalParameters, SimulationState, SimulationCompleteModel


class InvestProjectController(AbstractController[InvestSimWindow, InvestmentProjModel, MainModel]):
    def handleClose(self, event):
        event.accept()

    def __init__(self, model, view, app, parent):
        super().__init__(model, view, app, parent)
        self.thread = None
        self.worker = None

    def init(self):
        super().init()
        self.view.setWindowTitle("Nuovo progetto di investimento")
        print(self.parent_model.company_data.available_years)
        model = ItemListModel(list_data = [])
        self.set_internal_pointer("model", model)
        self.view.ui.projectComponentsListView.setModel(model)
        self.view.ui.startSimBtn.clicked.connect(self.run_simulation)

    def handleRemoveItem(self):
        r = self.view.ui.projectComponentsListView.selectedIndexes()
        if len(r) > 0:
            model: ItemListModel = self.view.ui.projectComponentsListView.model()
            model.remove_item_by_index(r[0].row())
            model.layoutChanged.emit()

    def handleItemAdd(self):
        dialog = EmployeeHireDialog()
        self.set_internal_pointer("dialog", dialog)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            self.model.components.append(dialog.item)
            self.view.ui.projectComponentsListView.model().add_item(dialog.item)
            self.view.ui.projectComponentsListView.model().layoutChanged.emit()

    @Slot()
    def run_simulation(self):
        if self.thread is not None:
            return
        print("Avvio thread")
        thread = QThread(None)
        worker = SimulationWorker(SimulationCompleteModel(
            SimulationState(
                self.parent_model.company_data,
                GlobalParameters(
                    self.parent_model.company_data.fiscal_code,
                    2,
                    2026,
                    organic_growth=0.5,
                    last_available_years=self.parent_model.company_data.available_years,
                    sim_id=5
                )
            ),
            InvestmentProject(
                "test",
                "test",
                []
            )
        ),)
        self.thread = thread
        self.worker = worker
        worker.moveToThread(thread)
        thread.started.connect(worker.start)
        worker.progress.connect(self.on_progress)
        worker.finished.connect(self.on_finished)
        worker.error.connect(self.on_error)
        worker.finished.connect(thread.quit)
        worker.error.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        worker.error.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(self.on_thread_finished)
        thread.start()

    def stop(self) -> None:
        """Richiede l'arresto della simulazione."""

        if self.worker is not None:
            self.worker.request_stop()

    @Slot(float)
    def on_progress(self, progress: float) -> None:
        print("In progress "+ str(progress))

    @Slot(object)
    def on_finished(self, results: object) -> None:
        print(results)
        print("Finito")

    @Slot(str)
    def on_error(self, error: str) -> None:
        print("Errore")

    @Slot()
    def on_thread_finished(self) -> None:
        self.thread = None
        self.worker = None