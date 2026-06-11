# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'resumen.ui'
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
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)
from recursos import recursos_rc

class Ui_resumen(object):
    def setupUi(self, resumen):
        if not resumen.objectName():
            resumen.setObjectName(u"resumen")
        resumen.resize(440, 400)
        font = QFont()
        font.setFamilies([u"72"])
        resumen.setFont(font)
        icon = QIcon()
        icon.addFile(u"../recursos/magnus.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        resumen.setWindowIcon(icon)
        resumen.setStyleSheet(u"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\n"
"   GLASSMORPHISM DARK \u2014 RESUMEN\n"
"   Base: fondo profundo con capa de \"vidrio\" encima\n"
"   \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"\n"
"QMainWindow, QWidget#centralwidget {\n"
"    background-color: #060B14;\n"
"    background-image:\n"
"        radial-gradient(ellipse at 20% 20%, rgba(24,119,242,0.08) 0%, transparent 55%),\n"
"        radial-gradient(ellipse at 80% 75%, rgba(7,94,84,0.07) 0%, transparent 55%);\n"
"}\n"
"   ")
        self.centralwidget = QWidget(resumen)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_main = QVBoxLayout(self.centralwidget)
        self.verticalLayout_main.setSpacing(0)
        self.verticalLayout_main.setObjectName(u"verticalLayout_main")
        self.verticalLayout_main.setContentsMargins(0, 0, 0, 0)
        self.header_frame = QFrame(self.centralwidget)
        self.header_frame.setObjectName(u"header_frame")
        self.header_frame.setMaximumSize(QSize(16777215, 35))
        self.header_frame.setStyleSheet(u"\n"
"QFrame#header_frame {\n"
"    background-color: #161B27;\n"
"    border: none;\n"
"    border-bottom: 1px solid #232B3E;\n"
"}\n"
"\n"
"QFrame#header_top_accent {\n"
"    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,\n"
"        stop:0   #1877F2,\n"
"        stop:0.4 #4FA3F7,\n"
"        stop:0.6 #38D9A9,\n"
"        stop:1   #075E54);\n"
"    border: none;\n"
"    min-height: 4px;\n"
"    max-height: 4px;\n"
"}\n"
"\n"
"QFrame#header_frame #pushButton_3,\n"
"QFrame#header_frame #pushButton_2,\n"
"QFrame#header_frame #pushButton {\n"
"    background: transparent;\n"
"    border: none;\n"
"}\n"
"\n"
"QPushButton#pushButton_3:hover { background-color: #1E2840; }\n"
"QPushButton#pushButton_3:pressed { background-color: #161B27; }\n"
"QPushButton#pushButton_2:hover { background-color: #1E2840; }\n"
"QPushButton#pushButton_2:pressed { background-color: #161B27; }\n"
"QPushButton#pushButton:hover { background-color: #3A1520; }\n"
"QPushButton#pushButton:pressed { background-color: #2A1018; }\n"
"       ")
        self.header_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.header_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_header = QVBoxLayout(self.header_frame)
        self.verticalLayout_header.setSpacing(0)
        self.verticalLayout_header.setObjectName(u"verticalLayout_header")
        self.verticalLayout_header.setContentsMargins(0, 0, 0, 0)
        self.header_top_accent = QFrame(self.header_frame)
        self.header_top_accent.setObjectName(u"header_top_accent")
        self.header_top_accent.setMinimumSize(QSize(0, 4))
        self.header_top_accent.setMaximumSize(QSize(16777215, 4))
        self.header_top_accent.setFrameShape(QFrame.Shape.NoFrame)
        self.header_top_accent.setFrameShadow(QFrame.Shadow.Plain)

        self.verticalLayout_header.addWidget(self.header_top_accent)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(12, 0, 0, 0)
        self.label = QLabel(self.header_frame)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setFamilies([u"72"])
        font1.setPointSize(10)
        font1.setBold(True)
        self.label.setFont(font1)
        self.label.setStyleSheet(u"color: #1877F2; background: transparent; border: none; padding: 0 8px;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.label)

        self.header_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.header_spacer)

        self.pushButton_3 = QPushButton(self.header_frame)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMinimumSize(QSize(35, 35))
        self.pushButton_3.setMaximumSize(QSize(35, 35))
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/minimizar.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_3.setIcon(icon1)
        self.pushButton_3.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.pushButton_3)

        self.pushButton_2 = QPushButton(self.header_frame)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(35, 35))
        self.pushButton_2.setMaximumSize(QSize(35, 35))
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/maximizar.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_2.setIcon(icon2)
        self.pushButton_2.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.pushButton_2)

        self.pushButton = QPushButton(self.header_frame)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(35, 35))
        self.pushButton.setMaximumSize(QSize(35, 35))
        icon3 = QIcon()
        icon3.addFile(u":/icons/icons/cerrar.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton.setIcon(icon3)
        self.pushButton.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.pushButton)


        self.verticalLayout_header.addLayout(self.horizontalLayout_2)


        self.verticalLayout_main.addWidget(self.header_frame)

        self.verticalLayout_body = QVBoxLayout()
        self.verticalLayout_body.setSpacing(15)
        self.verticalLayout_body.setObjectName(u"verticalLayout_body")
        self.verticalLayout_body.setContentsMargins(20, 20, 20, 20)
        self.lbl_titulo_proceso = QLabel(self.centralwidget)
        self.lbl_titulo_proceso.setObjectName(u"lbl_titulo_proceso")
        self.lbl_titulo_proceso.setFont(font1)
        self.lbl_titulo_proceso.setStyleSheet(u"color: #38D9A9; background: transparent; border: none;")
        self.lbl_titulo_proceso.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_body.addWidget(self.lbl_titulo_proceso)

        self.frame_stats = QFrame(self.centralwidget)
        self.frame_stats.setObjectName(u"frame_stats")
        self.frame_stats.setStyleSheet(u"\n"
"QFrame#frame_stats {\n"
"    background-color: #161B27;\n"
"    border-radius: 10px;\n"
"    border: 1.5px solid #232B3E;\n"
"}\n"
"QLabel { background: transparent; border: none; }\n"
"          ")
        self.vl_stats = QVBoxLayout(self.frame_stats)
        self.vl_stats.setSpacing(0)
        self.vl_stats.setObjectName(u"vl_stats")
        self.vl_stats.setContentsMargins(20, 16, 20, 16)
        self.hl_procesados = QHBoxLayout()
        self.hl_procesados.setSpacing(10)
        self.hl_procesados.setObjectName(u"hl_procesados")
        self.label_2 = QLabel(self.frame_stats)
        self.label_2.setObjectName(u"label_2")
        font2 = QFont()
        font2.setFamilies([u"72"])
        font2.setPointSize(10)
        self.label_2.setFont(font2)
        self.label_2.setStyleSheet(u"color: #A8B8D8; background: transparent; border: none;")

        self.hl_procesados.addWidget(self.label_2)

        self.sp_proc = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hl_procesados.addItem(self.sp_proc)

        self.lbl_procesados = QLabel(self.frame_stats)
        self.lbl_procesados.setObjectName(u"lbl_procesados")
        self.lbl_procesados.setFont(font1)
        self.lbl_procesados.setStyleSheet(u"color: #38D9A9; background: transparent; border: none;")
        self.lbl_procesados.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.hl_procesados.addWidget(self.lbl_procesados)


        self.vl_stats.addLayout(self.hl_procesados)

        self.sep_1 = QFrame(self.frame_stats)
        self.sep_1.setObjectName(u"sep_1")
        self.sep_1.setMinimumSize(QSize(0, 1))
        self.sep_1.setMaximumSize(QSize(16777215, 1))
        self.sep_1.setStyleSheet(u"QFrame#sep_1 { background-color: #1E2840; border: none; margin: 6px 0px; }")

        self.vl_stats.addWidget(self.sep_1)

        self.hl_omitidos = QHBoxLayout()
        self.hl_omitidos.setSpacing(10)
        self.hl_omitidos.setObjectName(u"hl_omitidos")
        self.label_3 = QLabel(self.frame_stats)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font2)
        self.label_3.setStyleSheet(u"color: #A8B8D8; background: transparent; border: none;")

        self.hl_omitidos.addWidget(self.label_3)

        self.sp_omit = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hl_omitidos.addItem(self.sp_omit)

        self.lbl_omitidos = QLabel(self.frame_stats)
        self.lbl_omitidos.setObjectName(u"lbl_omitidos")
        self.lbl_omitidos.setFont(font1)
        self.lbl_omitidos.setStyleSheet(u"color: #4FA3F7; background: transparent; border: none;")
        self.lbl_omitidos.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.hl_omitidos.addWidget(self.lbl_omitidos)


        self.vl_stats.addLayout(self.hl_omitidos)

        self.sep_2 = QFrame(self.frame_stats)
        self.sep_2.setObjectName(u"sep_2")
        self.sep_2.setMinimumSize(QSize(0, 1))
        self.sep_2.setMaximumSize(QSize(16777215, 1))
        self.sep_2.setStyleSheet(u"QFrame#sep_2 { background-color: #1E2840; border: none; margin: 6px 0px; }")

        self.vl_stats.addWidget(self.sep_2)

        self.hl_errores = QHBoxLayout()
        self.hl_errores.setSpacing(10)
        self.hl_errores.setObjectName(u"hl_errores")
        self.label_4 = QLabel(self.frame_stats)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font2)
        self.label_4.setStyleSheet(u"color: #A8B8D8; background: transparent; border: none;")

        self.hl_errores.addWidget(self.label_4)

        self.sp_err = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hl_errores.addItem(self.sp_err)

        self.lbl_errores = QLabel(self.frame_stats)
        self.lbl_errores.setObjectName(u"lbl_errores")
        self.lbl_errores.setFont(font1)
        self.lbl_errores.setStyleSheet(u"color: #E05070; background: transparent; border: none;")
        self.lbl_errores.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.hl_errores.addWidget(self.lbl_errores)


        self.vl_stats.addLayout(self.hl_errores)


        self.verticalLayout_body.addWidget(self.frame_stats)

        self.sep_monto = QFrame(self.centralwidget)
        self.sep_monto.setObjectName(u"sep_monto")
        self.sep_monto.setMinimumSize(QSize(0, 1))
        self.sep_monto.setMaximumSize(QSize(16777215, 1))
        self.sep_monto.setStyleSheet(u"QFrame#sep_monto { background-color: #232B3E; border: none; }")

        self.verticalLayout_body.addWidget(self.sep_monto)

        self.vl_monto = QVBoxLayout()
        self.vl_monto.setSpacing(4)
        self.vl_monto.setObjectName(u"vl_monto")
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setStyleSheet(u"\n"
"color: #3A5080;\n"
"font-family: \"72\";\n"
"font-size: 7.5pt;\n"
"font-weight: 700;\n"
"letter-spacing: 1px;\n"
"background: transparent;\n"
"border: none;\n"
"            ")
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.vl_monto.addWidget(self.label_5)

        self.lbl_monto_procesado = QLabel(self.centralwidget)
        self.lbl_monto_procesado.setObjectName(u"lbl_monto_procesado")
        font3 = QFont()
        font3.setFamilies([u"72"])
        font3.setPointSize(20)
        font3.setBold(True)
        self.lbl_monto_procesado.setFont(font3)
        self.lbl_monto_procesado.setStyleSheet(u"color: #A8B8D8; background: transparent; border: none;")
        self.lbl_monto_procesado.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.vl_monto.addWidget(self.lbl_monto_procesado)


        self.verticalLayout_body.addLayout(self.vl_monto)

        self.sp_bottom = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_body.addItem(self.sp_bottom)

        self.hl_footer = QHBoxLayout()
        self.hl_footer.setObjectName(u"hl_footer")
        self.sp_footer_l = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hl_footer.addItem(self.sp_footer_l)

        self.btn_cerrar = QPushButton(self.centralwidget)
        self.btn_cerrar.setObjectName(u"btn_cerrar")
        self.btn_cerrar.setMinimumSize(QSize(120, 45))
        font4 = QFont()
        font4.setFamilies([u"72"])
        font4.setPointSize(10)
        font4.setWeight(QFont.DemiBold)
        self.btn_cerrar.setFont(font4)
        self.btn_cerrar.setStyleSheet(u"\n"
"QPushButton#btn_cerrar {\n"
"    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,\n"
"        stop:0 #1877F2, stop:1 #3B8FF5);\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    font-family: \"72\";\n"
"    font-size: 10pt;\n"
"    font-weight: 600;\n"
"    border: none;\n"
"    padding: 6px 12px;\n"
"}\n"
"QPushButton#btn_cerrar:hover {\n"
"    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,\n"
"        stop:0 #145DB2, stop:1 #1877F2);\n"
"}\n"
"QPushButton#btn_cerrar:pressed { background-color: #0F4A99; }\n"
"            ")

        self.hl_footer.addWidget(self.btn_cerrar)

        self.sp_footer_r = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hl_footer.addItem(self.sp_footer_r)


        self.verticalLayout_body.addLayout(self.hl_footer)


        self.verticalLayout_main.addLayout(self.verticalLayout_body)

        resumen.setCentralWidget(self.centralwidget)

        self.retranslateUi(resumen)

        QMetaObject.connectSlotsByName(resumen)
    # setupUi

    def retranslateUi(self, resumen):
        resumen.setWindowTitle(QCoreApplication.translate("resumen", u"Magnus \u2014 Resumen", None))
        self.label.setText(QCoreApplication.translate("resumen", u"\U0001f4cb RESUMEN", None))
        self.pushButton_3.setText("")
        self.pushButton_2.setText("")
        self.pushButton.setText("")
        self.lbl_titulo_proceso.setText(QCoreApplication.translate("resumen", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">\u2705 PROCESO COMPLETADO</span></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("resumen", u"\u2705  Procesados:", None))
        self.lbl_procesados.setText(QCoreApplication.translate("resumen", u"0", None))
        self.label_3.setText(QCoreApplication.translate("resumen", u"\u26a0\ufe0f  Omitidos:", None))
        self.lbl_omitidos.setText(QCoreApplication.translate("resumen", u"0", None))
        self.label_4.setText(QCoreApplication.translate("resumen", u"\u274c  Errores:", None))
        self.lbl_errores.setText(QCoreApplication.translate("resumen", u"0", None))
        self.label_5.setText(QCoreApplication.translate("resumen", u"MONTO TOTAL PROCESADO", None))
        self.lbl_monto_procesado.setText(QCoreApplication.translate("resumen", u"Q. 0.00", None))
        self.btn_cerrar.setText(QCoreApplication.translate("resumen", u"Cerrar", None))
    # retranslateUi

