# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialogButtonBox, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QSlider, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(635, 392)
        MainWindow.setWindowTitle(u"Firome")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.buttonActivitySelect = QPushButton(self.centralwidget)
        self.buttonActivitySelect.setObjectName(u"buttonActivitySelect")
        self.buttonActivitySelect.setGeometry(QRect(480, 70, 121, 25))
        self.buttonBox = QDialogButtonBox(self.centralwidget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(260, 340, 341, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.inputActivitySelect = QLineEdit(self.centralwidget)
        self.inputActivitySelect.setObjectName(u"inputActivitySelect")
        self.inputActivitySelect.setGeometry(QRect(20, 70, 420, 25))
        self.buttonRouteSelect = QPushButton(self.centralwidget)
        self.buttonRouteSelect.setObjectName(u"buttonRouteSelect")
        self.buttonRouteSelect.setGeometry(QRect(480, 20, 121, 25))
        self.inputRouteSelect = QLineEdit(self.centralwidget)
        self.inputRouteSelect.setObjectName(u"inputRouteSelect")
        self.inputRouteSelect.setGeometry(QRect(20, 20, 420, 25))
        self.precisionLabel = QLabel(self.centralwidget)
        self.precisionLabel.setObjectName(u"precisionLabel")
        self.precisionLabel.setGeometry(QRect(490, 138, 91, 20))
        self.horizontalSlider = QSlider(self.centralwidget)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setGeometry(QRect(20, 140, 421, 21))
        self.horizontalSlider.setOrientation(Qt.Orientation.Horizontal)
        self.precisionValue = QLabel(self.centralwidget)
        self.precisionValue.setObjectName(u"precisionValue")
        self.precisionValue.setGeometry(QRect(460, 140, 67, 17))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        self.buttonActivitySelect.setText(QCoreApplication.translate("MainWindow", u"Select activity", None))
        self.buttonRouteSelect.setText(QCoreApplication.translate("MainWindow", u"Select route", None))
        self.precisionLabel.setText(QCoreApplication.translate("MainWindow", u"Precision, m", None))
        self.precisionValue.setText(QCoreApplication.translate("MainWindow", u"0", None))
        pass
    # retranslateUi

