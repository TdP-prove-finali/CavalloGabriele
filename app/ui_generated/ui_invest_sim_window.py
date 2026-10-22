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
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QListView, QMainWindow,
    QMenuBar, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QStatusBar, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1187, 815)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QSize(0, 300))
        self.groupBox.setMaximumSize(QSize(16777215, 800))
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
        font = QFont()
        font.setBold(True)
        self.label_2.setFont(font)

        self.horizontalLayout_3.addWidget(self.label_2)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.projectTitleLineEdit = QLineEdit(self.groupBox)
        self.projectTitleLineEdit.setObjectName(u"projectTitleLineEdit")

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
        self.label_3.setFont(font)

        self.verticalLayout_2.addWidget(self.label_3)

        self.projectDescription = QTextEdit(self.groupBox)
        self.projectDescription.setObjectName(u"projectDescription")
        self.projectDescription.setMaximumSize(QSize(16777215, 300))

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
        font1 = QFont()
        font1.setPointSize(15)
        font1.setBold(True)
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

        self.horizontalLayout_4.addWidget(self.newComponentBtn)

        self.removeComponentBtn = QPushButton(self.groupBox)
        self.removeComponentBtn.setObjectName(u"removeComponentBtn")
        sizePolicy2.setHeightForWidth(self.removeComponentBtn.sizePolicy().hasHeightForWidth())
        self.removeComponentBtn.setSizePolicy(sizePolicy2)

        self.horizontalLayout_4.addWidget(self.removeComponentBtn)


        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.projectComponentsListView = QListView(self.groupBox)
        self.projectComponentsListView.setObjectName(u"projectComponentsListView")

        self.verticalLayout_3.addWidget(self.projectComponentsListView)


        self.horizontalLayout_6.addLayout(self.verticalLayout_3)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy3)
        self.groupBox_2.setMinimumSize(QSize(0, 300))
        self.widget = QWidget(self.groupBox_2)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(60, 40, 511, 32))
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.label)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.companyComboBox = QComboBox(self.widget)
        self.companyComboBox.setObjectName(u"companyComboBox")
        self.companyComboBox.setEnabled(False)
        self.companyComboBox.setMaximumSize(QSize(300, 16777215))

        self.horizontalLayout_2.addWidget(self.companyComboBox)

        self.widget1 = QWidget(self.groupBox_2)
        self.widget1.setObjectName(u"widget1")
        self.widget1.setGeometry(QRect(60, 90, 191, 31))
        self.horizontalLayout_7 = QHBoxLayout(self.widget1)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.widget1)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_7.addWidget(self.label_5)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_5)

        self.numberOfYears = QSpinBox(self.widget1)
        self.numberOfYears.setObjectName(u"numberOfYears")

        self.horizontalLayout_7.addWidget(self.numberOfYears)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.widget2 = QWidget(self.centralwidget)
        self.widget2.setObjectName(u"widget2")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.widget2.sizePolicy().hasHeightForWidth())
        self.widget2.setSizePolicy(sizePolicy4)
        self.widget2.setMinimumSize(QSize(27, 0))
        self.horizontalLayout = QHBoxLayout(self.widget2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(421, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.simStatusBar = QProgressBar(self.widget2)
        self.simStatusBar.setObjectName(u"simStatusBar")
        self.simStatusBar.setEnabled(False)
        self.simStatusBar.setValue(24)

        self.horizontalLayout.addWidget(self.simStatusBar)

        self.stopSimBtn = QPushButton(self.widget2)
        self.stopSimBtn.setObjectName(u"stopSimBtn")
        sizePolicy2.setHeightForWidth(self.stopSimBtn.sizePolicy().hasHeightForWidth())
        self.stopSimBtn.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.stopSimBtn)

        self.startSimBtn = QPushButton(self.widget2)
        self.startSimBtn.setObjectName(u"startSimBtn")
        sizePolicy2.setHeightForWidth(self.startSimBtn.sizePolicy().hasHeightForWidth())
        self.startSimBtn.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.startSimBtn)


        self.verticalLayout.addWidget(self.widget2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1187, 30))
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
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Parametri simulazione", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Azienda selezionata", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Numero di anni", None))
        self.stopSimBtn.setText(QCoreApplication.translate("MainWindow", u"Ferma simulazione", None))
        self.startSimBtn.setText(QCoreApplication.translate("MainWindow", u"Avvia simulazione", None))
    # retranslateUi

