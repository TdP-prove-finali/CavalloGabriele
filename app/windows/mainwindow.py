from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow
from app.ui_generated.ui_main_window import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.sayHelloBtn.clicked.connect(self.on_pushBtnClick)

    @Slot()
    def on_pushBtnClick(self):
        print("Ciao " + self.ui.nameInput.text())

