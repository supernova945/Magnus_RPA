################################################################################
## Form generated from reading UI file 'about.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QSize, Qt
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import (
    QFormLayout,
    QFrame,
    QLabel,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


class Ui_about:
    def setupUi(self, about):
        if not about.objectName():
            about.setObjectName("about")
        about.resize(800, 650)
        font = QFont()
        font.setFamilies(["72"])
        about.setFont(font)
        icon = QIcon()
        icon.addFile("../magnus.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        about.setWindowIcon(icon)
        about.setStyleSheet(
            "\n"
            "QMainWindow, QWidget#centralwidget {\n"
            "    background-color: #0D1117;\n"
            "}\n"
            "   "
        )
        self.centralwidget = QWidget(about)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_main = QVBoxLayout(self.centralwidget)
        self.verticalLayout_main.setObjectName("verticalLayout_main")
        self.verticalSpacer_top = QSpacerItem(
            0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout_main.addItem(self.verticalSpacer_top)

        self.about_card = QFrame(self.centralwidget)
        self.about_card.setObjectName("about_card")
        self.about_card.setMinimumSize(QSize(450, 0))
        self.about_card.setStyleSheet(
            "\n"
            "QFrame#about_card {\n"
            "    border-radius: 14px;\n"
            "    background-color: #161B27;\n"
            "    border: 1.5px solid #232B3E;\n"
            "}\n"
            "QLabel {\n"
            "    background: transparent;\n"
            "    border: none;\n"
            "}\n"
            "       "
        )
        self.verticalLayout_card = QVBoxLayout(self.about_card)
        self.verticalLayout_card.setSpacing(25)
        self.verticalLayout_card.setObjectName("verticalLayout_card")
        self.verticalLayout_card.setContentsMargins(40, 40, 40, 40)
        self.label = QLabel(self.about_card)
        self.label.setObjectName("label")
        font1 = QFont()
        font1.setFamilies(["72"])
        font1.setPointSize(18)
        font1.setBold(True)
        self.label.setFont(font1)
        self.label.setStyleSheet("color: #1877F2;")

        self.verticalLayout_card.addWidget(self.label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.label_2 = QLabel(self.about_card)
        self.label_2.setObjectName("label_2")
        font2 = QFont()
        font2.setFamilies(["72"])
        font2.setPointSize(11)
        self.label_2.setFont(font2)
        self.label_2.setStyleSheet("color: #3A5080;")

        self.verticalLayout_card.addWidget(
            self.label_2, 0, Qt.AlignmentFlag.AlignHCenter
        )

        self.sep_card = QFrame(self.about_card)
        self.sep_card.setObjectName("sep_card")
        self.sep_card.setMinimumSize(QSize(0, 1))
        self.sep_card.setMaximumSize(QSize(16777215, 1))
        self.sep_card.setStyleSheet(
            "\n"
            "QFrame#sep_card {\n"
            "    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,\n"
            "        stop:0 transparent,\n"
            "        stop:0.15 #1877F2,\n"
            "        stop:0.85 #075E54,\n"
            "        stop:1 transparent);\n"
            "    border: none;\n"
            "}\n"
            "          "
        )

        self.verticalLayout_card.addWidget(self.sep_card)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.formLayout.setHorizontalSpacing(20)
        self.formLayout.setVerticalSpacing(15)
        self.label_24 = QLabel(self.about_card)
        self.label_24.setObjectName("label_24")
        font3 = QFont()
        font3.setFamilies(["72"])
        font3.setPointSize(8)
        font3.setBold(True)
        self.label_24.setFont(font3)
        self.label_24.setStyleSheet(
            "color: #3A5080; font-size: 7.5pt; font-weight: 700;"
        )

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_24)

        self.label_26 = QLabel(self.about_card)
        self.label_26.setObjectName("label_26")
        font4 = QFont()
        font4.setFamilies(["72"])
        font4.setPointSize(10)
        self.label_26.setFont(font4)
        self.label_26.setStyleSheet("color: #A8B8D8;")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.label_26)

        self.label_18 = QLabel(self.about_card)
        self.label_18.setObjectName("label_18")
        self.label_18.setFont(font3)
        self.label_18.setStyleSheet(
            "color: #3A5080; font-size: 7.5pt; font-weight: 700;"
        )

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_18)

        self.label_22 = QLabel(self.about_card)
        self.label_22.setObjectName("label_22")
        self.label_22.setFont(font4)
        self.label_22.setStyleSheet("color: #A8B8D8;")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.label_22)

        self.label_23 = QLabel(self.about_card)
        self.label_23.setObjectName("label_23")
        self.label_23.setFont(font3)
        self.label_23.setStyleSheet(
            "color: #3A5080; font-size: 7.5pt; font-weight: 700;"
        )

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_23)

        self.label_21 = QLabel(self.about_card)
        self.label_21.setObjectName("label_21")
        self.label_21.setFont(font4)
        self.label_21.setStyleSheet("color: #A8B8D8;")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.label_21)

        self.label_19 = QLabel(self.about_card)
        self.label_19.setObjectName("label_19")
        self.label_19.setFont(font3)
        self.label_19.setStyleSheet(
            "color: #3A5080; font-size: 7.5pt; font-weight: 700;"
        )

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_19)

        self.label_25 = QLabel(self.about_card)
        self.label_25.setObjectName("label_25")
        self.label_25.setFont(font4)
        self.label_25.setStyleSheet("color: #A8B8D8;")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.label_25)

        self.label_16 = QLabel(self.about_card)
        self.label_16.setObjectName("label_16")
        self.label_16.setFont(font3)
        self.label_16.setStyleSheet(
            "color: #3A5080; font-size: 7.5pt; font-weight: 700;"
        )

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_16)

        self.label_20 = QLabel(self.about_card)
        self.label_20.setObjectName("label_20")
        font5 = QFont()
        font5.setFamilies(["72"])
        font5.setPointSize(10)
        font5.setBold(True)
        self.label_20.setFont(font5)
        self.label_20.setStyleSheet("color: #075E54;")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.label_20)

        self.verticalLayout_card.addLayout(self.formLayout)

        self.verticalLayout_main.addWidget(
            self.about_card, 0, Qt.AlignmentFlag.AlignHCenter
        )

        self.verticalSpacer_bottom = QSpacerItem(
            0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout_main.addItem(self.verticalSpacer_bottom)

        about.setCentralWidget(self.centralwidget)

        self.retranslateUi(about)

        QMetaObject.connectSlotsByName(about)

    # setupUi

    def retranslateUi(self, about):
        about.setWindowTitle(QCoreApplication.translate("about", "Acerca De", None))
        self.label.setText(
            QCoreApplication.translate(
                "about",
                '<html><head/><body><p align="center"><span style=" font-size:20pt;">\U0001f468\U0001f3fc\U0000200d\U0001f4bb MAGNUS</span></p></body></html>',
                None,
            )
        )
        self.label_2.setText(QCoreApplication.translate("about", "RPA SOLUTIONS", None))
        self.label_24.setText(
            QCoreApplication.translate("about", "DESARROLLADO POR:", None)
        )
        self.label_26.setText(
            QCoreApplication.translate(
                "about", "\U0001faaa Franco Paolo L\U000000f3pez G\U000000e1lvez", None
            )
        )
        self.label_18.setText(
            QCoreApplication.translate("about", "CORREO PERSONAL:", None)
        )
        self.label_22.setText(
            QCoreApplication.translate(
                "about", "\U0001f4e7 francopaolo_lg@outlook.com", None
            )
        )
        self.label_23.setText(
            QCoreApplication.translate("about", "CORREO EMPRESARIAL:", None)
        )
        self.label_21.setText(
            QCoreApplication.translate(
                "about", "\u2709\ufe0f alfredo.jimenez@crediopciones.com", None
            )
        )
        self.label_19.setText(
            QCoreApplication.translate("about", "Id COLABORADOR:", None)
        )
        self.label_25.setText(
            QCoreApplication.translate("about", "\U0001f194 11734", None)
        )
        self.label_16.setText(
            QCoreApplication.translate("about", "VERSI\u00d3N DEL SISTEMA:", None)
        )
        self.label_20.setText(
            QCoreApplication.translate(
                "about",
                '<html><head/><body><p><span style=" font-weight:400;">\U0001f4be 0.0.0 versi\U000000f3n beta</span></p></body></html>',
                None,
            )
        )

    # retranslateUi
