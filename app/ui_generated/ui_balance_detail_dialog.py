# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'balance_detail_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QHBoxLayout,
    QHeaderView, QLabel, QSizePolicy, QSpacerItem,
    QTabWidget, QTableView, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1088, 613)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.companyNameLabel = QLabel(Dialog)
        self.companyNameLabel.setObjectName(u"companyNameLabel")
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(19)
        font.setBold(True)
        self.companyNameLabel.setFont(font)

        self.verticalLayout.addWidget(self.companyNameLabel)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.numberOfYearsCombo = QComboBox(Dialog)
        self.numberOfYearsCombo.setObjectName(u"numberOfYearsCombo")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.numberOfYearsCombo.sizePolicy().hasHeightForWidth())
        self.numberOfYearsCombo.setSizePolicy(sizePolicy)
        self.numberOfYearsCombo.setMinimumSize(QSize(200, 0))
        self.numberOfYearsCombo.setBaseSize(QSize(200, 0))

        self.horizontalLayout.addWidget(self.numberOfYearsCombo)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.balanceTabWidget = QTabWidget(Dialog)
        self.balanceTabWidget.setObjectName(u"balanceTabWidget")
        font1 = QFont()
        font1.setPointSize(11)
        self.balanceTabWidget.setFont(font1)
        self.conto_economico_tab = QWidget()
        self.conto_economico_tab.setObjectName(u"conto_economico_tab")
        self.horizontalLayout_11 = QHBoxLayout(self.conto_economico_tab)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.contoEconomicoTView = QTableView(self.conto_economico_tab)
        self.contoEconomicoTView.setObjectName(u"contoEconomicoTView")

        self.horizontalLayout_11.addWidget(self.contoEconomicoTView)

        self.balanceTabWidget.addTab(self.conto_economico_tab, "")
        self.stato_patrimoniale_tab = QWidget()
        self.stato_patrimoniale_tab.setObjectName(u"stato_patrimoniale_tab")
        self.horizontalLayout_12 = QHBoxLayout(self.stato_patrimoniale_tab)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.statoPatrimTView = QTableView(self.stato_patrimoniale_tab)
        self.statoPatrimTView.setObjectName(u"statoPatrimTView")

        self.horizontalLayout_12.addWidget(self.statoPatrimTView)

        self.balanceTabWidget.addTab(self.stato_patrimoniale_tab, "")

        self.verticalLayout.addWidget(self.balanceTabWidget)


        self.retranslateUi(Dialog)

        self.balanceTabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.companyNameLabel.setText(QCoreApplication.translate("Dialog", u"Bilancio di Azienda", None))
        self.numberOfYearsCombo.setCurrentText("")
        self.numberOfYearsCombo.setPlaceholderText(QCoreApplication.translate("Dialog", u"Numero di anni", None))
        self.balanceTabWidget.setTabText(self.balanceTabWidget.indexOf(self.conto_economico_tab), QCoreApplication.translate("Dialog", u"Conto Economico", None))
        self.balanceTabWidget.setTabText(self.balanceTabWidget.indexOf(self.stato_patrimoniale_tab), QCoreApplication.translate("Dialog", u"Stato Patrimoniale", None))
    # retranslateUi

