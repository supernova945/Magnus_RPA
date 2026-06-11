# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'operaciones.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)
from recursos import recursos_rc

class Ui_menu(object):
    def setupUi(self, menu):
        if not menu.objectName():
            menu.setObjectName(u"menu")
        menu.resize(800, 650)
        font = QFont()
        font.setFamilies([u"72"])
        menu.setFont(font)
        menu.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        icon = QIcon()
        icon.addFile(u"../recursos/magnus.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        menu.setWindowIcon(icon)
        menu.setStyleSheet(u"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\n"
"   GLASSMORPHISM DARK \u2014 OPERACIONES\n"
"   Base: fondo profundo con capa de \"vidrio\" encima\n"
"   \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"\n"
"QMainWindow, QWidget#centralwidget {\n"
"    background-color: #060B14;\n"
"    /* Puntos de luz de fondo simulando profundidad */\n"
"    background-image:\n"
"        radial-gradient(ellipse at 20% 20%, rgba(24,119,242,0.08) 0%, transparent 55%),\n"
"        radial-gradient(ellipse at 80% 75%, rgba(7,94,84,0.07) 0%, transpare"
                        "nt 55%);\n"
"}\n"
"   ")
        self.centralwidget = QWidget(menu)
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

        self.lbl_dropzone = QLabel(self.centralwidget)
        self.lbl_dropzone.setObjectName(u"lbl_dropzone")
        self.lbl_dropzone.setMinimumSize(QSize(0, 120))
        self.lbl_dropzone.setFont(font)
        self.lbl_dropzone.setStyleSheet(u"\n"
"QLabel {\n"
"    border: 2px dashed #232B3E;\n"
"    border-radius: 10px;\n"
"    background-color: #161B27;\n"
"    color: #3A5080;\n"
"    font-size: 12px;\n"
"}\n"
"QLabel:hover {\n"
"    background-color: #1A2236;\n"
"    border: 2px dashed #1877F2;\n"
"    color: #A8B8D8;\n"
"}\n"
"       ")
        self.lbl_dropzone.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_main.addWidget(self.lbl_dropzone)

        self.horizontalLayout_middle = QHBoxLayout()
        self.horizontalLayout_middle.setSpacing(15)
        self.horizontalLayout_middle.setObjectName(u"horizontalLayout_middle")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"\n"
"QFrame#frame {\n"
"    background-color: #161B27;\n"
"    border-radius: 10px;\n"
"    border: 1.5px solid #232B3E;\n"
"}\n"
"         ")
        self.horizontalLayout_frame = QHBoxLayout(self.frame)
        self.horizontalLayout_frame.setSpacing(10)
        self.horizontalLayout_frame.setObjectName(u"horizontalLayout_frame")
        self.horizontalLayout_frame.setContentsMargins(14, 10, 10, 10)
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        font2 = QFont()
        font2.setFamilies([u"72"])
        font2.setPointSize(8)
        font2.setBold(True)
        self.label_2.setFont(font2)
        self.label_2.setStyleSheet(u"\n"
"color: #3A5080;\n"
"font-size: 7.5pt;\n"
"font-weight: 700;\n"
"letter-spacing: 1px;\n"
"background: transparent;\n"
"border: none;\n"
"            ")

        self.horizontalLayout_frame.addWidget(self.label_2)

        self.txt_ruta_archivo = QLineEdit(self.frame)
        self.txt_ruta_archivo.setObjectName(u"txt_ruta_archivo")
        self.txt_ruta_archivo.setEnabled(False)
        self.txt_ruta_archivo.setMinimumSize(QSize(0, 40))
        self.txt_ruta_archivo.setFont(font)
        self.txt_ruta_archivo.setStyleSheet(u"\n"
"QLineEdit {\n"
"    background-color: #0D1117;\n"
"    border: 1.5px solid #232B3E;\n"
"    border-radius: 8px;\n"
"    color: #A8B8D8;\n"
"    font-family: \"72\";\n"
"    padding: 4px 10px;\n"
"}\n"
"QLineEdit:disabled {\n"
"    color: #3A5080;\n"
"    border-color: #1E2840;\n"
"}\n"
"            ")

        self.horizontalLayout_frame.addWidget(self.txt_ruta_archivo)

        self.btn_select_excel = QPushButton(self.frame)
        self.btn_select_excel.setObjectName(u"btn_select_excel")
        self.btn_select_excel.setMinimumSize(QSize(100, 45))
        font3 = QFont()
        font3.setFamilies([u"72"])
        font3.setPointSize(10)
        self.btn_select_excel.setFont(font3)
        self.btn_select_excel.setStyleSheet(u"\n"
"QPushButton#btn_select_excel {\n"
"    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,\n"
"        stop:0 #1877F2, stop:1 #3B8FF5);\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    font-family: \"72\";\n"
"    font-size: 10pt;\n"
"    border: none;\n"
"    padding: 6px 12px;\n"
"}\n"
"QPushButton#btn_select_excel:hover {\n"
"    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,\n"
"        stop:0 #145DB2, stop:1 #1877F2);\n"
"}\n"
"QPushButton#btn_select_excel:pressed {\n"
"    background-color: #0F4A99;\n"
"}\n"
"            ")

        self.horizontalLayout_frame.addWidget(self.btn_select_excel)


        self.horizontalLayout_middle.addWidget(self.frame)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setStyleSheet(u"\n"
"QGroupBox#groupBox {\n"
"    background-color: #161B27;\n"
"    border-radius: 10px;\n"
"    border: 1.5px solid #232B3E;\n"
"}\n"
"         ")
        self.verticalLayout_gb = QVBoxLayout(self.groupBox)
        self.verticalLayout_gb.setSpacing(8)
        self.verticalLayout_gb.setObjectName(u"verticalLayout_gb")
        self.verticalLayout_gb.setContentsMargins(14, 12, 14, 12)
        self.chk_mod_silencioso = QCheckBox(self.groupBox)
        self.chk_mod_silencioso.setObjectName(u"chk_mod_silencioso")
        self.chk_mod_silencioso.setStyleSheet(u"\n"
"QCheckBox#chk_mod_silencioso {\n"
"    color: #A8B8D8;\n"
"    background-color: transparent;\n"
"    font-family: \"72\";\n"
"    font-size: 10pt;\n"
"}\n"
"QCheckBox#chk_mod_silencioso::indicator {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"    border-radius: 8px;\n"
"    border: 1.5px solid #1877F2;\n"
"    background-color: #0D1117;\n"
"}\n"
"QCheckBox#chk_mod_silencioso::indicator:hover {\n"
"    border: 1.5px solid #4FA3F7;\n"
"    background-color: #1A2236;\n"
"}\n"
"QCheckBox#chk_mod_silencioso::indicator:checked {\n"
"    background-color: #1877F2;\n"
"    border: 1.5px solid #145DB2;\n"
"}\n"
"QCheckBox#chk_mod_silencioso::indicator:pressed {\n"
"    background-color: #145DB2;\n"
"}\n"
"            ")

        self.verticalLayout_gb.addWidget(self.chk_mod_silencioso)

        self.chk_reg_detallado = QCheckBox(self.groupBox)
        self.chk_reg_detallado.setObjectName(u"chk_reg_detallado")
        self.chk_reg_detallado.setStyleSheet(u"\n"
"QCheckBox#chk_reg_detallado {\n"
"    color: #A8B8D8;\n"
"    background-color: transparent;\n"
"    font-family: \"72\";\n"
"    font-size: 10pt;\n"
"}\n"
"QCheckBox#chk_reg_detallado::indicator {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"    border-radius: 8px;\n"
"    border: 1.5px solid #1877F2;\n"
"    background-color: #0D1117;\n"
"}\n"
"QCheckBox#chk_reg_detallado::indicator:hover {\n"
"    border: 1.5px solid #4FA3F7;\n"
"    background-color: #1A2236;\n"
"}\n"
"QCheckBox#chk_reg_detallado::indicator:checked {\n"
"    background-color: #1877F2;\n"
"    border: 1.5px solid #145DB2;\n"
"}\n"
"QCheckBox#chk_reg_detallado::indicator:pressed {\n"
"    background-color: #145DB2;\n"
"}\n"
"            ")

        self.verticalLayout_gb.addWidget(self.chk_reg_detallado)


        self.horizontalLayout_middle.addWidget(self.groupBox)


        self.verticalLayout_main.addLayout(self.horizontalLayout_middle)

        self.tbl_archivo = QTableWidget(self.centralwidget)
        if (self.tbl_archivo.columnCount() < 7):
            self.tbl_archivo.setColumnCount(7)
        __qtablewidgetitem = QTableWidgetItem()
        self.tbl_archivo.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tbl_archivo.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tbl_archivo.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tbl_archivo.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tbl_archivo.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tbl_archivo.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tbl_archivo.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        self.tbl_archivo.setObjectName(u"tbl_archivo")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tbl_archivo.sizePolicy().hasHeightForWidth())
        self.tbl_archivo.setSizePolicy(sizePolicy)
        self.tbl_archivo.setStyleSheet(u"\n"
"QTableWidget#tbl_archivo {\n"
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
"QTableWidget#tbl_archivo::item:selected {\n"
"    background-color: #1877F2;\n"
"    color: #FFFFFF;\n"
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
"}\n"
"QTableCornerButton::section {\n"
"    background-color: #0D1117;\n"
"    border: none;\n"
"    border-bottom: 2px solid #1877F2;\n"
"}\n"
"QHeaderView::section:vertical {\n"
"    border-bottom: none;\n"
"    border-right: 2px solid #1877F2;\n"
"}\n"
"QScrollBar:vertical {\n"
"    background: #0D1117;\n"
"    width: 6px;\n"
"    border-radius: 3px;\n"
"}\n"
""
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
"       ")

        self.verticalLayout_main.addWidget(self.tbl_archivo)

        self.horizontalLayout_pagination = QHBoxLayout()
        self.horizontalLayout_pagination.setSpacing(8)
        self.horizontalLayout_pagination.setObjectName(u"horizontalLayout_pagination")
        self.btn_anterior = QPushButton(self.centralwidget)
        self.btn_anterior.setObjectName(u"btn_anterior")
        self.btn_anterior.setMinimumSize(QSize(100, 36))
        self.btn_anterior.setFont(font3)
        self.btn_anterior.setStyleSheet(u"\n"
"QPushButton#btn_anterior {\n"
"    background-color: transparent;\n"
"    color: #1877F2;\n"
"    border: 1.5px solid #232B3E;\n"
"    border-radius: 8px;\n"
"    font-family: \"72\";\n"
"    font-size: 10pt;\n"
"    padding: 4px 12px;\n"
"}\n"
"QPushButton#btn_anterior:hover {\n"
"    background-color: #1A2236;\n"
"    border-color: #1877F2;\n"
"    color: #4FA3F7;\n"
"}\n"
"QPushButton#btn_anterior:pressed {\n"
"    background-color: #172035;\n"
"}\n"
"QPushButton#btn_anterior:disabled {\n"
"    color: #2A3A5A;\n"
"    border-color: #1A2236;\n"
"}\n"
"         ")

        self.horizontalLayout_pagination.addWidget(self.btn_anterior)

        self.btn_siguiente = QPushButton(self.centralwidget)
        self.btn_siguiente.setObjectName(u"btn_siguiente")
        self.btn_siguiente.setMinimumSize(QSize(100, 36))
        self.btn_siguiente.setFont(font3)
        self.btn_siguiente.setStyleSheet(u"\n"
"QPushButton#btn_siguiente {\n"
"    background-color: transparent;\n"
"    color: #1877F2;\n"
"    border: 1.5px solid #232B3E;\n"
"    border-radius: 8px;\n"
"    font-family: \"72\";\n"
"    font-size: 10pt;\n"
"    padding: 4px 12px;\n"
"}\n"
"QPushButton#btn_siguiente:hover {\n"
"    background-color: #1A2236;\n"
"    border-color: #1877F2;\n"
"    color: #4FA3F7;\n"
"}\n"
"QPushButton#btn_siguiente:pressed {\n"
"    background-color: #172035;\n"
"}\n"
"QPushButton#btn_siguiente:disabled {\n"
"    color: #2A3A5A;\n"
"    border-color: #1A2236;\n"
"}\n"
"         ")

        self.horizontalLayout_pagination.addWidget(self.btn_siguiente)

        self.lbl_paginacion = QLabel(self.centralwidget)
        self.lbl_paginacion.setObjectName(u"lbl_paginacion")
        font4 = QFont()
        font4.setFamilies([u"72"])
        font4.setPointSize(9)
        self.lbl_paginacion.setFont(font4)
        self.lbl_paginacion.setStyleSheet(u"\n"
"QLabel#lbl_paginacion {\n"
"    color: #3A5080;\n"
"    background: transparent;\n"
"    border: none;\n"
"    font-family: \"72\";\n"
"    font-size: 9pt;\n"
"    padding: 0px 6px;\n"
"}\n"
"         ")

        self.horizontalLayout_pagination.addWidget(self.lbl_paginacion)

        self.horizontalSpacer_pagination = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_pagination.addItem(self.horizontalSpacer_pagination)

        self.lbl_filas_por_pagina = QLabel(self.centralwidget)
        self.lbl_filas_por_pagina.setObjectName(u"lbl_filas_por_pagina")
        self.lbl_filas_por_pagina.setFont(font4)
        self.lbl_filas_por_pagina.setStyleSheet(u"\n"
"QLabel#lbl_filas_por_pagina {\n"
"    color: #3A5080;\n"
"    background: transparent;\n"
"    border: none;\n"
"    font-family: \"72\";\n"
"    font-size: 9pt;\n"
"}\n"
"         ")

        self.horizontalLayout_pagination.addWidget(self.lbl_filas_por_pagina)

        self.cmb_filas_por_pagina = QComboBox(self.centralwidget)
        self.cmb_filas_por_pagina.addItem("")
        self.cmb_filas_por_pagina.addItem("")
        self.cmb_filas_por_pagina.addItem("")
        self.cmb_filas_por_pagina.setObjectName(u"cmb_filas_por_pagina")
        self.cmb_filas_por_pagina.setMinimumSize(QSize(80, 36))
        self.cmb_filas_por_pagina.setFont(font3)
        self.cmb_filas_por_pagina.setStyleSheet(u"\n"
"QComboBox#cmb_filas_por_pagina {\n"
"    background-color: #161B27;\n"
"    color: #A8B8D8;\n"
"    border: 1.5px solid #232B3E;\n"
"    border-radius: 8px;\n"
"    font-family: \"72\";\n"
"    font-size: 10pt;\n"
"    padding: 4px 10px;\n"
"}\n"
"QComboBox#cmb_filas_por_pagina:hover {\n"
"    border-color: #1877F2;\n"
"}\n"
"QComboBox#cmb_filas_por_pagina::drop-down {\n"
"    border: none;\n"
"    width: 20px;\n"
"}\n"
"QComboBox#cmb_filas_por_pagina::down-arrow {\n"
"    image: none;\n"
"    border-left: 4px solid transparent;\n"
"    border-right: 4px solid transparent;\n"
"    border-top: 5px solid #1877F2;\n"
"    width: 0px;\n"
"    height: 0px;\n"
"}\n"
"QComboBox#cmb_filas_por_pagina QAbstractItemView {\n"
"    background-color: #161B27;\n"
"    color: #A8B8D8;\n"
"    border: 1.5px solid #1877F2;\n"
"    border-radius: 6px;\n"
"    selection-background-color: #1877F2;\n"
"    selection-color: #FFFFFF;\n"
"}\n"
"         ")

        self.horizontalLayout_pagination.addWidget(self.cmb_filas_por_pagina)


        self.verticalLayout_main.addLayout(self.horizontalLayout_pagination)

        self.horizontalLayout_bottom = QHBoxLayout()
        self.horizontalLayout_bottom.setObjectName(u"horizontalLayout_bottom")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_bottom.addItem(self.horizontalSpacer)

        self.btn_limpiar = QPushButton(self.centralwidget)
        self.btn_limpiar.setObjectName(u"btn_limpiar")
        self.btn_limpiar.setMinimumSize(QSize(100, 45))
        font5 = QFont()
        font5.setFamilies([u"72"])
        font5.setPointSize(10)
        font5.setWeight(QFont.DemiBold)
        self.btn_limpiar.setFont(font5)
        self.btn_limpiar.setStyleSheet(u"\n"
"QPushButton#btn_limpiar {\n"
"    background-color: transparent;\n"
"    color: #1877F2;\n"
"    border: 2px solid #1877F2;\n"
"    border-radius: 8px;\n"
"    font-family: \"72\";\n"
"    font-size: 10pt;\n"
"    font-weight: 600;\n"
"    padding: 6px 12px;\n"
"}\n"
"QPushButton#btn_limpiar:hover {\n"
"    background-color: #1A2236;\n"
"    color: #4FA3F7;\n"
"    border-color: #4FA3F7;\n"
"}\n"
"QPushButton#btn_limpiar:pressed {\n"
"    background-color: #172035;\n"
"    color: #1877F2;\n"
"}\n"
"         ")

        self.horizontalLayout_bottom.addWidget(self.btn_limpiar)

        self.btn_iniciar = QPushButton(self.centralwidget)
        self.btn_iniciar.setObjectName(u"btn_iniciar")
        self.btn_iniciar.setMinimumSize(QSize(100, 45))
        self.btn_iniciar.setFont(font5)
        self.btn_iniciar.setStyleSheet(u"\n"
"QPushButton#btn_iniciar {\n"
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
"QPushButton#btn_iniciar:hover {\n"
"    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,\n"
"        stop:0 #145DB2, stop:1 #1877F2);\n"
"}\n"
"QPushButton#btn_iniciar:pressed {\n"
"    background-color: #0F4A99;\n"
"}\n"
"         ")

        self.horizontalLayout_bottom.addWidget(self.btn_iniciar)

        self.btn_detener = QPushButton(self.centralwidget)
        self.btn_detener.setObjectName(u"btn_detener")
        self.btn_detener.setMinimumSize(QSize(100, 45))
        self.btn_detener.setFont(font5)
        self.btn_detener.setStyleSheet(u"\n"
"QPushButton#btn_detener {\n"
"    background-color: transparent;\n"
"    color: #E05070;\n"
"    border: 2px solid #7A4A55;\n"
"    border-radius: 8px;\n"
"    font-family: \"72\";\n"
"    font-size: 10pt;\n"
"    font-weight: 600;\n"
"    padding: 6px 12px;\n"
"}\n"
"QPushButton#btn_detener:hover {\n"
"    background-color: #2A1520;\n"
"    color: #FF5577;\n"
"    border-color: #E05070;\n"
"}\n"
"QPushButton#btn_detener:pressed {\n"
"    background-color: #200F18;\n"
"    color: #FF3355;\n"
"}\n"
"         ")

        self.horizontalLayout_bottom.addWidget(self.btn_detener)


        self.verticalLayout_main.addLayout(self.horizontalLayout_bottom)

        menu.setCentralWidget(self.centralwidget)

        self.retranslateUi(menu)

        QMetaObject.connectSlotsByName(menu)
    # setupUi

    def retranslateUi(self, menu):
        menu.setWindowTitle(QCoreApplication.translate("menu", u"Magnus", None))
        self.label.setText(QCoreApplication.translate("menu", u"<html><head/><body><p><span style=\" font-size:20pt;\">\U0001f579\U0000fe0f /DBM/CASHDESK</span></p></body></html>", None))
        self.lbl_dropzone.setText(QCoreApplication.translate("menu", u"<html><head/><body><p align=\"center\"><span style=\" font-size:28pt;\">\U0001f4c1</span><br/><span style=\" font-size:9pt; color:#3A5080;\">\U000000a1 Arrastra y suelta tu <br/>archivo aqu\U000000ed ! </span></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("menu", u"RUTA", None))
        self.txt_ruta_archivo.setPlaceholderText(QCoreApplication.translate("menu", u"Ruta del archivo...", None))
        self.btn_select_excel.setText(QCoreApplication.translate("menu", u"Explorar \U0001f4c2", None))
        self.chk_mod_silencioso.setText(QCoreApplication.translate("menu", u"Modo Silencioso", None))
        self.chk_reg_detallado.setText(QCoreApplication.translate("menu", u"Registro Detallado", None))
        ___qtablewidgetitem = self.tbl_archivo.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("menu", u"Sociedad", None));
        ___qtablewidgetitem1 = self.tbl_archivo.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("menu", u"Cliente", None));
        ___qtablewidgetitem2 = self.tbl_archivo.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("menu", u"No Doc", None));
        ___qtablewidgetitem3 = self.tbl_archivo.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("menu", u"Clase", None));
        ___qtablewidgetitem4 = self.tbl_archivo.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("menu", u"Banco", None));
        ___qtablewidgetitem5 = self.tbl_archivo.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("menu", u"Fecha", None));
        ___qtablewidgetitem6 = self.tbl_archivo.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("menu", u"Resultado", None));
        self.btn_anterior.setText(QCoreApplication.translate("menu", u"\u2b05\ufe0f Anterior", None))
        self.btn_siguiente.setText(QCoreApplication.translate("menu", u"Siguiente \u27a1\ufe0f", None))
        self.lbl_paginacion.setText(QCoreApplication.translate("menu", u"Mostrando 0 - 0 de 0", None))
        self.lbl_filas_por_pagina.setText(QCoreApplication.translate("menu", u"Filas por p\u00e1gina:", None))
        self.cmb_filas_por_pagina.setItemText(0, QCoreApplication.translate("menu", u"50", None))
        self.cmb_filas_por_pagina.setItemText(1, QCoreApplication.translate("menu", u"100", None))
        self.cmb_filas_por_pagina.setItemText(2, QCoreApplication.translate("menu", u"500", None))

        self.btn_limpiar.setText(QCoreApplication.translate("menu", u"Limpiar", None))
        self.btn_iniciar.setText(QCoreApplication.translate("menu", u"Iniciar ", None))
        self.btn_detener.setText(QCoreApplication.translate("menu", u"Detener", None))
    # retranslateUi

