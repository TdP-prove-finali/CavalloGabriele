# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'import_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.11.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_import_dialog(object):
    def setupUi(self, import_dialog):
        if not import_dialog.objectName():
            import_dialog.setObjectName(u"import_dialog")
        import_dialog.resize(400, 300)
        import_dialog.setModal(True)
        self.verticalLayout = QVBoxLayout(import_dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(import_dialog)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(19)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.label_2 = QLabel(import_dialog)
        self.label_2.setObjectName(u"label_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QSize(300, 0))
        self.label_2.setMaximumSize(QSize(300000, 16777215))
        self.label_2.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_3 = QLabel(import_dialog)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.selectedPathEdit = QLineEdit(import_dialog)
        self.selectedPathEdit.setObjectName(u"selectedPathEdit")

        self.horizontalLayout.addWidget(self.selectedPathEdit)

        self.chosePathButton = QPushButton(import_dialog)
        self.chosePathButton.setObjectName(u"chosePathButton")

        self.horizontalLayout.addWidget(self.chosePathButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(import_dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(import_dialog)
        self.buttonBox.accepted.connect(import_dialog.accept)
        self.buttonBox.rejected.connect(import_dialog.reject)

        QMetaObject.connectSlotsByName(import_dialog)
    # setupUi

    def retranslateUi(self, import_dialog):
        import_dialog.setWindowTitle(QCoreApplication.translate("import_dialog", u"Importazione dati", None))
        self.label.setText(QCoreApplication.translate("import_dialog", u"Importazione dati", None))
        self.label_2.setText(QCoreApplication.translate("import_dialog", u"Attualmente il database locale a cui sei connesso non contiene dati di aziende. Per utilizzare l'applicazione e fare simulazioni devi importare delle aziende a partire da uno o pi\u00f9 file Excel", None))
        self.label_3.setText(QCoreApplication.translate("import_dialog", u"Percorso file", None))
        self.chosePathButton.setText(QCoreApplication.translate("import_dialog", u"...", None))
    # retranslateUi

