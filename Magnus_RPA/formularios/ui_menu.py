# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'menu.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(897, 635)
        font = QFont()
        font.setFamilies([u"72"])
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.slide_menu_contanier = QFrame(self.centralwidget)
        self.slide_menu_contanier.setObjectName(u"slide_menu_contanier")
        self.slide_menu_contanier.setMaximumSize(QSize(200, 16777215))
        self.slide_menu_contanier.setFont(font)
        self.slide_menu_contanier.setStyleSheet(u"\n"
"/* \u2500\u2500 Contenedores padre e hijo \u2500\u2500 */\n"
"#slide_menu_contanier, #silde_menu {\n"
"    background-color: #161B27;\n"
"    border: none;\n"
"}\n"
"#slide_menu_contanier {\n"
"    border-right: 1px solid #232B3E;\n"
"}\n"
"\n"
"/* \u2500\u2500 Barra degradado superior \u2500\u2500 */\n"
"#silde_menu #top_accent {\n"
"    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,\n"
"        stop:0 #1877F2, stop:0.5 #4FA3F7, stop:1 #075E54);\n"
"    border: none;\n"
"}\n"
"\n"
"/* \u2500\u2500 Label t\u00edtulo \u2500\u2500 */\n"
"#silde_menu QLabel {\n"
"    color: #1877F2;\n"
"    font-family: \"72\";\n"
"    font-weight: bold;\n"
"    padding: 15px 10px;\n"
"    background: transparent;\n"
"    border: none;\n"
"}\n"
"\n"
"/* \u2500\u2500 Botones generales \u2500\u2500 */\n"
"#silde_menu QPushButton {\n"
"    background-color: transparent;\n"
"    color: #A8B8D8;\n"
"    font-size: 14px;\n"
"    text-align: left;\n"
"    padding: 12px 14px;\n"
"    border: none;\n"
"    margin: 2px 8px;\n"
"}\n"
""
                        "\n"
"#silde_menu QPushButton:hover {\n"
"    background-color: #1E2840;\n"
"    color: #1877F2;\n"
"    border-bottom: 2px solid #1877F2;\n"
"}\n"
"       ")
        self.slide_menu_contanier.setFrameShape(QFrame.Shape.StyledPanel)
        self.slide_menu_contanier.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.slide_menu_contanier)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.silde_menu = QFrame(self.slide_menu_contanier)
        self.silde_menu.setObjectName(u"silde_menu")
        self.silde_menu.setMinimumSize(QSize(196, 0))
        self.silde_menu.setStyleSheet(u"")
        self.silde_menu.setFrameShape(QFrame.Shape.StyledPanel)
        self.silde_menu.setFrameShadow(QFrame.Shadow.Raised)
        self.top_accent = QFrame(self.silde_menu)
        self.top_accent.setObjectName(u"top_accent")
        self.top_accent.setGeometry(QRect(0, 0, 196, 4))
        self.top_accent.setStyleSheet(u"\n"
"QFrame#top_accent {\n"
"    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,\n"
"        stop:0 #1877F2, stop:0.5 #4FA3F7, stop:1 #075E54);\n"
"    border: none;\n"
"}\n"
"           ")
        self.btn_analitica = QPushButton(self.silde_menu)
        self.btn_analitica.setObjectName(u"btn_analitica")
        self.btn_analitica.setGeometry(QRect(0, 70, 191, 61))
        self.btn_analitica.setFont(font)
        self.btn_analitica.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_procesar_datos = QPushButton(self.silde_menu)
        self.btn_procesar_datos.setObjectName(u"btn_procesar_datos")
        self.btn_procesar_datos.setGeometry(QRect(0, 130, 191, 61))
        self.btn_procesar_datos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_credenciales = QPushButton(self.silde_menu)
        self.btn_credenciales.setObjectName(u"btn_credenciales")
        self.btn_credenciales.setGeometry(QRect(0, 190, 191, 61))
        self.btn_credenciales.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_acerca_de = QPushButton(self.silde_menu)
        self.btn_acerca_de.setObjectName(u"btn_acerca_de")
        self.btn_acerca_de.setGeometry(QRect(0, 250, 191, 61))
        self.btn_acerca_de.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_salir = QPushButton(self.silde_menu)
        self.btn_salir.setObjectName(u"btn_salir")
        self.btn_salir.setGeometry(QRect(0, 310, 191, 61))
        self.btn_salir.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_inicio = QPushButton(self.silde_menu)
        self.btn_inicio.setObjectName(u"btn_inicio")
        self.btn_inicio.setGeometry(QRect(0, 8, 190, 61))
        self.btn_inicio.setFont(font)
        self.btn_inicio.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.verticalLayout_2.addWidget(self.silde_menu)


        self.horizontalLayout.addWidget(self.slide_menu_contanier)

        self.main_body = QFrame(self.centralwidget)
        self.main_body.setObjectName(u"main_body")
        self.main_body.setStyleSheet(u"\n"
"QFrame#main_body {\n"
"    background-color: #0D1117;\n"
"    border: none;\n"
"}\n"
"       ")
        self.main_body.setFrameShape(QFrame.Shape.StyledPanel)
        self.main_body.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.main_body)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.header_frame = QFrame(self.main_body)
        self.header_frame.setObjectName(u"header_frame")
        self.header_frame.setMaximumSize(QSize(16777215, 35))
        self.header_frame.setStyleSheet(u"\n"
"QFrame#header_frame {\n"
"    background-color: #161B27;\n"
"    border: none;\n"
"    border-bottom: 1px solid #232B3E;\n"
"}\n"
"\n"
"/* \u2500\u2500 Barra de acento del header \u2500\u2500 */\n"
"QFrame#header_top_accent {\n"
"    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,\n"
"        stop:0 #075E54, stop:1 #053D37);\n"
"    border: none;\n"
"    min-height: 4px;\n"
"    max-height: 4px;\n"
"}\n"
"\n"
"/* Botones sin hover ni pressed */\n"
"QFrame#header_frame #pushButton_3,\n"
"QFrame#header_frame #pushButton_2,\n"
"QFrame#header_frame #pushButton {\n"
"    background: transparent;\n"
"    border: none;\n"
"}\n"
"          ")
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
        self.label_2 = QLabel(self.header_frame)
        self.label_2.setObjectName(u"label_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setFamilies([u"72"])
        font1.setPointSize(10)
        font1.setBold(True)
        self.label_2.setFont(font1)
        self.label_2.setStyleSheet(u"\n"
"color: #1877F2;\n"
"background: transparent;\n"
"border: none;\n"
"padding: 0 8px;\n"
"               ")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.header_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.header_spacer)

        self.pushButton_3 = QPushButton(self.header_frame)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMinimumSize(QSize(35, 35))
        self.pushButton_3.setMaximumSize(QSize(35, 35))
        icon = QIcon()
        icon.addFile(u":/icons/icons/minimizar.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_3.setIcon(icon)
        self.pushButton_3.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.pushButton_3)

        self.pushButton_2 = QPushButton(self.header_frame)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(35, 35))
        self.pushButton_2.setMaximumSize(QSize(35, 35))
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/maximizar.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_2.setIcon(icon1)
        self.pushButton_2.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.pushButton_2)

        self.pushButton = QPushButton(self.header_frame)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(35, 35))
        self.pushButton.setMaximumSize(QSize(35, 35))
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/cerrar.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton.setIcon(icon2)
        self.pushButton.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.pushButton)


        self.verticalLayout_header.addLayout(self.horizontalLayout_2)


        self.verticalLayout.addWidget(self.header_frame)

        self.main_body_contents = QFrame(self.main_body)
        self.main_body_contents.setObjectName(u"main_body_contents")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.main_body_contents.sizePolicy().hasHeightForWidth())
        self.main_body_contents.setSizePolicy(sizePolicy1)
        self.main_body_contents.setStyleSheet(u"\n"
"QFrame#main_body_contents {\n"
"    background-color: #0D1117;\n"
"    border: none;\n"
"}\n"
"          ")
        self.main_body_contents.setFrameShape(QFrame.Shape.StyledPanel)
        self.main_body_contents.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.main_body_contents)


        self.horizontalLayout.addWidget(self.main_body)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
#if QT_CONFIG(tooltip)
        self.btn_analitica.setToolTip(QCoreApplication.translate("MainWindow", u"M\u00e9tricas y estad\u00edsticas de operaci\u00f3n", None))
#endif // QT_CONFIG(tooltip)
        self.btn_analitica.setText(QCoreApplication.translate("MainWindow", u"\U0001f4ca     An\U000000e1litica", None))
#if QT_CONFIG(tooltip)
        self.btn_procesar_datos.setToolTip(QCoreApplication.translate("MainWindow", u"Control de registros y operaciones", None))
#endif // QT_CONFIG(tooltip)
        self.btn_procesar_datos.setText(QCoreApplication.translate("MainWindow", u"\u26a1     Gestionar", None))
#if QT_CONFIG(tooltip)
        self.btn_credenciales.setToolTip(QCoreApplication.translate("MainWindow", u"Gesti\u00f3n de cuentas y accesos", None))
#endif // QT_CONFIG(tooltip)
        self.btn_credenciales.setText(QCoreApplication.translate("MainWindow", u"\U0001faaa     Usuarios", None))
#if QT_CONFIG(tooltip)
        self.btn_acerca_de.setToolTip(QCoreApplication.translate("MainWindow", u"Informaci\u00f3n y versi\u00f3n del sistema", None))
#endif // QT_CONFIG(tooltip)
        self.btn_acerca_de.setText(QCoreApplication.translate("MainWindow", u"\U0001f468\U0001f3fc\U0000200d\U0001f4bb     Acerca De", None))
        self.btn_salir.setText(QCoreApplication.translate("MainWindow", u"\U0001f6aa     Salir", None))
        self.btn_inicio.setText(QCoreApplication.translate("MainWindow", u"\U0001f3e0", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\U0001f916 MAGNUS RPA", None))
        self.pushButton_3.setText("")
        self.pushButton_2.setText("")
        self.pushButton.setText("")
    # retranslateUi

