# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sim_result.ui'
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QHeaderView,
    QMainWindow, QMenuBar, QSizePolicy, QStatusBar,
    QTabWidget, QTableView, QTextBrowser, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1273, 727)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_5 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.ceTab = QWidget()
        self.ceTab.setObjectName(u"ceTab")
        self.horizontalLayout_3 = QHBoxLayout(self.ceTab)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.contoEconomicoTView = QTableView(self.ceTab)
        self.contoEconomicoTView.setObjectName(u"contoEconomicoTView")

        self.horizontalLayout_3.addWidget(self.contoEconomicoTView)

        self.tabWidget.addTab(self.ceTab, "")
        self.spTab = QWidget()
        self.spTab.setObjectName(u"spTab")
        self.horizontalLayout_2 = QHBoxLayout(self.spTab)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.statoPatrimTView = QTableView(self.spTab)
        self.statoPatrimTView.setObjectName(u"statoPatrimTView")

        self.horizontalLayout_2.addWidget(self.statoPatrimTView)

        self.tabWidget.addTab(self.spTab, "")

        self.horizontalLayout_4.addWidget(self.tabWidget)

        self.chartSection = QGroupBox(self.centralwidget)
        self.chartSection.setObjectName(u"chartSection")
        font = QFont()
        font.setPointSize(17)
        self.chartSection.setFont(font)
        self.verticalLayout_2 = QVBoxLayout(self.chartSection)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.chartTabWidget = QTabWidget(self.chartSection)
        self.chartTabWidget.setObjectName(u"chartTabWidget")
        font1 = QFont()
        font1.setPointSize(13)
        self.chartTabWidget.setFont(font1)
        self.struttura_sp_tab = QWidget()
        self.struttura_sp_tab.setObjectName(u"struttura_sp_tab")
        self.chartTabWidget.addTab(self.struttura_sp_tab, "")
        self.evoluz_ricav_tab = QWidget()
        self.evoluz_ricav_tab.setObjectName(u"evoluz_ricav_tab")
        self.chartTabWidget.addTab(self.evoluz_ricav_tab, "")
        self.debitTab = QWidget()
        self.debitTab.setObjectName(u"debitTab")
        self.chartTabWidget.addTab(self.debitTab, "")
        self.creditTab = QWidget()
        self.creditTab.setObjectName(u"creditTab")
        self.chartTabWidget.addTab(self.creditTab, "")
        self.indicesTab = QWidget()
        self.indicesTab.setObjectName(u"indicesTab")
        self.horizontalLayout_6 = QHBoxLayout(self.indicesTab)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.indicesTableView = QTableView(self.indicesTab)
        self.indicesTableView.setObjectName(u"indicesTableView")

        self.horizontalLayout_6.addWidget(self.indicesTableView)

        self.chartTabWidget.addTab(self.indicesTab, "")

        self.verticalLayout_2.addWidget(self.chartTabWidget)


        self.horizontalLayout_4.addWidget(self.chartSection)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMaximumSize(QSize(16777215, 250))
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.logTextBrowser = QTextBrowser(self.groupBox)
        self.logTextBrowser.setObjectName(u"logTextBrowser")

        self.horizontalLayout.addWidget(self.logTextBrowser)


        self.verticalLayout.addWidget(self.groupBox)


        self.horizontalLayout_5.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1273, 30))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)
        self.chartTabWidget.setCurrentIndex(4)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ceTab), QCoreApplication.translate("MainWindow", u"Conto Economico", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.spTab), QCoreApplication.translate("MainWindow", u"Stato Patrimoniale", None))
        self.chartSection.setTitle(QCoreApplication.translate("MainWindow", u"Grafici", None))
        self.chartTabWidget.setTabText(self.chartTabWidget.indexOf(self.struttura_sp_tab), QCoreApplication.translate("MainWindow", u"Struttura SP", None))
        self.chartTabWidget.setTabText(self.chartTabWidget.indexOf(self.evoluz_ricav_tab), QCoreApplication.translate("MainWindow", u"Evoluzione ricavi", None))
        self.chartTabWidget.setTabText(self.chartTabWidget.indexOf(self.debitTab), QCoreApplication.translate("MainWindow", u"Evoluzione debiti", None))
        self.chartTabWidget.setTabText(self.chartTabWidget.indexOf(self.creditTab), QCoreApplication.translate("MainWindow", u"Evoluzione crediti", None))
        self.chartTabWidget.setTabText(self.chartTabWidget.indexOf(self.indicesTab), QCoreApplication.translate("MainWindow", u"Indici", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Log eventi simulazione", None))
    # retranslateUi

