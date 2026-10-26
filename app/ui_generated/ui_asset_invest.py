# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'asset_invest.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QSizePolicy, QSpacerItem, QTextBrowser,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.WindowModality.WindowModal)
        Dialog.resize(714, 589)
        Dialog.setMinimumSize(QSize(714, 589))
        Dialog.setMaximumSize(QSize(714, 589))
        Dialog.setModal(True)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(350, 530, 341, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.label_7 = QLabel(Dialog)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(40, 260, 281, 61))
        self.label_7.setWordWrap(True)
        self.label_8 = QLabel(Dialog)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(240, 20, 260, 23))
        font = QFont()
        font.setPointSize(19)
        font.setBold(True)
        self.label_8.setFont(font)
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(380, 70, 319, 211))
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.textBrowser = QTextBrowser(self.groupBox)
        self.textBrowser.setObjectName(u"textBrowser")

        self.horizontalLayout.addWidget(self.textBrowser)

        self.label_9 = QLabel(self.groupBox)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setWordWrap(True)

        self.horizontalLayout.addWidget(self.label_9)

        self.layoutWidget = QWidget(Dialog)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(30, 80, 271, 166))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout_4.addWidget(self.label)

        self.operationTitleEdit = QLineEdit(self.layoutWidget)
        self.operationTitleEdit.setObjectName(u"operationTitleEdit")

        self.horizontalLayout_4.addWidget(self.operationTitleEdit)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_3.addWidget(self.label_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.totalCostEdit = QLineEdit(self.layoutWidget)
        self.totalCostEdit.setObjectName(u"totalCostEdit")
        self.totalCostEdit.setMaximumSize(QSize(150, 16777215))
        self.totalCostEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.totalCostEdit)

        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_17 = QLabel(self.layoutWidget)
        self.label_17.setObjectName(u"label_17")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy)

        self.horizontalLayout_6.addWidget(self.label_17)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)

        self.durationYearsEdit = QLineEdit(self.layoutWidget)
        self.durationYearsEdit.setObjectName(u"durationYearsEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.durationYearsEdit.sizePolicy().hasHeightForWidth())
        self.durationYearsEdit.setSizePolicy(sizePolicy1)
        self.durationYearsEdit.setMaximumSize(QSize(150, 16777215))
        self.durationYearsEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_6.addWidget(self.durationYearsEdit)

        self.label_18 = QLabel(self.layoutWidget)
        self.label_18.setObjectName(u"label_18")
        sizePolicy.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy)

        self.horizontalLayout_6.addWidget(self.label_18)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_4 = QLabel(self.layoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_2.addWidget(self.label_4)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.maintenanceCostEdit = QLineEdit(self.layoutWidget)
        self.maintenanceCostEdit.setObjectName(u"maintenanceCostEdit")
        sizePolicy1.setHeightForWidth(self.maintenanceCostEdit.sizePolicy().hasHeightForWidth())
        self.maintenanceCostEdit.setSizePolicy(sizePolicy1)
        self.maintenanceCostEdit.setMaximumSize(QSize(150, 16777215))
        self.maintenanceCostEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.maintenanceCostEdit)

        self.label_5 = QLabel(self.layoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_2.addWidget(self.label_5)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_6 = QLabel(self.layoutWidget)
        self.label_6.setObjectName(u"label_6")
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)

        self.horizontalLayout_5.addWidget(self.label_6)

        self.assetTypeCombo = QComboBox(self.layoutWidget)
        self.assetTypeCombo.addItem("")
        self.assetTypeCombo.addItem("")
        self.assetTypeCombo.setObjectName(u"assetTypeCombo")
        self.assetTypeCombo.setEditable(True)

        self.horizontalLayout_5.addWidget(self.assetTypeCombo)


        self.verticalLayout.addLayout(self.horizontalLayout_5)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Acquisto nuovo cespite", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Nota: la quota di ammortamento annuale del cespite viene calcolata in automatico utilizzando l'ammortamento fisso", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Acquisto di un cespite", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Informazioni", None))
        self.textBrowser.setHtml(QCoreApplication.translate("Dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'.AppleSystemUIFont'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">L'investimento prevede l'acquisto di un cespite con una determinata durata). Tra gli effetti che apporter\u00e0 sul bilancio sono previsti: </p>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\">\n"
"<li style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Pagament"
                        "o annuale della quota di ammortamento</li>\n"
"<li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Accantonamento in apposito fondo</li>\n"
"<li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Esborso dei costi di manutenzione se presenti</li>\n"
"<li style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Aumento delle immobilizzazioni</li></ul>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label_9.setText("")
        self.label.setText(QCoreApplication.translate("Dialog", u"Titolo operazione*", None))
        self.operationTitleEdit.setPlaceholderText(QCoreApplication.translate("Dialog", u"Assunzione grafico", None))
#if QT_CONFIG(tooltip)
        self.label_2.setToolTip(QCoreApplication.translate("Dialog", u"Costo totale mensile sostenuto dall'impresa per il dipendente (stipendio + tasse)", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Costo complessivo*", None))
        self.totalCostEdit.setInputMask("")
        self.totalCostEdit.setText("")
        self.label_3.setText(QCoreApplication.translate("Dialog", u"\u20ac", None))
#if QT_CONFIG(tooltip)
        self.label_17.setToolTip(QCoreApplication.translate("Dialog", u"Costo una tantum speso dall'azienda per formare inizialmente il dipendente nuovo", None))
#endif // QT_CONFIG(tooltip)
        self.label_17.setText(QCoreApplication.translate("Dialog", u"Durata", None))
        self.durationYearsEdit.setText(QCoreApplication.translate("Dialog", u"100", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"anni", None))
#if QT_CONFIG(tooltip)
        self.label_4.setToolTip(QCoreApplication.translate("Dialog", u"Costo una tantum speso dall'azienda per formare inizialmente il dipendente nuovo", None))
#endif // QT_CONFIG(tooltip)
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Costo di manutenzione*", None))
        self.maintenanceCostEdit.setText(QCoreApplication.translate("Dialog", u"100", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"\u20ac", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Tipo*", None))
        self.assetTypeCombo.setItemText(0, QCoreApplication.translate("Dialog", u"Materiale", None))
        self.assetTypeCombo.setItemText(1, QCoreApplication.translate("Dialog", u"Immateriale", None))

    # retranslateUi

