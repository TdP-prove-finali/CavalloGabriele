from PySide6.QtWidgets import QMessageBox


class MainController:
    def __init__(self, model, view):
        self._model = model
        self._view = view

    def handleSayHelloButtonClick(self):
        print("Ciao " + self._view.ui.nameInput.text())
        msgBox = QMessageBox(self._view)
        msgBox.setText("Ciao " + self._view.ui.nameInput.text())
        msgBox.exec()