# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'notificacion_toast.ui'
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
    QProgressBar, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_notificacion_toast(object):
    def setupUi(self, notificacion_toast):
        if not notificacion_toast.objectName():
            notificacion_toast.setObjectName(u"notificacion_toast")
        notificacion_toast.setWindowModality(Qt.WindowModality.NonModal)
        notificacion_toast.resize(330, 110)
        notificacion_toast.setMinimumSize(QSize(280, 90))
        notificacion_toast.setMaximumSize(QSize(380, 150))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        notificacion_toast.setFont(font)
        notificacion_toast.setStyleSheet(u"\n"
"QWidget#notificacion_toast {\n"
"    background-color: #000000;\n"
"    border: 1px solid #1877F2;\n"
"    border-radius: 8px;\n"
"}\n"
"   ")
        self.vl_main = QVBoxLayout(notificacion_toast)
        self.vl_main.setSpacing(0)
        self.vl_main.setObjectName(u"vl_main")
        self.vl_main.setContentsMargins(0, 0, 0, 0)
        self.top_accent = QFrame(notificacion_toast)
        self.top_accent.setObjectName(u"top_accent")
        self.top_accent.setMinimumSize(QSize(0, 3))
        self.top_accent.setMaximumSize(QSize(16777215, 3))
        self.top_accent.setStyleSheet(u"\n"
"QFrame#top_accent {\n"
"    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,\n"
"        stop:0 #1877F2, stop:0.5 #4FA3F7, stop:1 #075E54);\n"
"    border: none;\n"
"    border-radius: 0px;\n"
"}\n"
"      ")

        self.vl_main.addWidget(self.top_accent)

        self.vl_body = QVBoxLayout()
        self.vl_body.setSpacing(6)
        self.vl_body.setObjectName(u"vl_body")
        self.vl_body.setContentsMargins(14, 10, 14, 8)
        self.hl_header = QHBoxLayout()
        self.hl_header.setSpacing(8)
        self.hl_header.setObjectName(u"hl_header")
        self.lbl_icon = QLabel(notificacion_toast)
        self.lbl_icon.setObjectName(u"lbl_icon")
        self.lbl_icon.setMinimumSize(QSize(20, 20))
        self.lbl_icon.setMaximumSize(QSize(20, 20))
        self.lbl_icon.setStyleSheet(u"\n"
"color: #1877F2;\n"
"font-size: 14px;\n"
"background: transparent;\n"
"border: none;\n"
"          ")
        self.lbl_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.hl_header.addWidget(self.lbl_icon)

        self.lbl_titulo = QLabel(notificacion_toast)
        self.lbl_titulo.setObjectName(u"lbl_titulo")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_titulo.sizePolicy().hasHeightForWidth())
        self.lbl_titulo.setSizePolicy(sizePolicy)
        self.lbl_titulo.setStyleSheet(u"\n"
"color: #E8EDF5;\n"
"font-size: 10pt;\n"
"font-weight: 700;\n"
"font-family: \"Segoe UI\";\n"
"background: transparent;\n"
"border: none;\n"
"          ")

        self.hl_header.addWidget(self.lbl_titulo)

        self.lbl_timestamp = QLabel(notificacion_toast)
        self.lbl_timestamp.setObjectName(u"lbl_timestamp")
        self.lbl_timestamp.setStyleSheet(u"\n"
"color: #3A5080;\n"
"font-size: 7pt;\n"
"font-family: \"Segoe UI\";\n"
"background: transparent;\n"
"border: none;\n"
"          ")
        self.lbl_timestamp.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.hl_header.addWidget(self.lbl_timestamp)

        self.btn_cerrar = QPushButton(notificacion_toast)
        self.btn_cerrar.setObjectName(u"btn_cerrar")
        self.btn_cerrar.setMinimumSize(QSize(18, 18))
        self.btn_cerrar.setMaximumSize(QSize(18, 18))
        self.btn_cerrar.setStyleSheet(u"\n"
"QPushButton#btn_cerrar {\n"
"    background-color: #111111;\n"
"    color: #3A5080;\n"
"    font-size: 9px;\n"
"    font-family: \"Segoe UI\";\n"
"    border: 1px solid #222222;\n"
"    border-radius: 4px;\n"
"}\n"
"QPushButton#btn_cerrar:hover {\n"
"    background-color: #1A1A2E;\n"
"    color: #E8EDF5;\n"
"    border-color: #1877F2;\n"
"}\n"
"QPushButton#btn_cerrar:pressed {\n"
"    background-color: #0D0D1A;\n"
"}\n"
"          ")
        self.btn_cerrar.setFlat(False)

        self.hl_header.addWidget(self.btn_cerrar)


        self.vl_body.addLayout(self.hl_header)

        self.lbl_mensaje = QLabel(notificacion_toast)
        self.lbl_mensaje.setObjectName(u"lbl_mensaje")
        self.lbl_mensaje.setStyleSheet(u"\n"
"color: #8899BB;\n"
"font-size: 8pt;\n"
"font-family: \"Segoe UI\";\n"
"background: transparent;\n"
"border: none;\n"
"padding-left: 28px;\n"
"        ")
        self.lbl_mensaje.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.lbl_mensaje.setWordWrap(True)

        self.vl_body.addWidget(self.lbl_mensaje)


        self.vl_main.addLayout(self.vl_body)

        self.progress_bar = QProgressBar(notificacion_toast)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setMinimumSize(QSize(0, 2))
        self.progress_bar.setMaximumSize(QSize(16777215, 2))
        self.progress_bar.setStyleSheet(u"\n"
"QProgressBar {\n"
"    background-color: #111111;\n"
"    border: none;\n"
"    border-radius: 0px;\n"
"    max-height: 2px;\n"
"    color: transparent;\n"
"}\n"
"QProgressBar::chunk {\n"
"    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,\n"
"        stop:0 #1877F2, stop:1 #075E54);\n"
"    border-radius: 0px;\n"
"}\n"
"      ")
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(100)

        self.vl_main.addWidget(self.progress_bar)


        self.retranslateUi(notificacion_toast)

        QMetaObject.connectSlotsByName(notificacion_toast)
    # setupUi

    def retranslateUi(self, notificacion_toast):
        notificacion_toast.setWindowTitle(QCoreApplication.translate("notificacion_toast", u"Notificaci\u00f3n", None))
        self.lbl_icon.setText(QCoreApplication.translate("notificacion_toast", u"\U0001f916", None))
        self.lbl_titulo.setText(QCoreApplication.translate("notificacion_toast", u"MAGNUS", None))
        self.lbl_timestamp.setText(QCoreApplication.translate("notificacion_toast", u"ahora", None))
        self.btn_cerrar.setText(QCoreApplication.translate("notificacion_toast", u"\u2715", None))
        self.lbl_mensaje.setText(QCoreApplication.translate("notificacion_toast", u"Mensaje de notificaci\u00f3n aqu\u00ed.", None))
        self.progress_bar.setFormat("")
    # retranslateUi

