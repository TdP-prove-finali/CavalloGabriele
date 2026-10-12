from typing import TypeVar, Generic
from PySide6.QtWidgets import QApplication, QWidget

ViewType = TypeVar('ViewType', bound=QWidget)
ModelType = TypeVar('ModelType')

class AbstractController(Generic[ViewType, ModelType]):
    """
    Definisce un generico controller e le sue caratteristiche base
    """
    def __init__(self, model, view, app):
        self._model: ModelType = model
        self._view: ViewType = view
        self._app: QApplication = app

        self.init()

    def init(self):
        """
        Funzione chiamata all'avvio del controller (ossia quando viene visualizzato il widget per la prima volta)
        :return: None
        """
        self._view.show()

    def handleClose(self, event):
        """
        Gestisce la chiusura della finestra
        :return: None
        """
        pass

    @property
    def model(self) -> ModelType:
        return self._model

    @property
    def view(self):
        return self._view

    @property
    def app(self):
        return self._app