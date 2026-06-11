# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'splash.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QProgressBar, QSizePolicy, QSpacerItem,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_splash(object):
    def setupUi(self, splash):
        if not splash.objectName():
            splash.setObjectName(u"splash")
        splash.setWindowModality(Qt.WindowModality.WindowModal)
        splash.resize(488, 305)
        splash.setMinimumSize(QSize(360, 180))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        splash.setFont(font)
        splash.setMouseTracking(False)
        splash.setTabletTracking(False)
        icon = QIcon()
        icon.addFile(u"../magnus.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        splash.setWindowIcon(icon)
        splash.setStyleSheet(u"\n"
"QMainWindow, QWidget#centralwidget {\n"
"    background-color: #0D1117;\n"
"}\n"
"   ")
        splash.setTabShape(QTabWidget.TabShape.Rounded)
        self.centralwidget = QWidget(splash)
        self.centralwidget.setObjectName(u"centralwidget")
        self.vl_main = QVBoxLayout(self.centralwidget)
        self.vl_main.setSpacing(0)
        self.vl_main.setObjectName(u"vl_main")
        self.vl_main.setContentsMargins(0, 0, 0, 0)
        self.top_accent = QFrame(self.centralwidget)
        self.top_accent.setObjectName(u"top_accent")
        self.top_accent.setMinimumSize(QSize(0, 4))
        self.top_accent.setMaximumSize(QSize(16777215, 4))
        self.top_accent.setStyleSheet(u"\n"
"QFrame#top_accent {\n"
"    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,\n"
"        stop:0 #1877F2, stop:0.5 #4FA3F7, stop:1 #075E54);\n"
"    border: none;\n"
"}\n"
"       ")

        self.vl_main.addWidget(self.top_accent)

        self.vl_body = QVBoxLayout()
        self.vl_body.setSpacing(6)
        self.vl_body.setObjectName(u"vl_body")
        self.vl_body.setContentsMargins(40, 0, 40, 0)
        self.spacer_top = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.vl_body.addItem(self.spacer_top)

        self.hl_title = QHBoxLayout()
        self.hl_title.setSpacing(10)
        self.hl_title.setObjectName(u"hl_title")
        self.spacer_title_l = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hl_title.addItem(self.spacer_title_l)

        self.lbl_icon = QLabel(self.centralwidget)
        self.lbl_icon.setObjectName(u"lbl_icon")
        self.lbl_icon.setStyleSheet(u"\n"
"color: #1877F2;\n"
"font-size: 22px;\n"
"background: transparent;\n"
"border: none;\n"
"           ")
        self.lbl_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.hl_title.addWidget(self.lbl_icon)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"\n"
"color: #1877F2;\n"
"font-size: 20pt;\n"
"font-weight: 700;\n"
"font-family: \"Segoe UI\";\n"
"background: transparent;\n"
"border: none;\n"
"           ")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.hl_title.addWidget(self.label)

        self.spacer_title_r = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hl_title.addItem(self.spacer_title_r)


        self.vl_body.addLayout(self.hl_title)

        self.lbl_subtitle = QLabel(self.centralwidget)
        self.lbl_subtitle.setObjectName(u"lbl_subtitle")
        self.lbl_subtitle.setStyleSheet(u"\n"
"color: #3A5080;\n"
"font-size: 7.5pt;\n"
"font-family: \"Segoe UI\";\n"
"font-weight: 700;\n"
"letter-spacing: 2px;\n"
"background: transparent;\n"
"border: none;\n"
"         ")
        self.lbl_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.vl_body.addWidget(self.lbl_subtitle, 0, Qt.AlignmentFlag.AlignHCenter)

        self.sep_mid = QFrame(self.centralwidget)
        self.sep_mid.setObjectName(u"sep_mid")
        self.sep_mid.setMinimumSize(QSize(0, 1))
        self.sep_mid.setMaximumSize(QSize(16777215, 1))
        self.sep_mid.setStyleSheet(u"\n"
"background: qlineargradient(x1:0,y1:0,x2:1,y2:0,\n"
"    stop:0 transparent, stop:0.2 #232B3E, stop:0.8 #232B3E, stop:1 transparent);\n"
"border: none;\n"
"         ")

        self.vl_body.addWidget(self.sep_mid)

        self.lbl_validar_actualizaciones = QLabel(self.centralwidget)
        self.lbl_validar_actualizaciones.setObjectName(u"lbl_validar_actualizaciones")
        self.lbl_validar_actualizaciones.setStyleSheet(u"\n"
"color: #3A5080;\n"
"font-size: 8pt;\n"
"font-family: \"Segoe UI\";\n"
"background: transparent;\n"
"border: none;\n"
"         ")
        self.lbl_validar_actualizaciones.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.vl_body.addWidget(self.lbl_validar_actualizaciones, 0, Qt.AlignmentFlag.AlignHCenter)

        self.spacer_mid = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.vl_body.addItem(self.spacer_mid)


        self.vl_main.addLayout(self.vl_body)

        self.frame_footer = QFrame(self.centralwidget)
        self.frame_footer.setObjectName(u"frame_footer")
        self.frame_footer.setMinimumSize(QSize(0, 38))
        self.frame_footer.setMaximumSize(QSize(16777215, 38))
        self.frame_footer.setStyleSheet(u"\n"
"QFrame#frame_footer {\n"
"    background-color: #161B27;\n"
"    border: none;\n"
"    border-top: 1px solid #232B3E;\n"
"}\n"
"       ")
        self.frame_footer.setFrameShape(QFrame.Shape.StyledPanel)
        self.vl_footer = QVBoxLayout(self.frame_footer)
        self.vl_footer.setSpacing(0)
        self.vl_footer.setObjectName(u"vl_footer")
        self.vl_footer.setContentsMargins(0, 0, 0, 0)
        self.progress_bar = QProgressBar(self.frame_footer)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setMinimumSize(QSize(0, 3))
        self.progress_bar.setMaximumSize(QSize(16777215, 3))
        self.progress_bar.setStyleSheet(u"\n"
"QProgressBar {\n"
"    background-color: #1E2840;\n"
"    border: none;\n"
"    border-radius: 0px;\n"
"    max-height: 3px;\n"
"    color: transparent;\n"
"}\n"
"QProgressBar::chunk {\n"
"    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,\n"
"        stop:0 #1877F2, stop:1 #075E54);\n"
"    border-radius: 0px;\n"
"}\n"
"          ")
        self.progress_bar.setValue(98)

        self.vl_footer.addWidget(self.progress_bar)

        self.lbl_footer = QLabel(self.frame_footer)
        self.lbl_footer.setObjectName(u"lbl_footer")
        self.lbl_footer.setStyleSheet(u"\n"
"color: #3A5080;\n"
"font-size: 7pt;\n"
"font-family: \"Segoe UI\";\n"
"background: transparent;\n"
"border: none;\n"
"padding: 0px 16px;\n"
"          ")
        self.lbl_footer.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.vl_footer.addWidget(self.lbl_footer)


        self.vl_main.addWidget(self.frame_footer)

        splash.setCentralWidget(self.centralwidget)

        self.retranslateUi(splash)

        QMetaObject.connectSlotsByName(splash)
    # setupUi

    def retranslateUi(self, splash):
        splash.setWindowTitle(QCoreApplication.translate("splash", u"Splash", None))
        self.lbl_icon.setText(QCoreApplication.translate("splash", u"\U0001f916", None))
        self.label.setText(QCoreApplication.translate("splash", u"MAGNUS", None))
        self.lbl_subtitle.setText(QCoreApplication.translate("splash", u"RPA SOLUTIONS  \u00b7  AUTOMATIZACI\u00d3N", None))
        self.lbl_validar_actualizaciones.setText(QCoreApplication.translate("splash", u"<html><head/><body><p align=\"center\"><span style=\" font-size:8pt;\">Buscando actualizaciones...</span></p></body></html>", None))
        self.progress_bar.setFormat("")
        self.lbl_footer.setText(QCoreApplication.translate("splash", u"\u00a9 2026 Magnus RPA \u00b7 Iniciando aplicaci\u00f3n...", None))
    # retranslateUi

