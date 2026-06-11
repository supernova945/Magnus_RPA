import sys
import os

# Añadir el directorio raíz al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtCore import Qt, QPropertyAnimation, QRect, QEvent, QEasingCurve
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QStackedWidget

from vistas.operaciones import MagnusApp
from vistas.usuarios import ControladorUsuarios
from vistas.dashboard import DemoDashboardFull

from formularios.ui_menu import Ui_MainWindow
from formularios.ui_about import Ui_about

class ContenedorPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 1. Cargar UI base compilada
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._is_maximized = False
        
        # 2. Configuración Frameless para quitar la barra de título nativa de Windows (y sus botones)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.setWindowTitle("Magnus")
        self.resize(850, 650)
        self.setMinimumSize(850, 650)
        
        # Opcional: Centrar y configurar tamaño base para poder redimensionar
        from PySide6.QtWidgets import QSizeGrip
        self.grip = QSizeGrip(self)
        self.grip.resize(20, 20)
        self.grip.setStyleSheet("background: transparent;")
        self.grip.raise_()
        
        # 3. Extraer elementos de la interfaz generada por ui_menu.py
        self.menu_lateral = self.ui.slide_menu_contanier
        self.contenedor_paginas = self.ui.main_body_contents
        
        # Configurar el espacio para las vistas
        from PySide6.QtWidgets import QVBoxLayout, QLabel
        self.layout_paginas = QVBoxLayout(self.contenedor_paginas)
        self.layout_paginas.setContentsMargins(0, 0, 0, 0)
        
        self.contenedor_vistas = QStackedWidget(self)
        self.layout_paginas.addWidget(self.contenedor_vistas)
        
        # Iniciar Vistas Secundarias
        self.vista_bienvenida = QWidget()
        lay_bienvenida = QVBoxLayout(self.vista_bienvenida)
        
        lbl_titulo = QLabel("¡Bienvenido a MAGNUS RPA!")
        lbl_titulo.setStyleSheet("font-size: 28px; font-weight: bold; color: #1877F2;")
        lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        lbl_subtitulo = QLabel("Seleccione una opción en el menú lateral para comenzar")
        lbl_subtitulo.setStyleSheet("font-size: 14px; color: #A8B8D8;")
        lbl_subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        lay_bienvenida.addStretch()
        lay_bienvenida.addWidget(lbl_titulo)
        lay_bienvenida.addWidget(lbl_subtitulo)
        lay_bienvenida.addStretch()
        
        self.app_dashboard = DemoDashboardFull()
        self.app_operaciones = MagnusApp()
        self.app_usuarios = ControladorUsuarios()
        
        # Cargar About (que no tiene controlador, es solo UI)
        self.vista_about = QMainWindow()
        self.ui_about = Ui_about()
        self.ui_about.setupUi(self.vista_about)
        
        # Añadir al StackedWidget
        self.id_vista_bienvenida = self.contenedor_vistas.addWidget(self.vista_bienvenida)
        self.id_vista_dash = self.contenedor_vistas.addWidget(self.app_dashboard)
        self.id_vista_operaciones = self.contenedor_vistas.addWidget(self.app_operaciones.ventana.centralWidget() if hasattr(self.app_operaciones.ventana, "centralWidget") else self.app_operaciones.ventana)
        self.id_vista_usuarios = self.contenedor_vistas.addWidget(self.app_usuarios.ventana.centralWidget() if hasattr(self.app_usuarios.ventana, "centralWidget") else self.app_usuarios.ventana)
        self.id_vista_about = self.contenedor_vistas.addWidget(self.vista_about.centralWidget() if hasattr(self.vista_about, "centralWidget") else self.vista_about)
        
        # Mostrar la Bienvenida por defecto
        self.contenedor_vistas.setCurrentIndex(self.id_vista_bienvenida)
        
        from PySide6.QtCore import QTimer
        self._is_maximized = False
        # Maximizar por defecto (esperamos a que se muestre para que tome su geometría base correctamente)
        QTimer.singleShot(10, self.toggle_maximize)
        
        # 4. Configurar el menú lateral
        self.ancho_menu_expandido = 200
        # Ahora el menú se reduce hasta mostrar solo el ícono (ej. 60px) en lugar de ocultarse por completo (0px).
        self.ancho_menu_contraido = 60 
        self.menu_lateral.setMaximumWidth(self.ancho_menu_contraido)
        
        # 5. CONECTAR LOS BOTONES DEL MENU LATERAL A LAS VISTAS
        if hasattr(self.ui, 'btn_inicio'):
            # Conectar el botón de inicio para alternar (abrir/cerrar) el menú
            self.ui.btn_inicio.clicked.connect(self.toggle_menu)
            
        if hasattr(self.ui, 'btn_analitica'):
            self.ui.btn_analitica.clicked.connect(lambda: self.cambiar_pantalla(self.id_vista_dash))
            
        if hasattr(self.ui, 'btn_procesar_datos'):
            self.ui.btn_procesar_datos.clicked.connect(lambda: self.cambiar_pantalla(self.id_vista_operaciones))
            
        if hasattr(self.ui, 'btn_credenciales'):
            self.ui.btn_credenciales.clicked.connect(lambda: self.cambiar_pantalla(self.id_vista_usuarios))
            
        if hasattr(self.ui, 'btn_acerca_de'):
            self.ui.btn_acerca_de.clicked.connect(lambda: self.cambiar_pantalla(self.id_vista_about))

        # Conectar botones
        if hasattr(self.ui, 'btn_salir'):
            self.ui.btn_salir.clicked.connect(self.close)
            
        if hasattr(self.ui, 'pushButton'):
            self.ui.pushButton.clicked.connect(self.close)
        if hasattr(self.ui, 'pushButton_2'):
            self.ui.pushButton_2.clicked.connect(self.toggle_maximize)
        if hasattr(self.ui, 'pushButton_3'):
            self.ui.pushButton_3.clicked.connect(self.showMinimized)

        # Configurar arrastre de ventana desde el header
        self._start_pos = None
        if hasattr(self.ui, 'header_frame'):
            self.ui.header_frame.mousePressEvent = self.header_mouse_press
            self.ui.header_frame.mouseMoveEvent = self.header_mouse_move
            self.ui.header_frame.mouseReleaseEvent = self.header_mouse_release

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'grip'):
            self.grip.move(self.width() - 20, self.height() - 20)
            self.grip.raise_()

    def cambiar_pantalla(self, id_pantalla):
        self.contenedor_vistas.setCurrentIndex(id_pantalla)

    def toggle_menu(self):
        # Comprobar el estado actual por su ancho máximo para mayor precisión
        max_width = self.menu_lateral.maximumWidth()
        
        # Si ya está expandido, lo contraemos; si está contraído, lo expandimos
        if max_width == self.ancho_menu_expandido:
            nuevo_ancho = self.ancho_menu_contraido
        else:
            nuevo_ancho = self.ancho_menu_expandido
            
        self.animacion = QPropertyAnimation(self.menu_lateral, b"maximumWidth")
        self.animacion.setDuration(300)
        self.animacion.setStartValue(max_width)
        self.animacion.setEndValue(nuevo_ancho)
        self.animacion.setEasingCurve(QEasingCurve.Type.InOutQuart)
        self.animacion.start()

    def toggle_maximize(self):
        if self._is_maximized:
            self.showNormal()
            self._is_maximized = False
            self.ui.centralwidget.setProperty("maximized", False)
            self.menu_lateral.setProperty("maximized", False)
        else:
            self.showMaximized()
            self._is_maximized = True
            self.ui.centralwidget.setProperty("maximized", True)
            self.menu_lateral.setProperty("maximized", True)
            
        # Refresca el CSS para quitar o poner bordes al maximizar
        self.ui.centralwidget.style().unpolish(self.ui.centralwidget)
        self.ui.centralwidget.style().polish(self.ui.centralwidget)
        self.menu_lateral.style().unpolish(self.menu_lateral)
        self.menu_lateral.style().polish(self.menu_lateral)

    def header_mouse_press(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._start_pos = event.globalPosition().toPoint()

    def header_mouse_move(self, event):
        if self._start_pos is not None:
            if self._is_maximized:
                self.toggle_maximize()
            delta = event.globalPosition().toPoint() - self._start_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self._start_pos = event.globalPosition().toPoint()

    def header_mouse_release(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._start_pos = None

    def mostrar_menu(self):
        # SOLUCIÓN HOVER: Ocultamos (o desactivamos) el gatillo para que no intercepte clics/hover en los botones
        self.gatillo_izquierdo.hide()
        
        self.animacion = QPropertyAnimation(self.menu_lateral, b"maximumWidth")
        self.animacion.setDuration(300)
        self.animacion.setStartValue(self.menu_lateral.width())
        self.animacion.setEndValue(self.ancho_menu_expandido)
        self.animacion.setEasingCurve(QEasingCurve.Type.InOutQuart)
        self.animacion.start()

    def ocultar_menu(self):
        self.animacion = QPropertyAnimation(self.menu_lateral, b"maximumWidth")
        self.animacion.setDuration(300)
        self.animacion.setStartValue(self.menu_lateral.width())
        self.animacion.setEndValue(self.ancho_menu_contraido)
        self.animacion.setEasingCurve(QEasingCurve.Type.InOutQuart)
        
        # SOLUCIÓN HOVER: Volvemos a mostrar el gatillo solo cuando el menú termina de ocultarse
        self.animacion.finished.connect(self.gatillo_izquierdo.show)
        self.animacion.start()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    import recursos.recursos_rc 
    recursos.recursos_rc.qInitResources()
    
    ventana = ContenedorPrincipal()
    ventana.show()
    
    sys.exit(app.exec())
