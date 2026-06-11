import os
import sys
import ctypes
from PySide6.QtWidgets import QApplication, QMessageBox, QMainWindow
from PySide6.QtCore import Qt, QThread, Signal

# --- IDENTIDAD DE PROCESO (ícono en barra de tareas de Windows) ---
# Debe llamarse ANTES de crear cualquier ventana
try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
        'crediopciones.magnus.bot.1.0'
    )
except Exception:
    pass

# --- CONFIGURACIÓN ---
APP_NAME = "Magnus_Core.exe" 

class HiloActualizacion(QThread):
    # Definimos las señales que enviarán datos a la interfaz gráfica
    actualizar_texto = Signal(str)
    actualizar_progreso = Signal(int)
    preguntar_actualizacion = Signal(str)
    mostrar_info = Signal(str, str)
    mostrar_error = Signal(str, str)
    finalizar_lanzamiento = Signal()
    cerrar_sistema = Signal()

    def __init__(self):
        super().__init__()
        self.respuesta_usuario = None
        self.esperando_respuesta = False

    def run(self):
        self.actualizar_texto.emit("Iniciando Magnus...")
        self.msleep(1000)
        self.finalizar_lanzamiento.emit()


class ControladorSplash:
    def __init__(self):
        from formularios.ui_splash import Ui_splash
        self.ventana = QMainWindow()
        self.ui = Ui_splash()
        self.ui.setupUi(self.ventana)
        
        # Quitar los bordes de Windows
        self.ventana.setWindowFlag(Qt.FramelessWindowHint)
        self.ventana.setAttribute(Qt.WA_TranslucentBackground)

        # Iniciar barra en "Modo Indeterminado" (cargando de lado a lado)
        if hasattr(self.ui, "progress_bar"):
            self.ui.progress_bar.setRange(0, 0)

        # Configurar y conectar el Hilo (Worker)
        self.worker = HiloActualizacion()
        self.worker.actualizar_texto.connect(self.set_texto_estado)
        self.worker.actualizar_progreso.connect(self.set_progreso)
        self.worker.preguntar_actualizacion.connect(self.mostrar_pregunta)
        self.worker.mostrar_info.connect(self.mostrar_alerta_info)
        self.worker.mostrar_error.connect(self.mostrar_alerta_error)
        self.worker.finalizar_lanzamiento.connect(self.lanzar_app)
        self.worker.cerrar_sistema.connect(self.ventana.close)

        self.worker.start()

    def mostrar(self):
        self.ventana.show()

    def set_texto_estado(self, texto):
        # Actualiza tu label lbl_validar_actualizacion
        if hasattr(self.ui, "lbl_validar_actualizaciones"):
            # Mantenemos el formato HTML para forzar el tamaño de 8pt y el texto centrado
            html_texto = f'<html><head/><body><p align="center"><span style=" font-size:8pt;">{texto}</span></p></body></html>'
            self.ui.lbl_validar_actualizaciones.setText(html_texto)

    def set_progreso(self, valor):
        if not hasattr(self.ui, "progress_bar"):
            return
            
        if valor == -1:
            # -1 es nuestra señal para detener el "modo indeterminado" infinito
            self.ui.progress_bar.setRange(0, 100)
            self.ui.progress_bar.setValue(0)
        else:
            self.ui.progress_bar.setValue(valor)

    def mostrar_pregunta(self, version_remota):
        respuesta = QMessageBox.question(
            self.ventana,
            "Actualización Disponible",
            f"Se encontró la versión {version_remota}.\n\n¿Deseas descargar las mejoras ahora?",
            QMessageBox.Yes | QMessageBox.No
        )
        # Devolver respuesta al hilo que está pausado
        self.worker.respuesta_usuario = (respuesta == QMessageBox.Yes)
        self.worker.esperando_respuesta = False

    def mostrar_alerta_info(self, titulo, mensaje):
        QMessageBox.information(self.ventana, titulo, mensaje)
        
    def mostrar_alerta_error(self, titulo, mensaje):
        QMessageBox.critical(self.ventana, titulo, mensaje)

    def lanzar_app(self):
        # Lanzar la app principal instanciando directamente su clase nativa en memoria (seguro para EXE)
        import vistas.main as app_principal
        
        # Guardamos referencia en controlador para que el GC no lo elimine
        self.ventana_principal = app_principal.ContenedorPrincipal()
        self.ventana_principal.show()
        
        # Cerrar el splash
        self.ventana.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controlador = ControladorSplash()
    controlador.mostrar()
    sys.exit(app.exec())