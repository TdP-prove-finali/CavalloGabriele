from typing import TypeVar, Generic, Any

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication, QWidget

ModelType = TypeVar('ModelType')
T = TypeVar("T", bound=Any)

class HasModel[T]:
    """
    Rappresenta una generica classe che ha accesso ad un model di tipo T generico
    """
    def __init__(self, model: ModelType):
        self._model = model

    @property
    def model(self) -> ModelType:
        return self._model

ViewType = TypeVar('ViewType', bound=QWidget)

class AbstractController[ViewType, ModelType, ParentModelType] (HasModel, QObject):
    """
    Definisce un generico controller e le sue caratteristiche base

    Type Parameters:
        ViewType: Tipo della view che viene gestita, deve essere un QWidget di QT
        ModelType: Tipo del model gestito da questo controller
        ParentModelType: Tipo di model dell'eventuale controller parent

        L'ultimo può anche essere None nel caso in cui non ci sia un parent
    """
    def __init__(self, model, view, app, parent: HasModel | None = None):
        """
        Inizializza un nuovo controller
        :param model: Model
        :param view: View
        :param app: Puntatore alla QApplication qt per permettere di eseguire azioni su tutta l'applicazione (come stopparne l'esecuzione)
        :param parent: Puntatore al controller che ha aperto questo nuovo controller, utile per permettere di accedere al model del padre e non dover
        copiare i dati per renderli accessibili anche ad un controller figlio.
        Un esempio di utilizzo è questo:
            * MainWindow (che ha il suo controller MainWindowController) deve aprire la finestra per modificare il progetto di investimento. Questa finestra necessita di accedere
            alle informazioni di bilancio della company attualmente selezionata (presenti nel model del MainController). Per non ricopiarle e passarle al controller figlio (spawnato insieme al suo model all'apertura
            della finestra) gli si passa un puntatore al controller parent.
            Il controller figlio potrà quindi fare: `self.parent_model.company_data` per accedere alle informazioni della company, senza passarle esplicitamente.
        I controller figli non possono mai chiamare metodi sul parent per ragioni di sicurezza e pulizia.

        Nota: la classe eredita anche da QObject per permettere di gestire i thread correttamente
        """
        QObject.__init__(self)
        HasModel.__init__(self, model)
        self._view: ViewType = view
        self._app: QApplication = app
        self.__parent__ = parent
        self.__internal_pointers__ = dict()     # Dizionario con puntatori ad eventuali dati interni che il controller deve mantenere (ad esempio puntatori a finestre che ha aperto e vuole tenere in memoria)
        self.init()

    @property
    def internal_pointers(self) -> dict[str, Any]:
        return self.__internal_pointers__

    def set_internal_pointer(self, key, value):
        self.__internal_pointers__[key] = value

    def get_internal_pointer(self, key):
        return self.__internal_pointers__.get(key)

    def init(self):
        """
        Funzione chiamata all'avvio del controller (ossia quando viene visualizzato il widget per la prima volta)
        :return: None
        """
        if self._view is not None:
            self._view.show()

    def handleClose(self, event):
        """
        Gestisce la chiusura della finestra
        :return: None
        """
        pass

    def hasParent(self):
        return self.__parent__ is not None

    @property
    def parent_model(self) -> ParentModelType:
        """
        Permette di accedere al model del controller parent
        :return:
        """
        if self.__parent__ is None:
            raise Exception("Impossibile accedere al parent di un controller top level")

        return self.__parent__.model

    @property
    def view(self):
        return self._view

    @property
    def app(self):
        return self._app