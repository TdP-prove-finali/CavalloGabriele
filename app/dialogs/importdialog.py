from PySide6.QtCore import Slot
from PySide6.QtWidgets import QDialog, QFileDialog

from app.ui_generated.ui_import_dialog import Ui_import_dialog
from config.paths import project_rooted


class ImportDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_import_dialog()
        self.ui.setupUi(self)
        self._controller = None
        self.ui.selectedPathEdit.setText(project_rooted("dataset").__str__())
        self.ui.chosePathButton.clicked.connect(self.on_chose_file)

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    @Slot()
    def on_chose_file(self):
        print("Scegli file")
        res = QFileDialog.getOpenFileName(
            self,
            caption="Seleziona il file da importare"
        )
        if res[0] != '':
            self.ui.selectedPathEdit.setText(res[0])