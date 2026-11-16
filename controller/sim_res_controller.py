
from typing import Any
from app.windows.simresultwindow import SimResultWindow
from controller.abstract import AbstractController
from model.sim_output import SimulationOutput


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