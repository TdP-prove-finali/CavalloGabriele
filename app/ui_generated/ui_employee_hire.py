# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'employee_hire.ui'
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
    QDialogButtonBox, QDoubleSpinBox, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QSizePolicy, QSpacerItem,
    QSpinBox, QTextBrowser, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.WindowModality.WindowModal)
        Dialog.resize(714, 589)
        Dialog.setModal(True)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(350, 540, 341, 32))
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

        self.groupBox_2 = QGroupBox(Dialog)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(30, 340, 281, 161))
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_10 = QLabel(self.groupBox_2)
        self.label_10.setObjectName(u"label_10")

        self.verticalLayout_3.addWidget(self.label_10)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_11 = QLabel(self.groupBox_2)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_10.addWidget(self.label_11)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_6)

        self.scaleEditNum = QDoubleSpinBox(self.groupBox_2)
        self.scaleEditNum.setObjectName(u"scaleEditNum")

        self.horizontalLayout_10.addWidget(self.scaleEditNum)


        self.verticalLayout_3.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_12 = QLabel(self.groupBox_2)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_11.addWidget(self.label_12)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_7)

        self.shapeEditNum = QDoubleSpinBox(self.groupBox_2)
        self.shapeEditNum.setObjectName(u"shapeEditNum")

        self.horizontalLayout_11.addWidget(self.shapeEditNum)


        self.verticalLayout_3.addLayout(self.horizontalLayout_11)

        self.groupBox_3 = QGroupBox(Dialog)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(380, 340, 251, 161))
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_13 = QLabel(self.groupBox_3)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_13.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_13)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_14 = QLabel(self.groupBox_3)
        self.label_14.setObjectName(u"label_14")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)

        self.horizontalLayout_9.addWidget(self.label_14)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_4)

        self.averageEditNum = QDoubleSpinBox(self.groupBox_3)
        self.averageEditNum.setObjectName(u"averageEditNum")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.averageEditNum.sizePolicy().hasHeightForWidth())
        self.averageEditNum.setSizePolicy(sizePolicy1)

        self.horizontalLayout_9.addWidget(self.averageEditNum)


        self.verticalLayout_2.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_15 = QLabel(self.groupBox_3)
        self.label_15.setObjectName(u"label_15")
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)

        self.horizontalLayout_8.addWidget(self.label_15)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_5)

        self.varianceEditNum = QDoubleSpinBox(self.groupBox_3)
        self.varianceEditNum.setObjectName(u"varianceEditNum")
        sizePolicy1.setHeightForWidth(self.varianceEditNum.sizePolicy().hasHeightForWidth())
        self.varianceEditNum.setSizePolicy(sizePolicy1)

        self.horizontalLayout_8.addWidget(self.varianceEditNum)


        self.verticalLayout_2.addLayout(self.horizontalLayout_8)

        self.widget = QWidget(Dialog)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(30, 80, 271, 166))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.horizontalLayout_4.addWidget(self.label)

        self.operationTitleEdit = QLineEdit(self.widget)
        self.operationTitleEdit.setObjectName(u"operationTitleEdit")

        self.horizontalLayout_4.addWidget(self.operationTitleEdit)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_3.addWidget(self.label_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.monthlyCostEdit = QLineEdit(self.widget)
        self.monthlyCostEdit.setObjectName(u"monthlyCostEdit")
        self.monthlyCostEdit.setMaximumSize(QSize(150, 16777215))
        self.monthlyCostEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.monthlyCostEdit)

        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_17 = QLabel(self.widget)
        self.label_17.setObjectName(u"label_17")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy2)

        self.horizontalLayout_6.addWidget(self.label_17)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)

        self.onboardingCostEdit_2 = QLineEdit(self.widget)
        self.onboardingCostEdit_2.setObjectName(u"onboardingCostEdit_2")
        sizePolicy1.setHeightForWidth(self.onboardingCostEdit_2.sizePolicy().hasHeightForWidth())
        self.onboardingCostEdit_2.setSizePolicy(sizePolicy1)
        self.onboardingCostEdit_2.setMaximumSize(QSize(150, 16777215))
        self.onboardingCostEdit_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_6.addWidget(self.onboardingCostEdit_2)

        self.label_18 = QLabel(self.widget)
        self.label_18.setObjectName(u"label_18")
        sizePolicy2.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy2)

        self.horizontalLayout_6.addWidget(self.label_18)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_2.addWidget(self.label_4)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.onboardingCostEdit = QLineEdit(self.widget)
        self.onboardingCostEdit.setObjectName(u"onboardingCostEdit")
        sizePolicy1.setHeightForWidth(self.onboardingCostEdit.sizePolicy().hasHeightForWidth())
        self.onboardingCostEdit.setSizePolicy(sizePolicy1)
        self.onboardingCostEdit.setMaximumSize(QSize(150, 16777215))
        self.onboardingCostEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.onboardingCostEdit)

        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_2.addWidget(self.label_5)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_6 = QLabel(self.widget)
        self.label_6.setObjectName(u"label_6")
        sizePolicy2.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy2)

        self.horizontalLayout_5.addWidget(self.label_6)

        self.roleComboBox = QComboBox(self.widget)
        self.roleComboBox.setObjectName(u"roleComboBox")

        self.horizontalLayout_5.addWidget(self.roleComboBox)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.widget1 = QWidget(Dialog)
        self.widget1.setObjectName(u"widget1")
        self.widget1.setGeometry(QRect(40, 510, 105, 23))
        self.horizontalLayout_7 = QHBoxLayout(self.widget1)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label_16 = QLabel(self.widget1)
        self.label_16.setObjectName(u"label_16")

        self.horizontalLayout_7.addWidget(self.label_16)

        self.stopRatioEditNum = QSpinBox(self.widget1)
        self.stopRatioEditNum.setObjectName(u"stopRatioEditNum")

        self.horizontalLayout_7.addWidget(self.stopRatioEditNum)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Assunzione nuovo dipendente", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Nota: la quota di accantonamento TFR viene calcolata in automatico utilizzando il costo mensile lordo e le aliquote ufficiali", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Assunzione nuovo dipendente", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Informazioni", None))
        self.textBrowser.setHtml(QCoreApplication.translate("Dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'.AppleSystemUIFont'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">L'investimento prevede l'assunzione di un nuovo dipendente al giorno 0 della simulazione. Tra gli effetti che apporter\u00e0 sul bilancio sono previsti: </p>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\">\n"
"<li style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0p"
                        "x;\">Pagamento mensile pari al costo lordo per l'impresa</li>\n"
"<li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Accantonamento annuale del TFR</li>\n"
"<li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Esborso iniziale pari al costo di onboarding</li>\n"
"<li style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Aumento della produttivit\u00e0 in termini di guadagno</li></ul>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label_9.setText("")
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"Hyper-performers", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Parametri della distribuzione Lomax HP", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"Scala", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"Forma", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Dialog", u"Time-to-productivity", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"Parametri della distribuzione del TTP (Normale)", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"Media", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"Varianza", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Titolo operazione", None))
        self.operationTitleEdit.setPlaceholderText(QCoreApplication.translate("Dialog", u"Assunzione grafico", None))
#if QT_CONFIG(tooltip)
        self.label_2.setToolTip(QCoreApplication.translate("Dialog", u"Costo totale mensile sostenuto dall'impresa per il dipendente (stipendio + tasse)", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Costo mensile lordo", None))
        self.monthlyCostEdit.setText(QCoreApplication.translate("Dialog", u"2000", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"\u20ac", None))
#if QT_CONFIG(tooltip)
        self.label_17.setToolTip(QCoreApplication.translate("Dialog", u"Costo una tantum speso dall'azienda per formare inizialmente il dipendente nuovo", None))
#endif // QT_CONFIG(tooltip)
        self.label_17.setText(QCoreApplication.translate("Dialog", u"Attrezzature", None))
        self.onboardingCostEdit_2.setText(QCoreApplication.translate("Dialog", u"100", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"\u20ac", None))
#if QT_CONFIG(tooltip)
        self.label_4.setToolTip(QCoreApplication.translate("Dialog", u"Costo una tantum speso dall'azienda per formare inizialmente il dipendente nuovo", None))
#endif // QT_CONFIG(tooltip)
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Costo di onboarding", None))
        self.onboardingCostEdit.setText(QCoreApplication.translate("Dialog", u"100", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"\u20ac", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Ruolo", None))
#if QT_CONFIG(tooltip)
        self.label_16.setToolTip(QCoreApplication.translate("Dialog", u"Rapporto massimo tra la produttivit\u00e0 media e quella effettiva del dipendente, per non superare l'effettiva capacit\u00e0 produttiva dell'azienda", None))
#endif // QT_CONFIG(tooltip)
        self.label_16.setText(QCoreApplication.translate("Dialog", u"Stop ratio", None))
    # retranslateUi

