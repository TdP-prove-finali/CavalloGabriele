from model.model import Model

class SimulationController:
    def __init__(self, model: Model, view):        # Model e view sono istanziati nel main e passati al controller che ci lavora sopra
        self._model = model
        self._view = view                   # Puntatore ad un widget Qt (tipicamente una finestra)