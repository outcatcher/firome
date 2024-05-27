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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialogButtonBox, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(537, 231)
        MainWindow.setWindowTitle(u"Firome")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.buttonActivitySelect = QPushButton(self.centralwidget)
        self.buttonActivitySelect.setObjectName(u"buttonActivitySelect")
        self.buttonActivitySelect.setGeometry(QRect(400, 70, 121, 25))
        self.buttonBox = QDialogButtonBox(self.centralwidget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(180, 180, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.inputActivitySelect = QLineEdit(self.centralwidget)
        self.inputActivitySelect.setObjectName(u"inputActivitySelect")
        self.inputActivitySelect.setGeometry(QRect(20, 70, 341, 25))
        self.buttonRouteSelect = QPushButton(self.centralwidget)
        self.buttonRouteSelect.setObjectName(u"buttonRouteSelect")
        self.buttonRouteSelect.setGeometry(QRect(400, 20, 121, 25))
        self.inputRouteSelect = QLineEdit(self.centralwidget)
        self.inputRouteSelect.setObjectName(u"inputRouteSelect")
        self.inputRouteSelect.setGeometry(QRect(20, 20, 341, 25))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        self.buttonActivitySelect.setText(QCoreApplication.translate("MainWindow", u"Select activity", None))
        self.buttonRouteSelect.setText(QCoreApplication.translate("MainWindow", u"Select route", None))
        pass
    # retranslateUi

