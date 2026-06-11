"""
NotificacionToast — Controlador del formulario de notificaciones de red.
Aparece en la esquina superior derecha sin robar el foco ni minimizar ventanas activas.
Se cierra automáticamente tras 5 segundos o al presionar ✕.
"""
import os
import sys
from datetime import datetime

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QGuiApplication

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from formularios.ui_notificacion_toast import Ui_notificacion_toast


# Margen desde el borde de la pantalla (px)
_MARGEN_DERECHO = 20
_MARGEN_SUPERIOR = 40
# Duración fija de auto-cierre (ms)
_DURACION_MS = 10000


class NotificacionToast(QWidget):
    """
    Widget Toast que se posiciona en la esquina superior derecha de la pantalla.
    Permanece sobre todas las ventanas sin robar el foco ni minimizarlas.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_notificacion_toast()
        self.ui.setupUi(self)

        # Asegurar flags: sin borde, siempre encima, tipo Tool (no aparece en taskbar)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        # SIN WA_TranslucentBackground — el fondo es sólido (#000000) y no requiere transparencia del SO

        # Timer para el auto-cierre
        self._timer = QTimer(self)
        self._timer.setInterval(50)   # actualiza la barra cada 50ms
        self._elapsed = 0
        self._timer.timeout.connect(self._tick)

        # Conectar botón cerrar
        self.ui.btn_cerrar.clicked.connect(self.cerrar)

        # Inicializar barra en 100 %
        self.ui.progress_bar.setValue(100)

        # Referencia a una posible instancia anterior (singleton suave)
        self._oculto = False

    # ------------------------------------------------------------------
    # API PÚBLICA
    # ------------------------------------------------------------------

    def mostrar(self, mensaje: str, icono: str = "⚠️"):
        """
        Muestra el toast en la esquina superior derecha con el mensaje indicado.
        Reinicia el contador si ya estaba visible.
        """
        # Actualizar contenido
        self.ui.lbl_mensaje.setText(mensaje)
        self.ui.lbl_icon.setText(icono)
        self.ui.lbl_timestamp.setText(datetime.now().strftime("%H:%M:%S"))

        # Reiniciar barra y timer
        self._elapsed = 0
        self.ui.progress_bar.setValue(100)
        self._timer.stop()

        # Posicionar antes de mostrar
        self._posicionar()
        self.show()
        self.raise_()
        self._timer.start()

    def cerrar(self):
        """Cierra el toast inmediatamente con una pequeña animación de opacidad."""
        self._timer.stop()
        self._animar_cierre()

    # ------------------------------------------------------------------
    # INTERNO
    # ------------------------------------------------------------------

    def _posicionar(self):
        """Calcula la posición top-right respecto a la pantalla activa."""
        screen = QGuiApplication.primaryScreen().availableGeometry()
        x = screen.right() - self.width() - _MARGEN_DERECHO
        y = screen.top() + _MARGEN_SUPERIOR
        self.move(x, y)

    def _tick(self):
        """Actualiza la barra de progreso y cierra al llegar a 0."""
        self._elapsed += 50
        progreso = max(0, 100 - int((self._elapsed / _DURACION_MS) * 100))
        self.ui.progress_bar.setValue(progreso)
        if self._elapsed >= _DURACION_MS:
            self.cerrar()

    def _animar_cierre(self):
        """Desvanece el toast antes de ocultarlo."""
        anim = QPropertyAnimation(self, b"windowOpacity", self)
        anim.setDuration(250)
        anim.setStartValue(1.0)
        anim.setEndValue(0.0)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.finished.connect(self._on_cierre_terminado)
        anim.start()
        self._anim = anim  # evitar garbage collection

    def _on_cierre_terminado(self):
        self.hide()
        self.setWindowOpacity(1.0)  # restaurar para la próxima vez
