# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.11.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QMainWindow, QMenu,
    QMenuBar, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QStatusBar, QTabWidget, QTableView,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1621, 938)
        MainWindow.setStyleSheet(u"QLabel[cssClass=\"number-label\"] {\n"
"	padding: 5px;\n"
"	background-color: rgb(18, 65, 255);\n"
"	border-radius: 5px;\n"
"	font-style: italic;\n"
"}")
        self.actionImportazione = QAction(MainWindow)
        self.actionImportazione.setObjectName(u"actionImportazione")
        self.actionCambia_impresa = QAction(MainWindow)
        self.actionCambia_impresa.setObjectName(u"actionCambia_impresa")
        self.actionChiudi = QAction(MainWindow)
        self.actionChiudi.setObjectName(u"actionChiudi")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_19 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.overviewSecWidget = QWidget(self.centralwidget)
        self.overviewSecWidget.setObjectName(u"overviewSecWidget")
        self.overviewSecWidget.setMaximumSize(QSize(400, 16777215))
        self.horizontalLayout_18 = QHBoxLayout(self.overviewSecWidget)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(0, 0, 0, -1)
        self.overviewSection = QVBoxLayout()
        self.overviewSection.setObjectName(u"overviewSection")
        self.companyNameLabel = QLabel(self.overviewSecWidget)
        self.companyNameLabel.setObjectName(u"companyNameLabel")
        font = QFont()
        font.setPointSize(26)
        font.setBold(True)
        self.companyNameLabel.setFont(font)

        self.overviewSection.addWidget(self.companyNameLabel)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.overviewSecWidget)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setBold(True)
        self.label.setFont(font1)

        self.horizontalLayout.addWidget(self.label)

        self.fiscalCodeLabel = QLabel(self.overviewSecWidget)
        self.fiscalCodeLabel.setObjectName(u"fiscalCodeLabel")
        sizePolicy.setHeightForWidth(self.fiscalCodeLabel.sizePolicy().hasHeightForWidth())
        self.fiscalCodeLabel.setSizePolicy(sizePolicy)
        font2 = QFont()
        font2.setItalic(True)
        self.fiscalCodeLabel.setFont(font2)
        self.fiscalCodeLabel.setAutoFillBackground(False)
        self.fiscalCodeLabel.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.fiscalCodeLabel)


        self.horizontalLayout_8.addLayout(self.horizontalLayout)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_5)

        self.openWebsiteButton = QPushButton(self.overviewSecWidget)
        self.openWebsiteButton.setObjectName(u"openWebsiteButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.openWebsiteButton.sizePolicy().hasHeightForWidth())
        self.openWebsiteButton.setSizePolicy(sizePolicy1)

        self.horizontalLayout_8.addWidget(self.openWebsiteButton)


        self.overviewSection.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.overviewSecWidget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setFont(font1)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.cciaaNumberLabel = QLabel(self.overviewSecWidget)
        self.cciaaNumberLabel.setObjectName(u"cciaaNumberLabel")
        sizePolicy.setHeightForWidth(self.cciaaNumberLabel.sizePolicy().hasHeightForWidth())
        self.cciaaNumberLabel.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.cciaaNumberLabel)

        self.horizontalSpacer = QSpacerItem(80, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.overviewSection.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.overviewSection.addItem(self.verticalSpacer)

        self.groupBox = QGroupBox(self.overviewSecWidget)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy2)
        self.groupBox.setMinimumSize(QSize(200, 200))
        self.groupBox.setMaximumSize(QSize(600, 600))
        self.groupBox.setFont(font1)
        self.groupBox.setFlat(False)
        self.horizontalLayout_17 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.groupBox)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 390, 226))
        self.horizontalLayout_3 = QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.descriptionLabel = QLabel(self.scrollAreaWidgetContents)
        self.descriptionLabel.setObjectName(u"descriptionLabel")
        self.descriptionLabel.setWordWrap(True)

        self.horizontalLayout_3.addWidget(self.descriptionLabel)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_17.addWidget(self.scrollArea)


        self.overviewSection.addWidget(self.groupBox)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(self.overviewSecWidget)
        self.label_4.setObjectName(u"label_4")
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setFont(font1)

        self.horizontalLayout_4.addWidget(self.label_4)

        self.legalFormLabel = QLabel(self.overviewSecWidget)
        self.legalFormLabel.setObjectName(u"legalFormLabel")
        sizePolicy.setHeightForWidth(self.legalFormLabel.sizePolicy().hasHeightForWidth())
        self.legalFormLabel.setSizePolicy(sizePolicy)

        self.horizontalLayout_4.addWidget(self.legalFormLabel)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)


        self.overviewSection.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(self.overviewSecWidget)
        self.label_5.setObjectName(u"label_5")
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setFont(font1)

        self.horizontalLayout_5.addWidget(self.label_5)

        self.lastBalanceDateLabel = QLabel(self.overviewSecWidget)
        self.lastBalanceDateLabel.setObjectName(u"lastBalanceDateLabel")
        sizePolicy.setHeightForWidth(self.lastBalanceDateLabel.sizePolicy().hasHeightForWidth())
        self.lastBalanceDateLabel.setSizePolicy(sizePolicy)

        self.horizontalLayout_5.addWidget(self.lastBalanceDateLabel)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)


        self.overviewSection.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_8 = QLabel(self.overviewSecWidget)
        self.label_8.setObjectName(u"label_8")
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setFont(font1)

        self.horizontalLayout_9.addWidget(self.label_8)

        self.legalAddressLabel = QLabel(self.overviewSecWidget)
        self.legalAddressLabel.setObjectName(u"legalAddressLabel")
        sizePolicy1.setHeightForWidth(self.legalAddressLabel.sizePolicy().hasHeightForWidth())
        self.legalAddressLabel.setSizePolicy(sizePolicy1)
        self.legalAddressLabel.setMaximumSize(QSize(300, 16777215))
        self.legalAddressLabel.setWordWrap(True)

        self.horizontalLayout_9.addWidget(self.legalAddressLabel)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_6)


        self.overviewSection.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_7 = QLabel(self.overviewSecWidget)
        self.label_7.setObjectName(u"label_7")
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setFont(font1)

        self.horizontalLayout_7.addWidget(self.label_7)

        self.operatingMarketLabel = QLabel(self.overviewSecWidget)
        self.operatingMarketLabel.setObjectName(u"operatingMarketLabel")
        sizePolicy1.setHeightForWidth(self.operatingMarketLabel.sizePolicy().hasHeightForWidth())
        self.operatingMarketLabel.setSizePolicy(sizePolicy1)
        self.operatingMarketLabel.setMaximumSize(QSize(300, 16777215))
        self.operatingMarketLabel.setWordWrap(True)

        self.horizontalLayout_7.addWidget(self.operatingMarketLabel)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_7)


        self.overviewSection.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_6 = QLabel(self.overviewSecWidget)
        self.label_6.setObjectName(u"label_6")
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setFont(font1)

        self.horizontalLayout_6.addWidget(self.label_6)

        self.numberOfYearsLabel = QLabel(self.overviewSecWidget)
        self.numberOfYearsLabel.setObjectName(u"numberOfYearsLabel")
        sizePolicy.setHeightForWidth(self.numberOfYearsLabel.sizePolicy().hasHeightForWidth())
        self.numberOfYearsLabel.setSizePolicy(sizePolicy)

        self.horizontalLayout_6.addWidget(self.numberOfYearsLabel)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_4)


        self.overviewSection.addLayout(self.horizontalLayout_6)

        self.line = QFrame(self.overviewSecWidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.overviewSection.addWidget(self.line)

        self.groupBox_2 = QGroupBox(self.overviewSecWidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy2.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy2)
        self.groupBox_2.setMinimumSize(QSize(250, 200))
        self.groupBox_2.setMaximumSize(QSize(16777215, 16777215))
        font3 = QFont()
        font3.setPointSize(17)
        self.groupBox_2.setFont(font3)
        self.horizontalLayout_20 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.summaryTableView = QTableView(self.groupBox_2)
        self.summaryTableView.setObjectName(u"summaryTableView")

        self.horizontalLayout_20.addWidget(self.summaryTableView)


        self.overviewSection.addWidget(self.groupBox_2)


        self.horizontalLayout_18.addLayout(self.overviewSection)


        self.horizontalLayout_19.addWidget(self.overviewSecWidget)

        self.balanceIndicesSection = QVBoxLayout()
        self.balanceIndicesSection.setObjectName(u"balanceIndicesSection")
        self.balanceSection = QGroupBox(self.centralwidget)
        self.balanceSection.setObjectName(u"balanceSection")
        sizePolicy2.setHeightForWidth(self.balanceSection.sizePolicy().hasHeightForWidth())
        self.balanceSection.setSizePolicy(sizePolicy2)
        self.balanceSection.setMinimumSize(QSize(400, 400))
        self.balanceSection.setFont(font3)
        self.horizontalLayout_10 = QHBoxLayout(self.balanceSection)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.balanceTabWidget = QTabWidget(self.balanceSection)
        self.balanceTabWidget.setObjectName(u"balanceTabWidget")
        font4 = QFont()
        font4.setPointSize(11)
        self.balanceTabWidget.setFont(font4)
        self.conto_economico_tab = QWidget()
        self.conto_economico_tab.setObjectName(u"conto_economico_tab")
        self.horizontalLayout_11 = QHBoxLayout(self.conto_economico_tab)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.contoEconomicoTView = QTableView(self.conto_economico_tab)
        self.contoEconomicoTView.setObjectName(u"contoEconomicoTView")

        self.horizontalLayout_11.addWidget(self.contoEconomicoTView)

        self.balanceTabWidget.addTab(self.conto_economico_tab, "")
        self.stato_patrimoniale_tab = QWidget()
        self.stato_patrimoniale_tab.setObjectName(u"stato_patrimoniale_tab")
        self.horizontalLayout_12 = QHBoxLayout(self.stato_patrimoniale_tab)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.statoPatrimTView = QTableView(self.stato_patrimoniale_tab)
        self.statoPatrimTView.setObjectName(u"statoPatrimTView")

        self.horizontalLayout_12.addWidget(self.statoPatrimTView)

        self.balanceTabWidget.addTab(self.stato_patrimoniale_tab, "")

        self.horizontalLayout_10.addWidget(self.balanceTabWidget)


        self.balanceIndicesSection.addWidget(self.balanceSection)

        self.verticalSpacer_2 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.balanceIndicesSection.addItem(self.verticalSpacer_2)

        self.indiciesSection = QGroupBox(self.centralwidget)
        self.indiciesSection.setObjectName(u"indiciesSection")
        sizePolicy2.setHeightForWidth(self.indiciesSection.sizePolicy().hasHeightForWidth())
        self.indiciesSection.setSizePolicy(sizePolicy2)
        self.indiciesSection.setMinimumSize(QSize(300, 300))
        self.indiciesSection.setFont(font3)
        self.horizontalLayout_16 = QHBoxLayout(self.indiciesSection)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.indiciesTabWidget = QTabWidget(self.indiciesSection)
        self.indiciesTabWidget.setObjectName(u"indiciesTabWidget")
        self.indiciesTabWidget.setFont(font4)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.indiciesTabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.indiciesTabWidget.addTab(self.tab_2, "")

        self.horizontalLayout_16.addWidget(self.indiciesTabWidget)


        self.balanceIndicesSection.addWidget(self.indiciesSection)


        self.horizontalLayout_19.addLayout(self.balanceIndicesSection)

        self.chartSection = QGroupBox(self.centralwidget)
        self.chartSection.setObjectName(u"chartSection")
        self.chartSection.setFont(font3)
        self.verticalLayout_2 = QVBoxLayout(self.chartSection)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tabWidget = QTabWidget(self.chartSection)
        self.tabWidget.setObjectName(u"tabWidget")
        font5 = QFont()
        font5.setPointSize(13)
        self.tabWidget.setFont(font5)
        self.struttura_sp_tab = QWidget()
        self.struttura_sp_tab.setObjectName(u"struttura_sp_tab")
        self.tabWidget.addTab(self.struttura_sp_tab, "")
        self.struttura_ce_tab = QWidget()
        self.struttura_ce_tab.setObjectName(u"struttura_ce_tab")
        self.tabWidget.addTab(self.struttura_ce_tab, "")
        self.evoluz_ricav_tab = QWidget()
        self.evoluz_ricav_tab.setObjectName(u"evoluz_ricav_tab")
        self.tabWidget.addTab(self.evoluz_ricav_tab, "")
        self.evoluz_costi_tab = QWidget()
        self.evoluz_costi_tab.setObjectName(u"evoluz_costi_tab")
        self.tabWidget.addTab(self.evoluz_costi_tab, "")

        self.verticalLayout_2.addWidget(self.tabWidget)


        self.horizontalLayout_19.addWidget(self.chartSection)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1621, 30))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionImportazione)
        self.menuFile.addAction(self.actionCambia_impresa)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionChiudi)

        self.retranslateUi(MainWindow)

        self.openWebsiteButton.setDefault(True)
        self.balanceTabWidget.setCurrentIndex(0)
        self.indiciesTabWidget.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionImportazione.setText(QCoreApplication.translate("MainWindow", u"Importazione", None))
#if QT_CONFIG(shortcut)
        self.actionImportazione.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+I", None))
#endif // QT_CONFIG(shortcut)
        self.actionCambia_impresa.setText(QCoreApplication.translate("MainWindow", u"Cambia impresa", None))
        self.actionChiudi.setText(QCoreApplication.translate("MainWindow", u"Chiudi", None))
        self.companyNameLabel.setText(QCoreApplication.translate("MainWindow", u"Societ\u00e0 esempio", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Codice fiscale", None))
        self.fiscalCodeLabel.setText(QCoreApplication.translate("MainWindow", u"8948598439", None))
        self.fiscalCodeLabel.setProperty(u"cssClass", QCoreApplication.translate("MainWindow", u"number-label", None))
        self.openWebsiteButton.setText(QCoreApplication.translate("MainWindow", u"Sito web", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Codice CCIAA", None))
        self.cciaaNumberLabel.setText(QCoreApplication.translate("MainWindow", u"8948598439", None))
        self.cciaaNumberLabel.setProperty(u"cssClass", QCoreApplication.translate("MainWindow", u"number-label", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Descrizione", None))
        self.descriptionLabel.setText(QCoreApplication.translate("MainWindow", u"Una descrizione bella", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Forma giuridica", None))
        self.legalFormLabel.setText(QCoreApplication.translate("MainWindow", u"SPA", None))
#if QT_CONFIG(tooltip)
        self.label_5.setToolTip(QCoreApplication.translate("MainWindow", u"Data dell'ultimo bilancio caricato", None))
#endif // QT_CONFIG(tooltip)
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Data ultimo bilancio", None))
        self.lastBalanceDateLabel.setText(QCoreApplication.translate("MainWindow", u"2015", None))
        self.lastBalanceDateLabel.setProperty(u"cssClass", QCoreApplication.translate("MainWindow", u"number-label", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Sede legale", None))
        self.legalAddressLabel.setText(QCoreApplication.translate("MainWindow", u"Milano", None))
#if QT_CONFIG(tooltip)
        self.label_7.setToolTip(QCoreApplication.translate("MainWindow", u"Mercato in cui opera l'azienda", None))
#endif // QT_CONFIG(tooltip)
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Mercato in cui opera", None))
        self.operatingMarketLabel.setText(QCoreApplication.translate("MainWindow", u"Assicurazioni", None))
#if QT_CONFIG(tooltip)
        self.label_6.setToolTip(QCoreApplication.translate("MainWindow", u"Numero di anni per cui \u00e8 disponibile un bilancio", None))
#endif // QT_CONFIG(tooltip)
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Numero anni disponibili", None))
        self.numberOfYearsLabel.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.numberOfYearsLabel.setProperty(u"cssClass", QCoreApplication.translate("MainWindow", u"number-label", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Informazioni riassuntive", None))
        self.balanceSection.setTitle(QCoreApplication.translate("MainWindow", u"Dati di bilancio", None))
        self.balanceTabWidget.setTabText(self.balanceTabWidget.indexOf(self.conto_economico_tab), QCoreApplication.translate("MainWindow", u"Conto Economico", None))
        self.balanceTabWidget.setTabText(self.balanceTabWidget.indexOf(self.stato_patrimoniale_tab), QCoreApplication.translate("MainWindow", u"Stato Patrimoniale", None))
        self.indiciesSection.setTitle(QCoreApplication.translate("MainWindow", u"Indici riassuntivi", None))
        self.indiciesTabWidget.setTabText(self.indiciesTabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Tab 1", None))
        self.indiciesTabWidget.setTabText(self.indiciesTabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Tab 2", None))
        self.chartSection.setTitle(QCoreApplication.translate("MainWindow", u"Grafici", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.struttura_sp_tab), QCoreApplication.translate("MainWindow", u"Struttura SP", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.struttura_ce_tab), QCoreApplication.translate("MainWindow", u"Struttura CE", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.evoluz_ricav_tab), QCoreApplication.translate("MainWindow", u"Evoluzione ricavi", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.evoluz_costi_tab), QCoreApplication.translate("MainWindow", u"Evoluz. Costi", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

