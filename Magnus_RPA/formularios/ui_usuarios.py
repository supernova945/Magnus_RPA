# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'usuarios.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_credenciales(object):
    def setupUi(self, credenciales):
        if not credenciales.objectName():
            credenciales.setObjectName(u"credenciales")
        credenciales.resize(1000, 700)
        font = QFont()
        font.setFamilies([u"72"])
        credenciales.setFont(font)
        icon = QIcon()
        icon.addFile(u"../recursos/magnus.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        credenciales.setWindowIcon(icon)
        credenciales.setStyleSheet(u"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\n"
"   GLASSMORPHISM DARK \u2014 CREDENCIALES\n"
"   Base: fondo profundo con capa de \"vidrio\" encima\n"
"   \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"\n"
"QMainWindow, QWidget#centralwidget {\n"
"    background-color: #060B14;\n"
"    background-image:\n"
"        radial-gradient(ellipse at 20% 20%, rgba(24,119,242,0.08) 0%, transparent 55%),\n"
"        radial-gradient(ellipse at 80% 75%, rgba(7,94,84,0.07) 0%, transparent 55%);\n"
"}\n"
"\n"
"QScrollBar:vertical { background:#"
                        "0D1117; width:6px; border-radius:3px; }\n"
"QScrollBar::handle:vertical { background:#232B3E; border-radius:3px; min-height:20px; }\n"
"QScrollBar::handle:vertical:hover { background:#1877F2; }\n"
"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height:0px; }\n"
"   ")
        self.centralwidget = QWidget(credenciales)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_main = QVBoxLayout(self.centralwidget)
        self.verticalLayout_main.setSpacing(15)
        self.verticalLayout_main.setObjectName(u"verticalLayout_main")
        self.verticalLayout_main.setContentsMargins(20, 20, 20, 20)
        self.top_accent = QFrame(self.centralwidget)
        self.top_accent.setObjectName(u"top_accent")
        self.top_accent.setMinimumSize(QSize(0, 3))
        self.top_accent.setMaximumSize(QSize(16777215, 3))
        self.top_accent.setStyleSheet(u"\n"
"QFrame#top_accent {\n"
"    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,\n"
"        stop:0   #1877F2,\n"
"        stop:0.4 #4FA3F7,\n"
"        stop:0.6 #38D9A9,\n"
"        stop:1   #075E54);\n"
"    border: none;\n"
"}\n"
"       ")

        self.verticalLayout_main.addWidget(self.top_accent)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setFamilies([u"72"])
        font1.setPointSize(12)
        font1.setBold(True)
        self.label.setFont(font1)
        self.label.setStyleSheet(u"\n"
"color: #1877F2;\n"
"background: transparent;\n"
"border: none;\n"
"       ")

        self.verticalLayout_main.addWidget(self.label)

        self.hl_nuevo_perfil = QHBoxLayout()
        self.hl_nuevo_perfil.setObjectName(u"hl_nuevo_perfil")
        self.sp_header = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hl_nuevo_perfil.addItem(self.sp_header)

        self.btn_nuevo_perfil = QPushButton(self.centralwidget)
        self.btn_nuevo_perfil.setObjectName(u"btn_nuevo_perfil")
        self.btn_nuevo_perfil.setMinimumSize(QSize(130, 36))
        self.btn_nuevo_perfil.setMaximumSize(QSize(130, 36))
        font2 = QFont()
        font2.setFamilies([u"72"])
        font2.setPointSize(10)
        font2.setWeight(QFont.DemiBold)
        self.btn_nuevo_perfil.setFont(font2)
        self.btn_nuevo_perfil.setStyleSheet(u"\n"
"QPushButton#btn_nuevo_perfil {\n"
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
"QPushButton#btn_nuevo_perfil:hover {\n"
"    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,\n"
"        stop:0 #145DB2, stop:1 #1877F2);\n"
"}\n"
"QPushButton#btn_nuevo_perfil:pressed { background-color: #0F4A99; }\n"
"         ")

        self.hl_nuevo_perfil.addWidget(self.btn_nuevo_perfil)


        self.verticalLayout_main.addLayout(self.hl_nuevo_perfil)

        self.hl_body = QHBoxLayout()
        self.hl_body.setSpacing(15)
        self.hl_body.setObjectName(u"hl_body")
        self.hl_body.setContentsMargins(0, 0, 0, 0)
        self.login_card = QFrame(self.centralwidget)
        self.login_card.setObjectName(u"login_card")
        self.login_card.setMinimumSize(QSize(380, 0))
        self.login_card.setMaximumSize(QSize(430, 16777215))
        self.login_card.setStyleSheet(u"\n"
"QFrame#login_card {\n"
"    background-color: #161B27;\n"
"    border: 1.5px solid #232B3E;\n"
"    border-radius: 10px;\n"
"}\n"
"QLabel { background: transparent; border: none; }\n"
"         ")
        self.verticalLayout_card = QVBoxLayout(self.login_card)
        self.verticalLayout_card.setSpacing(12)
        self.verticalLayout_card.setObjectName(u"verticalLayout_card")
        self.verticalLayout_card.setContentsMargins(20, 20, 20, 20)
        self.lbl_form_title = QLabel(self.login_card)
        self.lbl_form_title.setObjectName(u"lbl_form_title")
        font3 = QFont()
        font3.setFamilies([u"72"])
        font3.setPointSize(11)
        font3.setBold(True)
        self.lbl_form_title.setFont(font3)
        self.lbl_form_title.setStyleSheet(u"color: #A8B8D8; background: transparent; border: none;")

        self.verticalLayout_card.addWidget(self.lbl_form_title)

        self.vl_f_alias = QVBoxLayout()
        self.vl_f_alias.setSpacing(6)
        self.vl_f_alias.setObjectName(u"vl_f_alias")
        self.lbl_f_alias = QLabel(self.login_card)
        self.lbl_f_alias.setObjectName(u"lbl_f_alias")
        self.lbl_f_alias.setStyleSheet(u"\n"
"color: #3A5080;\n"
"font-family: \"72\";\n"
"font-size: 7.5pt;\n"
"font-weight: 700;\n"
"letter-spacing: 1px;\n"
"background: transparent;\n"
"border: none;\n"
"              ")

        self.vl_f_alias.addWidget(self.lbl_f_alias)

        self.frame_alias = QFrame(self.login_card)
        self.frame_alias.setObjectName(u"frame_alias")
        self.frame_alias.setMinimumSize(QSize(0, 40))
        self.frame_alias.setStyleSheet(u"\n"
"QFrame#frame_alias {\n"
"    background-color: #0D1117;\n"
"    border-radius: 8px;\n"
"    border: 1.5px solid #232B3E;\n"
"}\n"
"QFrame#frame_alias:focus-within {\n"
"    border-color: #1877F2;\n"
"}\n"
"              ")
        self.hl_alias = QHBoxLayout(self.frame_alias)
        self.hl_alias.setSpacing(8)
        self.hl_alias.setObjectName(u"hl_alias")
        self.hl_alias.setContentsMargins(10, 0, 10, 0)
        self.lbl_alias_icon = QLabel(self.frame_alias)
        self.lbl_alias_icon.setObjectName(u"lbl_alias_icon")
        self.lbl_alias_icon.setStyleSheet(u"color: #1877F2; font-size: 12pt; background: transparent; border: none;")

        self.hl_alias.addWidget(self.lbl_alias_icon)

        self.txt_usuario = QLineEdit(self.frame_alias)
        self.txt_usuario.setObjectName(u"txt_usuario")
        font4 = QFont()
        font4.setFamilies([u"72"])
        font4.setPointSize(9)
        self.txt_usuario.setFont(font4)
        self.txt_usuario.setStyleSheet(u"\n"
"QLineEdit {\n"
"    background: transparent;\n"
"    border: none;\n"
"    color: #A8B8D8;\n"
"    font-family: \"72\";\n"
"    font-size: 9pt;\n"
"    padding: 2px;\n"
"}\n"
"                 ")

        self.hl_alias.addWidget(self.txt_usuario)


        self.vl_f_alias.addWidget(self.frame_alias)


        self.verticalLayout_card.addLayout(self.vl_f_alias)

        self.vl_f_user = QVBoxLayout()
        self.vl_f_user.setSpacing(6)
        self.vl_f_user.setObjectName(u"vl_f_user")
        self.lbl_user = QLabel(self.login_card)
        self.lbl_user.setObjectName(u"lbl_user")
        self.lbl_user.setStyleSheet(u"\n"
"color: #3A5080;\n"
"font-family: \"72\";\n"
"font-size: 7.5pt;\n"
"font-weight: 700;\n"
"letter-spacing: 1px;\n"
"background: transparent;\n"
"border: none;\n"
"              ")

        self.vl_f_user.addWidget(self.lbl_user)

        self.frame_user = QFrame(self.login_card)
        self.frame_user.setObjectName(u"frame_user")
        self.frame_user.setMinimumSize(QSize(0, 40))
        self.frame_user.setStyleSheet(u"\n"
"QFrame#frame_user {\n"
"    background-color: #0D1117;\n"
"    border-radius: 8px;\n"
"    border: 1.5px solid #232B3E;\n"
"}\n"
"              ")
        self.hl_user = QHBoxLayout(self.frame_user)
        self.hl_user.setSpacing(8)
        self.hl_user.setObjectName(u"hl_user")
        self.hl_user.setContentsMargins(10, 0, 10, 0)
        self.lbl_user_icon = QLabel(self.frame_user)
        self.lbl_user_icon.setObjectName(u"lbl_user_icon")
        self.lbl_user_icon.setStyleSheet(u"color: #1877F2; font-size: 12pt; background: transparent; border: none;")

        self.hl_user.addWidget(self.lbl_user_icon)

        self.txt_clave = QLineEdit(self.frame_user)
        self.txt_clave.setObjectName(u"txt_clave")
        self.txt_clave.setFont(font4)
        self.txt_clave.setStyleSheet(u"\n"
"QLineEdit {\n"
"    background: transparent;\n"
"    border: none;\n"
"    color: #A8B8D8;\n"
"    font-family: \"72\";\n"
"    font-size: 9pt;\n"
"    padding: 2px;\n"
"}\n"
"                 ")

        self.hl_user.addWidget(self.txt_clave)


        self.vl_f_user.addWidget(self.frame_user)


        self.verticalLayout_card.addLayout(self.vl_f_user)

        self.vl_f_pass = QVBoxLayout()
        self.vl_f_pass.setSpacing(6)
        self.vl_f_pass.setObjectName(u"vl_f_pass")
        self.lbl_f_pass = QLabel(self.login_card)
        self.lbl_f_pass.setObjectName(u"lbl_f_pass")
        self.lbl_f_pass.setStyleSheet(u"\n"
"color: #3A5080;\n"
"font-family: \"72\";\n"
"font-size: 7.5pt;\n"
"font-weight: 700;\n"
"letter-spacing: 1px;\n"
"background: transparent;\n"
"border: none;\n"
"              ")

        self.vl_f_pass.addWidget(self.lbl_f_pass)

        self.frame_pass = QFrame(self.login_card)
        self.frame_pass.setObjectName(u"frame_pass")
        self.frame_pass.setMinimumSize(QSize(0, 40))
        self.frame_pass.setStyleSheet(u"\n"
"QFrame#frame_pass {\n"
"    background-color: #0D1117;\n"
"    border-radius: 8px;\n"
"    border: 1.5px solid #232B3E;\n"
"}\n"
"              ")
        self.hl_pass = QHBoxLayout(self.frame_pass)
        self.hl_pass.setSpacing(8)
        self.hl_pass.setObjectName(u"hl_pass")
        self.hl_pass.setContentsMargins(10, 0, 10, 0)
        self.lbl_pass_icon = QLabel(self.frame_pass)
        self.lbl_pass_icon.setObjectName(u"lbl_pass_icon")
        self.lbl_pass_icon.setStyleSheet(u"color: #1877F2; font-size: 12pt; background: transparent; border: none;")

        self.hl_pass.addWidget(self.lbl_pass_icon)

        self.txt_clave_sap = QLineEdit(self.frame_pass)
        self.txt_clave_sap.setObjectName(u"txt_clave_sap")
        self.txt_clave_sap.setFont(font4)
        self.txt_clave_sap.setStyleSheet(u"\n"
"QLineEdit {\n"
"    background: transparent;\n"
"    border: none;\n"
"    color: #A8B8D8;\n"
"    font-family: \"72\";\n"
"    font-size: 9pt;\n"
"    padding: 2px;\n"
"}\n"
"                 ")
        self.txt_clave_sap.setEchoMode(QLineEdit.EchoMode.Password)

        self.hl_pass.addWidget(self.txt_clave_sap)


        self.vl_f_pass.addWidget(self.frame_pass)


        self.verticalLayout_card.addLayout(self.vl_f_pass)

        self.separator_entorno = QFrame(self.login_card)
        self.separator_entorno.setObjectName(u"separator_entorno")
        self.separator_entorno.setMinimumSize(QSize(0, 1))
        self.separator_entorno.setMaximumSize(QSize(16777215, 1))
        self.separator_entorno.setStyleSheet(u"\n"
"QFrame#separator_entorno {\n"
"    background-color: #232B3E;\n"
"    border: none;\n"
"}\n"
"            ")

        self.verticalLayout_card.addWidget(self.separator_entorno)

        self.lbl_entorno_title = QLabel(self.login_card)
        self.lbl_entorno_title.setObjectName(u"lbl_entorno_title")
        self.lbl_entorno_title.setStyleSheet(u"\n"
"color: #3A5080;\n"
"font-family: \"72\";\n"
"font-size: 7.5pt;\n"
"font-weight: 700;\n"
"letter-spacing: 1px;\n"
"background: transparent;\n"
"border: none;\n"
"            ")

        self.verticalLayout_card.addWidget(self.lbl_entorno_title)

        self.vl_entorno = QVBoxLayout()
        self.vl_entorno.setSpacing(8)
        self.vl_entorno.setObjectName(u"vl_entorno")
        self.hl_entorno_radios = QHBoxLayout()
        self.hl_entorno_radios.setSpacing(20)
        self.hl_entorno_radios.setObjectName(u"hl_entorno_radios")
        self.radio_prd = QRadioButton(self.login_card)
        self.radio_prd.setObjectName(u"radio_prd")
        self.radio_prd.setStyleSheet(u"\n"
"QRadioButton {\n"
"    color: #A8B8D8;\n"
"    background: transparent;\n"
"    font-family: \"72\";\n"
"    font-size: 10pt;\n"
"    border: none;\n"
"    spacing: 6px;\n"
"}\n"
"QRadioButton::indicator {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"    border-radius: 8px;\n"
"    border: 1.5px solid #1877F2;\n"
"    background-color: #0D1117;\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 1.5px solid #4FA3F7;\n"
"    background-color: #1A2236;\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: qlineargradient(x1:0,y1:0,x2:1,y2:1,\n"
"        stop:0 #1877F2, stop:1 #0E5DA9);\n"
"    border-color: #1877F2;\n"
"}\n"
"                ")

        self.hl_entorno_radios.addWidget(self.radio_prd)

        self.radio_qas = QRadioButton(self.login_card)
        self.radio_qas.setObjectName(u"radio_qas")
        self.radio_qas.setStyleSheet(u"\n"
"QRadioButton {\n"
"    color: #A8B8D8;\n"
"    background: transparent;\n"
"    font-family: \"72\";\n"
"    font-size: 10pt;\n"
"    border: none;\n"
"    spacing: 6px;\n"
"}\n"
"QRadioButton::indicator {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"    border-radius: 8px;\n"
"    border: 1.5px solid #1877F2;\n"
"    background-color: #0D1117;\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 1.5px solid #4FA3F7;\n"
"    background-color: #1A2236;\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: qlineargradient(x1:0,y1:0,x2:1,y2:1,\n"
"        stop:0 #1877F2, stop:1 #0E5DA9);\n"
"    border-color: #1877F2;\n"
"}\n"
"                ")

        self.hl_entorno_radios.addWidget(self.radio_qas)

        self.sp_radios = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hl_entorno_radios.addItem(self.sp_radios)


        self.vl_entorno.addLayout(self.hl_entorno_radios)

        self.chx_activo = QCheckBox(self.login_card)
        self.chx_activo.setObjectName(u"chx_activo")
        self.chx_activo.setStyleSheet(u"\n"
"QCheckBox {\n"
"    color: #A8B8D8;\n"
"    background: transparent;\n"
"    font-family: \"72\";\n"
"    font-size: 10pt;\n"
"    border: none;\n"
"    spacing: 6px;\n"
"}\n"
"QCheckBox::indicator {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"    border-radius: 3px;\n"
"    border: 1.5px solid #1877F2;\n"
"    background-color: #0D1117;\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"    border: 1.5px solid #4FA3F7;\n"
"    background-color: #1A2236;\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background-color: #1877F2;\n"
"    border-color: #145DB2;\n"
"}\n"
"QCheckBox::indicator:pressed {\n"
"    background-color: #145DB2;\n"
"}\n"
"              ")

        self.vl_entorno.addWidget(self.chx_activo)


        self.verticalLayout_card.addLayout(self.vl_entorno)

        self.sp_middle = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_card.addItem(self.sp_middle)

        self.hl_buttons = QHBoxLayout()
        self.hl_buttons.setSpacing(10)
        self.hl_buttons.setObjectName(u"hl_buttons")
        self.btn_guardar = QPushButton(self.login_card)
        self.btn_guardar.setObjectName(u"btn_guardar")
        self.btn_guardar.setMinimumSize(QSize(0, 45))
        self.btn_guardar.setFont(font2)
        self.btn_guardar.setStyleSheet(u"\n"
"QPushButton#btn_guardar {\n"
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
"QPushButton#btn_guardar:hover {\n"
"    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,\n"
"        stop:0 #145DB2, stop:1 #1877F2);\n"
"}\n"
"QPushButton#btn_guardar:pressed { background-color: #0F4A99; }\n"
"              ")

        self.hl_buttons.addWidget(self.btn_guardar)

        self.btn_eliminar_perfil = QPushButton(self.login_card)
        self.btn_eliminar_perfil.setObjectName(u"btn_eliminar_perfil")
        self.btn_eliminar_perfil.setMinimumSize(QSize(0, 45))
        self.btn_eliminar_perfil.setFont(font2)
        self.btn_eliminar_perfil.setStyleSheet(u"\n"
"QPushButton#btn_eliminar_perfil {\n"
"    background-color: transparent;\n"
"    color: #E05070;\n"
"    border: 2px solid #7A4A55;\n"
"    border-radius: 8px;\n"
"    font-family: \"72\";\n"
"    font-size: 10pt;\n"
"    font-weight: 600;\n"
"    padding: 6px 12px;\n"
"}\n"
"QPushButton#btn_eliminar_perfil:hover {\n"
"    background-color: #2A1520;\n"
"    color: #FF5577;\n"
"    border-color: #E05070;\n"
"}\n"
"QPushButton#btn_eliminar_perfil:pressed {\n"
"    background-color: #200F18;\n"
"    color: #FF3355;\n"
"}\n"
"              ")

        self.hl_buttons.addWidget(self.btn_eliminar_perfil)


        self.verticalLayout_card.addLayout(self.hl_buttons)


        self.hl_body.addWidget(self.login_card)

        self.vl_lista_area = QVBoxLayout()
        self.vl_lista_area.setSpacing(10)
        self.vl_lista_area.setObjectName(u"vl_lista_area")
        self.hl_lista_header = QHBoxLayout()
        self.hl_lista_header.setSpacing(8)
        self.hl_lista_header.setObjectName(u"hl_lista_header")
        self.lbl_sec_perfiles = QLabel(self.centralwidget)
        self.lbl_sec_perfiles.setObjectName(u"lbl_sec_perfiles")
        self.lbl_sec_perfiles.setStyleSheet(u"\n"
"color: #3A5080;\n"
"font-family: \"72\";\n"
"font-size: 7.5pt;\n"
"font-weight: 700;\n"
"letter-spacing: 1px;\n"
"background: transparent;\n"
"border: none;\n"
"             ")

        self.hl_lista_header.addWidget(self.lbl_sec_perfiles)

        self.lbl_conteo = QLabel(self.centralwidget)
        self.lbl_conteo.setObjectName(u"lbl_conteo")
        self.lbl_conteo.setStyleSheet(u"\n"
"color: #FFFFFF;\n"
"background-color: #1877F2;\n"
"border-radius: 6px;\n"
"font-family: \"72\";\n"
"font-size: 7.5pt;\n"
"font-weight: 700;\n"
"min-width: 18px;\n"
"max-width: 28px;\n"
"min-height: 18px;\n"
"max-height: 18px;\n"
"padding: 0px 4px;\n"
"             ")
        self.lbl_conteo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.hl_lista_header.addWidget(self.lbl_conteo)

        self.sp_lista_h = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hl_lista_header.addItem(self.sp_lista_h)


        self.vl_lista_area.addLayout(self.hl_lista_header)

        self.tbl_usuarios = QTableWidget(self.centralwidget)
        if (self.tbl_usuarios.columnCount() < 4):
            self.tbl_usuarios.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.tbl_usuarios.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tbl_usuarios.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tbl_usuarios.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tbl_usuarios.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.tbl_usuarios.setObjectName(u"tbl_usuarios")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tbl_usuarios.sizePolicy().hasHeightForWidth())
        self.tbl_usuarios.setSizePolicy(sizePolicy)
        self.tbl_usuarios.setStyleSheet(u"\n"
"QTableWidget#tbl_usuarios {\n"
"    background-color: #161B27;\n"
"    color: #A8B8D8;\n"
"    font-family: \"72\";\n"
"    font-size: 13px;\n"
"    border: 1.5px solid #232B3E;\n"
"    border-radius: 10px;\n"
"    padding: 4px;\n"
"    gridline-color: #1E2840;\n"
"    outline: none;\n"
"}\n"
"QTableWidget#tbl_usuarios::item {\n"
"    padding: 8px;\n"
"    border: none;\n"
"}\n"
"QTableWidget#tbl_usuarios::item:selected {\n"
"    background-color: #1877F2;\n"
"    color: #FFFFFF;\n"
"    border-radius: 4px;\n"
"}\n"
"QTableWidget#tbl_usuarios::item:hover {\n"
"    background-color: #1A2236;\n"
"}\n"
"QHeaderView::section {\n"
"    background-color: #0D1117;\n"
"    color: #1877F2;\n"
"    font-family: \"72\";\n"
"    font-size: 13px;\n"
"    font-weight: bold;\n"
"    border: none;\n"
"    border-bottom: 2px solid #1877F2;\n"
"    padding: 6px;\n"
"    text-align: left;\n"
"}\n"
"QTableCornerButton::section {\n"
"    background-color: #0D1117;\n"
"    border: none;\n"
"    border-bottom: 2px solid #1877F2"
                        ";\n"
"}\n"
"QHeaderView::section:vertical {\n"
"    border-bottom: none;\n"
"    border-right: none;\n"
"    width: 0px;\n"
"}\n"
"QScrollBar:vertical {\n"
"    background: #0D1117;\n"
"    width: 6px;\n"
"    border-radius: 3px;\n"
"}\n"
"QScrollBar::handle:vertical {\n"
"    background: #232B3E;\n"
"    border-radius: 3px;\n"
"    min-height: 20px;\n"
"}\n"
"QScrollBar::handle:vertical:hover { background: #1877F2; }\n"
"QScrollBar::add-line:vertical,\n"
"QScrollBar::sub-line:vertical { height: 0px; }\n"
"QScrollBar:horizontal {\n"
"    background: #0D1117;\n"
"    height: 6px;\n"
"    border-radius: 3px;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    background: #232B3E;\n"
"    border-radius: 3px;\n"
"    min-width: 20px;\n"
"}\n"
"QScrollBar::handle:horizontal:hover { background: #1877F2; }\n"
"QScrollBar::add-line:horizontal,\n"
"QScrollBar::sub-line:horizontal { width: 0px; }\n"
"           ")
        self.tbl_usuarios.horizontalHeader().setMinimumSectionSize(80)
        self.tbl_usuarios.horizontalHeader().setDefaultSectionSize(160)
        self.tbl_usuarios.horizontalHeader().setStretchLastSection(True)
        self.tbl_usuarios.verticalHeader().setVisible(False)

        self.vl_lista_area.addWidget(self.tbl_usuarios)


        self.hl_body.addLayout(self.vl_lista_area)


        self.verticalLayout_main.addLayout(self.hl_body)

        credenciales.setCentralWidget(self.centralwidget)

        self.retranslateUi(credenciales)

        QMetaObject.connectSlotsByName(credenciales)
    # setupUi

    def retranslateUi(self, credenciales):
        credenciales.setWindowTitle(QCoreApplication.translate("credenciales", u"Credenciales", None))
        self.label.setText(QCoreApplication.translate("credenciales", u"<html><head/><body><p><span style=\" font-size:20pt;\">\U0001f510 GESTI\U000000d3N DE USUARIOS</span></p></body></html>", None))
        self.btn_nuevo_perfil.setText(QCoreApplication.translate("credenciales", u"+ Nuevo perfil", None))
        self.lbl_form_title.setText(QCoreApplication.translate("credenciales", u"Detalles del Perfil", None))
        self.lbl_f_alias.setText(QCoreApplication.translate("credenciales", u"NOMBRE DEL PERFIL", None))
        self.lbl_alias_icon.setText(QCoreApplication.translate("credenciales", u"\U0001f3f7", None))
        self.txt_usuario.setPlaceholderText(QCoreApplication.translate("credenciales", u"Nombre del perfil", None))
        self.lbl_user.setText(QCoreApplication.translate("credenciales", u"USUARIO SAP", None))
        self.lbl_user_icon.setText(QCoreApplication.translate("credenciales", u"\U0001f464", None))
        self.txt_clave.setPlaceholderText(QCoreApplication.translate("credenciales", u"Usuario SAP", None))
        self.lbl_f_pass.setText(QCoreApplication.translate("credenciales", u"CLAVE SAP", None))
        self.lbl_pass_icon.setText(QCoreApplication.translate("credenciales", u"\U0001f511", None))
        self.txt_clave_sap.setPlaceholderText(QCoreApplication.translate("credenciales", u"Clave SAP", None))
        self.lbl_entorno_title.setText(QCoreApplication.translate("credenciales", u"CONFIGURACI\u00d3N DE ENTORNO", None))
        self.radio_prd.setText(QCoreApplication.translate("credenciales", u"Productivo (PR)", None))
        self.radio_qas.setText(QCoreApplication.translate("credenciales", u"Pruebas (QA)", None))
        self.chx_activo.setText(QCoreApplication.translate("credenciales", u"Usar para ejecuci\u00f3n", None))
        self.btn_guardar.setText(QCoreApplication.translate("credenciales", u"\U0001f4be  Guardar", None))
        self.btn_eliminar_perfil.setText(QCoreApplication.translate("credenciales", u"\u2715  Eliminar", None))
        self.lbl_sec_perfiles.setText(QCoreApplication.translate("credenciales", u"PERFILES CONFIGURADOS", None))
        self.lbl_conteo.setText(QCoreApplication.translate("credenciales", u"0", None))
        ___qtablewidgetitem = self.tbl_usuarios.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("credenciales", u"Alias", None));
        ___qtablewidgetitem1 = self.tbl_usuarios.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("credenciales", u"Usuario SAP", None));
        ___qtablewidgetitem2 = self.tbl_usuarios.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("credenciales", u"Entorno", None));
        ___qtablewidgetitem3 = self.tbl_usuarios.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("credenciales", u"Seleccionado", None));
    # retranslateUi

