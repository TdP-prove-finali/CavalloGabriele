# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'invest_sim_window.ui'
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
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QListView, QMainWindow,
    QMenuBar, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QStatusBar, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1436, 922)
        MainWindow.setStyleSheet(u"QLabel[cssClass=\"number-label\"] {\n"
"	padding: 5px;\n"
"	background-color: rgb(18, 65, 255);\n"
"	border-radius: 5px;\n"
"	font-style: italic;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QSize(0, 300))
        self.groupBox.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setPointSize(17)
        self.groupBox.setFont(font)
        self.horizontalLayout_6 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setPointSize(13)
        font1.setBold(True)
        self.label_2.setFont(font1)

        self.horizontalLayout_3.addWidget(self.label_2)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.projectTitleLineEdit = QLineEdit(self.groupBox)
        self.projectTitleLineEdit.setObjectName(u"projectTitleLineEdit")
        font2 = QFont()
        font2.setPointSize(13)
        self.projectTitleLineEdit.setFont(font2)

        self.horizontalLayout_3.addWidget(self.projectTitleLineEdit)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy2)
        self.label_3.setFont(font1)

        self.verticalLayout_2.addWidget(self.label_3)

        self.projectDescription = QTextEdit(self.groupBox)
        self.projectDescription.setObjectName(u"projectDescription")
        self.projectDescription.setMaximumSize(QSize(16777215, 300))
        self.projectDescription.setFont(font2)

        self.verticalLayout_2.addWidget(self.projectDescription)


        self.verticalLayout_4.addLayout(self.verticalLayout_2)


        self.horizontalLayout_6.addLayout(self.verticalLayout_4)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        sizePolicy1.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy1)
        self.label_4.setFont(font1)

        self.horizontalLayout_5.addWidget(self.label_4)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)

        self.newComponentBtn = QPushButton(self.groupBox)
        self.newComponentBtn.setObjectName(u"newComponentBtn")
        sizePolicy2.setHeightForWidth(self.newComponentBtn.sizePolicy().hasHeightForWidth())
        self.newComponentBtn.setSizePolicy(sizePolicy2)
        self.newComponentBtn.setFont(font2)

        self.horizontalLayout_4.addWidget(self.newComponentBtn)

        self.removeComponentBtn = QPushButton(self.groupBox)
        self.removeComponentBtn.setObjectName(u"removeComponentBtn")
        sizePolicy2.setHeightForWidth(self.removeComponentBtn.sizePolicy().hasHeightForWidth())
        self.removeComponentBtn.setSizePolicy(sizePolicy2)
        self.removeComponentBtn.setFont(font2)

        self.horizontalLayout_4.addWidget(self.removeComponentBtn)


        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.projectComponentsListView = QListView(self.groupBox)
        self.projectComponentsListView.setObjectName(u"projectComponentsListView")
        self.projectComponentsListView.setFont(font2)

        self.verticalLayout_3.addWidget(self.projectComponentsListView)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_10 = QLabel(self.groupBox)
        self.label_10.setObjectName(u"label_10")
        sizePolicy1.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy1)
        font3 = QFont()
        font3.setPointSize(11)
        self.label_10.setFont(font3)

        self.horizontalLayout_12.addWidget(self.label_10)

        self.liquidAvailabilityLabel = QLabel(self.groupBox)
        self.liquidAvailabilityLabel.setObjectName(u"liquidAvailabilityLabel")
        sizePolicy1.setHeightForWidth(self.liquidAvailabilityLabel.sizePolicy().hasHeightForWidth())
        self.liquidAvailabilityLabel.setSizePolicy(sizePolicy1)
        font4 = QFont()
        font4.setPointSize(11)
        font4.setItalic(True)
        self.liquidAvailabilityLabel.setFont(font4)

        self.horizontalLayout_12.addWidget(self.liquidAvailabilityLabel)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_5)

        self.label_13 = QLabel(self.groupBox)
        self.label_13.setObjectName(u"label_13")
        sizePolicy1.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy1)
        self.label_13.setFont(font3)

        self.horizontalLayout_12.addWidget(self.label_13)

        self.totalEsbLabel = QLabel(self.groupBox)
        self.totalEsbLabel.setObjectName(u"totalEsbLabel")
        sizePolicy1.setHeightForWidth(self.totalEsbLabel.sizePolicy().hasHeightForWidth())
        self.totalEsbLabel.setSizePolicy(sizePolicy1)
        self.totalEsbLabel.setFont(font4)

        self.horizontalLayout_12.addWidget(self.totalEsbLabel)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_7)

        self.label_15 = QLabel(self.groupBox)
        self.label_15.setObjectName(u"label_15")
        sizePolicy1.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy1)
        self.label_15.setFont(font3)

        self.horizontalLayout_12.addWidget(self.label_15)

        self.totalFundingLabel = QLabel(self.groupBox)
        self.totalFundingLabel.setObjectName(u"totalFundingLabel")
        sizePolicy1.setHeightForWidth(self.totalFundingLabel.sizePolicy().hasHeightForWidth())
        self.totalFundingLabel.setSizePolicy(sizePolicy1)
        self.totalFundingLabel.setFont(font4)

        self.horizontalLayout_12.addWidget(self.totalFundingLabel)


        self.verticalLayout_3.addLayout(self.horizontalLayout_12)


        self.horizontalLayout_6.addLayout(self.verticalLayout_3)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy3)
        self.groupBox_2.setMinimumSize(QSize(0, 300))
        self.groupBox_2.setMaximumSize(QSize(16777215, 200))
        self.groupBox_2.setFont(font)
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        self.label.setFont(font2)

        self.horizontalLayout_2.addWidget(self.label)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.companyNameEdit = QLineEdit(self.groupBox_2)
        self.companyNameEdit.setObjectName(u"companyNameEdit")
        self.companyNameEdit.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.companyNameEdit)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_9)


        self.verticalLayout_5.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font2)

        self.horizontalLayout_7.addWidget(self.label_5)

        self.numberOfYears = QSpinBox(self.groupBox_2)
        self.numberOfYears.setObjectName(u"numberOfYears")
        self.numberOfYears.setFont(font2)
        self.numberOfYears.setMinimum(1)

        self.horizontalLayout_7.addWidget(self.numberOfYears)


        self.horizontalLayout_11.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_6)

        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font2)

        self.horizontalLayout_8.addWidget(self.label_6)

        self.startingYearEdit = QSpinBox(self.groupBox_2)
        self.startingYearEdit.setObjectName(u"startingYearEdit")
        self.startingYearEdit.setFont(font2)
        self.startingYearEdit.setMinimum(2000)
        self.startingYearEdit.setMaximum(3000)
        self.startingYearEdit.setValue(2026)

        self.horizontalLayout_8.addWidget(self.startingYearEdit)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_10)


        self.horizontalLayout_11.addLayout(self.horizontalLayout_8)


        self.verticalLayout_5.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_11 = QLabel(self.groupBox_2)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_9.addWidget(self.label_11)

        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font2)

        self.horizontalLayout_9.addWidget(self.label_7)

        self.organicGrowthSpin = QDoubleSpinBox(self.groupBox_2)
        self.organicGrowthSpin.setObjectName(u"organicGrowthSpin")
        self.organicGrowthSpin.setFont(font2)

        self.horizontalLayout_9.addWidget(self.organicGrowthSpin)

        self.label_8 = QLabel(self.groupBox_2)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font2)

        self.horizontalLayout_9.addWidget(self.label_8)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_11)


        self.verticalLayout_5.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_9 = QLabel(self.groupBox_2)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font2)

        self.horizontalLayout_10.addWidget(self.label_9)

        self.lastAvYearsLabel = QLabel(self.groupBox_2)
        self.lastAvYearsLabel.setObjectName(u"lastAvYearsLabel")
        font5 = QFont()
        font5.setPointSize(13)
        font5.setItalic(True)
        self.lastAvYearsLabel.setFont(font5)
        self.lastAvYearsLabel.setStyleSheet(u"")

        self.horizontalLayout_10.addWidget(self.lastAvYearsLabel)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_12)


        self.verticalLayout_5.addLayout(self.horizontalLayout_10)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy4)
        self.widget.setMinimumSize(QSize(27, 0))
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(421, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.simStatusBar = QProgressBar(self.widget)
        self.simStatusBar.setObjectName(u"simStatusBar")
        self.simStatusBar.setEnabled(False)
        self.simStatusBar.setValue(24)

        self.horizontalLayout.addWidget(self.simStatusBar)

        self.stopSimBtn = QPushButton(self.widget)
        self.stopSimBtn.setObjectName(u"stopSimBtn")
        sizePolicy2.setHeightForWidth(self.stopSimBtn.sizePolicy().hasHeightForWidth())
        self.stopSimBtn.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.stopSimBtn)

        self.startSimBtn = QPushButton(self.widget)
        self.startSimBtn.setObjectName(u"startSimBtn")
        sizePolicy2.setHeightForWidth(self.startSimBtn.sizePolicy().hasHeightForWidth())
        self.startSimBtn.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.startSimBtn)


        self.verticalLayout.addWidget(self.widget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1436, 30))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Progetto di investimento", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Titolo", None))
        self.projectTitleLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Titolo del progetto di investimento", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Descrizione", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Componenti", None))
        self.newComponentBtn.setText(QCoreApplication.translate("MainWindow", u"Nuova", None))
        self.removeComponentBtn.setText(QCoreApplication.translate("MainWindow", u"Rimuovi", None))
#if QT_CONFIG(tooltip)
        self.label_10.setToolTip(QCoreApplication.translate("MainWindow", u"Disponibilit\u00e0 liquide disponibili all'ultimo bilancio", None))
#endif // QT_CONFIG(tooltip)
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Disponibilit\u00e0 liquide", None))
        self.liquidAvailabilityLabel.setText(QCoreApplication.translate("MainWindow", u"1000\u20ac", None))
        self.liquidAvailabilityLabel.setProperty(u"cssClass", QCoreApplication.translate("MainWindow", u"number-label", None))
#if QT_CONFIG(tooltip)
        self.label_13.setToolTip(QCoreApplication.translate("MainWindow", u"Totale esborso immediato del progetto nel primo mese", None))
#endif // QT_CONFIG(tooltip)
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Totale esborso progetto", None))
        self.totalEsbLabel.setText(QCoreApplication.translate("MainWindow", u"1000\u20ac", None))
        self.totalEsbLabel.setProperty(u"cssClass", QCoreApplication.translate("MainWindow", u"number-label", None))
#if QT_CONFIG(tooltip)
        self.label_15.setToolTip(QCoreApplication.translate("MainWindow", u"Totale finanziamenti (a debito e tramite soci) richiesti", None))
#endif // QT_CONFIG(tooltip)
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Totale finanziamenti", None))
        self.totalFundingLabel.setText(QCoreApplication.translate("MainWindow", u"1000\u20ac", None))
        self.totalFundingLabel.setProperty(u"cssClass", QCoreApplication.translate("MainWindow", u"number-label", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Parametri simulazione", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Azienda selezionata", None))
#if QT_CONFIG(tooltip)
        self.label_5.setToolTip(QCoreApplication.translate("MainWindow", u"Numero di anni su cui strutturare la simulazione", None))
#endif // QT_CONFIG(tooltip)
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Numero di anni", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Anno iniziale", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
#if QT_CONFIG(tooltip)
        self.label_7.setToolTip(QCoreApplication.translate("MainWindow", u"Crescita spontanea del fatturato senza operazioni", None))
#endif // QT_CONFIG(tooltip)
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Crescita organica", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"%", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Anni passati disponibili", None))
        self.lastAvYearsLabel.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.lastAvYearsLabel.setProperty(u"cssClass", QCoreApplication.translate("MainWindow", u"number-label", None))
        self.stopSimBtn.setText(QCoreApplication.translate("MainWindow", u"Ferma simulazione", None))
        self.startSimBtn.setText(QCoreApplication.translate("MainWindow", u"Avvia simulazione", None))
    # retranslateUi

