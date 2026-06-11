import sys
import os

# Añadir el directorio raíz al sys.path para que reconozca 'metodos' y 'recursos' al ejecutar desde VSCode
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import ctypes
import subprocess
import json
from datetime import datetime
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox, QTableWidgetItem
from PySide6.QtCore import Qt, QThread, Signal, QObject, QEvent
from PySide6.QtGui import QIcon, QColor


from metodos import metodo_01 
from metodos import metodo_02

from metodos.sap_conexion import obtener_perfil_activo
from recursos import recursos_rc
from vistas.notificacion_toast import NotificacionToast

# --- CONFIGURACIÓN DE IDENTIDAD DE LA APP (ICONO EN BARRA DE TAREAS) ---
try:
    myappid = 'crediopciones.magnus.bot.1.0'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except:
    pass

def resolver_ruta(ruta_relativa):
    """ Función blindada para cuando conviertas el bot a .exe con PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, ruta_relativa)

def actualizar_resumen_acumulado(stats, metodo, duracion_s=0.0, eventos=None):
    """
    Actualiza el archivo logs/resumen_acumulado.json con los resultados
    de la ejección actual. Se llama siempre, sin depender de 'Registro Detallado'.
    """
    ruta = os.path.join("logs", "resumen_acumulado.json")

    # Cargar existente o inicializar
    if os.path.exists(ruta):
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except:
            data = {}
    else:
        data = {}

    # Estructura base
    data.setdefault("total", {"exitosos": 0, "errores": 0, "omitidos": 0, "monto": 0.0})
    data.setdefault("por_metodo", {})
    data.setdefault("por_sociedad", {
        "GT03": {"exitosos": 0, "errores": 0, "omitidos": 0},
        "GT09": {"exitosos": 0, "errores": 0, "omitidos": 0}
    })
    data.setdefault("por_fecha", [])
    data.setdefault("errores_frecuentes", {})

    # Totales globales
    data["total"].setdefault("num_ejecuciones", 0)
    data["total"].setdefault("duracion_total_s", 0.0)
    data["total"]["exitosos"]       += stats.get("ok", 0)
    data["total"]["errores"]         += stats.get("errores", 0)
    data["total"]["omitidos"]        += stats.get("omitidos", 0)
    data["total"]["monto"]            = round(data["total"]["monto"] + stats.get("monto", 0.0), 2)
    data["total"]["num_ejecuciones"] += 1
    data["total"]["duracion_total_s"] = round(data["total"]["duracion_total_s"] + duracion_s, 1)

    # Por método
    mk = str(metodo)
    data["por_metodo"].setdefault(mk, {"ejecuciones": 0, "exitosos": 0, "errores": 0, "omitidos": 0, "monto": 0.0})
    data["por_metodo"][mk]["ejecuciones"] += 1
    data["por_metodo"][mk]["exitosos"]    += stats.get("ok", 0)
    data["por_metodo"][mk]["errores"]     += stats.get("errores", 0)
    data["por_metodo"][mk]["omitidos"]    += stats.get("omitidos", 0)
    data["por_metodo"][mk]["monto"]        = round(data["por_metodo"][mk]["monto"] + stats.get("monto", 0.0), 2)

    # Por fecha (tendencia) — agrega o suma al día de hoy
    hoy = datetime.now().strftime("%d.%m.%Y")
    entrada_hoy = next((e for e in data["por_fecha"] if e["fecha"] == hoy), None)
    if entrada_hoy:
        entrada_hoy["exitosos"]   += stats.get("ok", 0)
        entrada_hoy["errores"]    += stats.get("errores", 0)
        entrada_hoy["monto"]       = round(entrada_hoy["monto"] + stats.get("monto", 0.0), 2)
        entrada_hoy["duracion_s"]  = round(entrada_hoy.get("duracion_s", 0.0) + duracion_s, 1)
    else:
        data["por_fecha"].append({
            "fecha":       hoy,
            "exitosos":    stats.get("ok", 0),
            "errores":     stats.get("errores", 0),
            "monto":       round(stats.get("monto", 0.0), 2),
            "duracion_s":  round(duracion_s, 1)
        })
    data["por_fecha"] = data["por_fecha"][-30:]  # Mantener solo 30 días

    # Por sociedad y errores frecuentes (solo si hay eventos detallados)
    if eventos:
        for ev in eventos:
            soc = str(ev.get("sociedad", "")).strip().upper()
            tipo = ev.get("tipo", "")
            if soc in data["por_sociedad"]:
                if tipo == "EXITO":
                    data["por_sociedad"][soc]["exitosos"] += 1
                elif tipo == "ERROR":
                    data["por_sociedad"][soc]["errores"] += 1
                elif tipo == "ADVERTENCIA":
                    data["por_sociedad"][soc]["omitidos"] += 1

        for ev in eventos:
            if ev.get("tipo") == "ERROR":
                msg = str(ev.get("mensaje", ""))[:60]
                data["errores_frecuentes"][msg] = data["errores_frecuentes"].get(msg, 0) + 1

    data["ultima_actualizacion"] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    try:
        os.makedirs("logs", exist_ok=True)
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"[AVISO] No se pudo actualizar resumen_acumulado: {e}")

# =========================================================
# 1. EL HILO DE TRABAJO (Previene que la UI se congele)
# =========================================================

class HiloRPA(QThread):
    senal_log = Signal(str)
    # ACTUALIZADO: Ahora acepta 8 strings para coincidir con tus métodos
    senal_log_tabla = Signal(str, str, str, str, str, str, str, str) 
    senal_progreso = Signal(float)
    senal_fin = Signal(dict, bool) 

    def __init__(self, modulo, ruta_excel):
        super().__init__()
        self.modulo = modulo
        self.ruta_excel = ruta_excel
        self.stop_flag = False

    def run(self):
        try:
            silencioso = getattr(self, "silencioso", False)
            detallado = getattr(self, "detallado", False)
            
            self.modulo.ejecutar(
                self.ruta_excel, 
                self.emitir_log, 
                lambda: self.stop_flag,
                self.emitir_progreso,      
                self.emitir_fin,
                self.emitir_log_tabla,
                silencioso,
                detallado
            )
        except Exception as e:
            self.senal_log.emit(f"❌ Error crítico del hilo: {e}")
            self.senal_fin.emit({'ok':0, 'omitidos':0, 'errores':0, 'monto':0}, self.stop_flag)

    def emitir_log(self, mensaje):
        self.senal_log.emit(mensaje)
    
    # ACTUALIZADO: Se reciben los 8 parámetros y se emiten a la interfaz
    def emitir_log_tabla(self, hora, cliente, documento, estado, sociedad="", clase="", banco="", fecha=""):
        self.senal_log_tabla.emit(hora, cliente, documento, estado, sociedad, clase, banco, fecha)
        
    def emitir_progreso(self, valor):
        self.senal_progreso.emit(valor)
        
    def emitir_fin(self, stats):
        self.senal_fin.emit(stats, self.stop_flag)

    def detener(self):
        self.stop_flag = True

# =========================================================
# 2. HILO WATCHDOG (Monitoreo de red en paralelo)
# =========================================================

class HiloWatchdog(QThread):
    senal_red_caida    = Signal()
    senal_red_ok       = Signal()

    def __init__(self):
        super().__init__()
        self._activo = True
        self._estado_anterior = True  # Asumimos internet activo al inicio
        self._sap_caido_anterior = False  # Rastrear caidá de servidor SAP

    def run(self):
        from metodos.sap_conexion import hay_internet, hay_servidor_sap
        import os
        while self._activo:
            tiene_red = hay_internet(timeout=1)
            tiene_sap = hay_servidor_sap(timeout=2)
            
            # Caso 1: El servidor SAP se cayó (incluso con internet activo = WSAECONNRESET)
            sap_caido_ahora = not tiene_sap
            if sap_caido_ahora and not self._sap_caido_anterior:
                # MATAR SAP inmediatamente para limpiar el popup nativo bloqueante
                os.system("taskkill /F /IM saplogon.exe")
                if not self._estado_anterior:  # Solo emitir una vez si no ya fue caida de red
                    pass  # La señal de red caida ya fue emitida antes
                else:
                    self.senal_red_caida.emit()
            
            # Caso 2: Caída de internet general
            if not tiene_red and self._estado_anterior:
                self.senal_red_caida.emit()
            
            # Caso 3: Recuperación: tanto internet como servidor SAP están activos
            red_recuperada = tiene_red and tiene_sap
            estado_anterior_ok = self._estado_anterior and not self._sap_caido_anterior
            if red_recuperada and not estado_anterior_ok:
                os.system("taskkill /F /IM saplogon.exe")  # Limpiar zombie si quedara
                import time as _time; _time.sleep(2)
                self.senal_red_ok.emit()
            
            self._estado_anterior = tiene_red
            self._sap_caido_anterior = sap_caido_ahora
            self.msleep(1000)

    def detener(self):
        self._activo = False

# =========================================================
# 3. LA APLICACIÓN PRINCIPAL
# =========================================================
class MagnusApp(QObject):
    def __init__(self):
        super().__init__() 
        
        # --- CARGAR LA INTERFAZ VISUAL COMPILADA ---
        from PySide6.QtWidgets import QMainWindow
        from formularios.ui_operaciones import Ui_menu
        
        self.ventana = QMainWindow()
        self.ui = Ui_menu()
        self.ui.setupUi(self.ventana)
        
        # Bloquear el tamaño y maximizar
        self.ventana.setFixedSize(800, 650)
        
        self.ruta_excel = ""
        self.hilo_worker = None
        self.hilo_watchdog = None
        self.registro_json = None

        # Toast de Red (persistente, se reutiliza)
        self.toast = NotificacionToast()

        if not os.path.exists("logs"): 
            os.makedirs("logs")

        # --- CARGAR ÍCONO DE LA VENTANA (MAGNUS) ---
        self.ruta_icono = resolver_ruta(os.path.join("..", "recursos", "magnus.ico"))
        if os.path.exists(self.ruta_icono):
            self.ventana.setWindowIcon(QIcon(self.ruta_icono))

        # --- CONFIGURAR DRAG & DROP ESTRICTO ---
        # Apagamos las cajas de texto/tablas para que NO roben el Excel
        if hasattr(self.ui, "txt_ruta_archivo"):
            self.ui.txt_ruta_archivo.setAcceptDrops(False)
        if hasattr(self.ui, "tbl_archivo"):
            self.ui.tbl_archivo.setAcceptDrops(False)
        
        # Encendemos el DropZone y le asignamos el vigilante (eventFilter)
        self.ui.lbl_dropzone.setAcceptDrops(True)
        self.ui.lbl_dropzone.installEventFilter(self)
        
        # Configurar lbl_about
        if hasattr(self.ui, "lbl_about"):
            self.ui.lbl_about.installEventFilter(self)
            self.ui.lbl_about.setCursor(Qt.CursorShape.PointingHandCursor)

        # --- CONECTAR BOTONES ---
        self.ui.btn_select_excel.clicked.connect(self.seleccionar_archivo)
        self.ui.btn_iniciar.clicked.connect(self.iniciar_proceso)
        self.ui.btn_detener.clicked.connect(self.detener_proceso)
        self.ui.btn_limpiar.clicked.connect(self.limpiar_consola)

        # Estado inicial
        self.ui.btn_detener.setEnabled(False)

        # --- PAGINACIÓN ---
        self.datos_grid = []         # Lista de listas: [[sociedad, cliente, doc, clase, banco, fecha], ...]
        self.resultados_grid = {}    # Dict {indice_absoluto: (estado_texto, color_hex)}
        self.pagina_actual = 0
        self.filas_por_pagina = 50
        self.usuario_navego = False  # Flag para saber si el usuario cambió de página manualmente
        
        if hasattr(self.ui, 'btn_anterior'):
            self.ui.btn_anterior.clicked.connect(self._pagina_anterior)
        if hasattr(self.ui, 'btn_siguiente'):
            self.ui.btn_siguiente.clicked.connect(self._pagina_siguiente)
        if hasattr(self.ui, 'cmb_filas_por_pagina'):
            self.ui.cmb_filas_por_pagina.currentIndexChanged.connect(self._cambio_filas_pagina)
        self._actualizar_label_paginacion()

        # --- CONFIGURACIÓN DE TABLA VISUAL ---
        self.configurar_tabla()
        
        # --- BOTÓN CONECTAR A SAP (Flujo de UI) ---
        if hasattr(self.ui, "label_3"):
            self.ui.label_3.installEventFilter(self)
            self.ui.label_3.setCursor(Qt.CursorShape.PointingHandCursor)
            self.ui.label_3.setText("<html><head/><body><p align=\"left\">🔑 CONECTAR A SAP</p></body></html>")
            self.ui.label_3.setStyleSheet("color: grey;")
            self.ui.label_3.setToolTip("Haz clic aquí para iniciar sesión en SAP")

    def configurar_tabla(self):
        """Prepara las columnas y el tamaño de la tabla tbl_archivo"""
        if not hasattr(self.ui, "tbl_archivo"): return
        
        # Ajustar ancho de columnas dinámicamente según el contenido
        from PySide6.QtWidgets import QHeaderView, QAbstractItemView, QApplication
        from PySide6.QtGui import QFont, QKeySequence
        from PySide6.QtCore import Qt
        tabla = self.ui.tbl_archivo
        
        # Aplicar fuente 72
        fuente_tabla = QFont("72")
        tabla.setFont(fuente_tabla)
        
        # Propiedades de interacción: No editable, Selección por fila completa
        tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tabla.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        header = tabla.horizontalHeader()
        
        # Las primeras columnas se ajustan al texto que contienen
        for col in range(6):
            header.setSectionResizeMode(col, QHeaderView.ResizeToContents)
            
        # La última columna (Estado) toma todo el espacio sobrante
        header.setSectionResizeMode(6, QHeaderView.Stretch)
        
        # Ocultar números de fila laterales
        tabla.verticalHeader().setVisible(False)
        
        # Override de keyPressEvent para Ctrl+C con cabeceras
        def custom_keyPressEvent(event):
            if event.matches(QKeySequence.Copy):
                self._copiar_tabla_con_cabeceras(tabla)
            else:
                type(tabla).keyPressEvent(tabla, event)
        tabla.keyPressEvent = custom_keyPressEvent
        
    def _copiar_tabla_con_cabeceras(self, tabla):
        from PySide6.QtWidgets import QApplication
        seleccionados = tabla.selectedRanges()
        if not seleccionados: return
        
        headers = [tabla.horizontalHeaderItem(c).text() for c in range(tabla.columnCount()) if not tabla.isColumnHidden(c)]
        texto_copiar = "\t".join(headers) + "\n"
        
        filas = set()
        for rango in seleccionados:
            for row in range(rango.topRow(), rango.bottomRow() + 1):
                filas.add(row)
                
        for row in sorted(filas):
            fila_texto = []
            for col in range(tabla.columnCount()):
                if not tabla.isColumnHidden(col):
                    item = tabla.item(row, col)
                    fila_texto.append(item.text().replace('\n', ' ') if item else "")
            texto_copiar += "\t".join(fila_texto) + "\n"
            
        QApplication.clipboard().setText(texto_copiar)

        # Estilizar únicamente la barra de scroll (colores Magnus)
        # Se le aplica directamente a la barra para no afectar el resto de la tabla (header, bordes)
        from PySide6.QtWidgets import QScrollBar
        scroll_bar = QScrollBar(Qt.Vertical)
        scroll_bar.setStyleSheet("""
            QScrollBar:vertical {
                border: none;
                background: #1E1E1E;
                width: 5px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #1877F2;
                min-height: 10px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background: #1877F2;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        tabla.setVerticalScrollBar(scroll_bar)

    def agregar_log_tabla(self, hora, cliente, documento, estado, sociedad="", clase="", banco="", fecha=""):
        """Almacena el resultado en memoria y actualiza la celda visible si corresponde."""
        if not hasattr(self.ui, "tbl_archivo"): return
        
        indice_absoluto = getattr(self, 'fila_actual_progreso', 0)
        
        # 1. Determinar el color según el estado
        texto_estado = estado.lower()
        if any(p in texto_estado for p in ["ok", "éxito", "contabilizado", "creado", "documento de contabilización"]):
            color_hex = "#00CC6A"
        elif any(p in texto_estado for p in ["error", "fallo", "crítico"]):
            color_hex = "#f85149"
        elif any(p in texto_estado for p in ["omitido", "vacío", "insuficiente", "saldo negativo", "nota de crédito"]):
            color_hex = "#e3b341"
        else:
            color_hex = "#8b949e"

        # 2. Guardar resultado en memoria (fuente de verdad)
        self.resultados_grid[indice_absoluto] = (estado, color_hex)
        
        # 3. Actualizar datos de la fila en memoria (por si los valores cambiaron)
        if indice_absoluto < len(self.datos_grid):
            self.datos_grid[indice_absoluto] = [sociedad, cliente, documento, clase, banco, fecha]
        
        # 4. Si la fila está en la página visible, actualizar la celda directamente
        inicio_pagina = self.pagina_actual * self.filas_por_pagina
        fin_pagina = inicio_pagina + self.filas_por_pagina
        
        if inicio_pagina <= indice_absoluto < fin_pagina:
            fila_visual = indice_absoluto - inicio_pagina
            tabla = self.ui.tbl_archivo
            
            items_data = [sociedad, cliente, documento, clase, banco, fecha, estado]
            for col, txt in enumerate(items_data):
                item = QTableWidgetItem(txt)
                item.setTextAlignment(Qt.AlignCenter)
                if col == 6:  # Columna resultado
                    item.setForeground(QColor(color_hex))
                else:
                    item.setForeground(QColor("#8b949e"))
                tabla.setItem(fila_visual, col, item)
            tabla.scrollToItem(tabla.item(fila_visual, 6))
        
        # 5. Auto-navegar a la página del registro activo (solo si el usuario no navegó manualmente)
        if not self.usuario_navego and not (inicio_pagina <= indice_absoluto < fin_pagina):
            pagina_del_registro = indice_absoluto // self.filas_por_pagina
            self.pagina_actual = pagina_del_registro
            self._renderizar_pagina()
        
        # 6. Avanzar contador global
        self.fila_actual_progreso = indice_absoluto + 1
        color = QColor(color_hex)

        # 7. Auditar Datos Exactos de la Tabla en el JSON de Telemetría (Si está activo)
        if self.registro_json is not None:
            es_error = color == QColor("#f85149")
            es_exito = color == QColor("#00CC6A")
            es_advertencia = color == QColor("#e3b341")
            
            semaforo = "NEUTRAL"
            tipo_msg = "INFO"
            
            if es_exito:
                semaforo = "VERDE"
                tipo_msg = "EXITO"
            elif es_error:
                semaforo = "ROJO"
                tipo_msg = "ERROR"
            elif es_advertencia:
                semaforo = "AMARILLO"
                tipo_msg = "ADVERTENCIA"
                
            evento = {
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "tipo": tipo_msg,
                "semaforo": semaforo,
                "sociedad": sociedad,
                "cliente": cliente,
                "documento": documento,
                "clase_pago": clase,
                "banco": banco,
                "fecha_doc": fecha,
                "mensaje": texto_estado
            }
            self.registro_json["eventos_detallados"].append(evento)


    # --- LÓGICA DE DRAG & DROP Y CLICS ---
    def eventFilter(self, objeto, evento):
        # 1. Detectar clic en lbl_about
        if hasattr(self.ui, "lbl_about") and objeto == self.ui.lbl_about and evento.type() == QEvent.Type.MouseButtonRelease:
            self.mostrar_about()
            return True        
        
        # 1.5 Detectar clic en lbl_conectar_sap (label_3)
        if hasattr(self.ui, "label_3") and objeto == self.ui.label_3:
            if evento.type() == QEvent.Type.MouseButtonRelease:
                self.escribir_log("🔑 Abriendo conector SAP...")
                # Levantar el login.py en un subproceso aislado
                ruta_login = resolver_ruta("login.py")
                if os.path.exists("login.exe"):
                    subprocess.Popen(["login.exe"])
                elif os.path.exists(ruta_login):
                    subprocess.Popen(["python", ruta_login])
                return True

        # 2. Filtro estricto: Solo interactuamos si el evento ocurre sobre lbl_dropzone
        if objeto == self.ui.lbl_dropzone:
            if evento.type() == QEvent.Type.DragEnter:
                if evento.mimeData().hasUrls():
                    evento.accept()
                else:
                    evento.ignore()
                return True
            
            elif evento.type() == QEvent.Type.Drop:
                rutas = [url.toLocalFile() for url in evento.mimeData().urls()]
                if rutas:
                    archivo = rutas[0]
                    if archivo.endswith(('.xlsx', '.xls', '.csv')):
                        self.cargar_archivo(archivo)
                    else:
                        self.escribir_log("\u274c Error: Por favor arrastra un archivo Excel (.xlsx) o un Avance (.csv)")
                return True
                
        # Para todo lo demás, que el sistema siga su curso normal
        return super().eventFilter(objeto, evento)


    # --- LÓGICA DE ARCHIVOS ---
    def seleccionar_archivo(self):
        archivo, _ = QFileDialog.getOpenFileName(self.ventana, "Seleccionar Archivo", "", "Archivos de Datos (*.xlsx *.xls *.csv)")
        if archivo:
            self.cargar_archivo(archivo)

    def cargar_archivo(self, ruta):
        self.ruta_excel = ruta
        
        # Actualizar la caja de texto inferior
        self.ui.txt_ruta_archivo.setText(ruta)
        nombre_corto = os.path.basename(ruta)
        
        # --- AUTO-DETECCIÓN DE MÉTODO POR COLUMNAS MIENTRAS SE CARGA ---
        import pandas as pd
        self.metodo_auto_detectado = None
        df_completo = None
        try:
            if ruta.endswith('.csv'):
                # Usar un detector de separador robusto para CSV
                try: 
                    df_test = pd.read_csv(ruta, sep=';', encoding='utf-8-sig', dtype=str)
                    cols = df_test.columns.tolist()
                    if len(cols) == 1 and ',' in cols[0]:
                        df_test = pd.read_csv(ruta, sep=',', encoding='utf-8-sig', dtype=str)
                        cols = df_test.columns.tolist()
                except:
                    df_test = pd.read_csv(ruta, sep=',', encoding='utf-8-sig', dtype=str)
                    cols = df_test.columns.tolist()
                df_completo = df_test
            else:
                df_completo = pd.read_excel(ruta, dtype=str)
                cols = df_completo.columns.tolist()
                
            # Limpieza básica de NaNs en strings para la tabla
            df_completo = df_completo.fillna("")
                
            # Columnas clave del Metodo 1
            if 'txt_cab_doc' in cols and 'monto_total' in cols:
                self.metodo_auto_detectado = 1
                self.escribir_log("🔍 Método 1 detectado automáticamente.")
                self._precargar_grid_excel(df_completo, 1)
            # Columnas clave del Metodo 2
            elif 'monto_total' in cols and 'comentario' in cols:
                self.metodo_auto_detectado = 2
                self.escribir_log("🔍 Método 2 detectado automáticamente.")
                self._precargar_grid_excel(df_completo, 2)
            else:
                msg = "⚠️ El Archivo no cuadra con la estructura del Método 1 ni Método 2."
                self.escribir_log(msg)
                QMessageBox.warning(self.ventana, "Formato Incorrecto", msg)
                self.ruta_excel = ""
                self.ui.txt_ruta_archivo.setText("")
                if hasattr(self.ui, "tbl_archivo"):
                    self.ui.tbl_archivo.setRowCount(0)
                return
        except Exception as e:
            msg = f"\u26a0\ufe0f No se pudo auto-detectar el método. Verifique que no esté abierto en otra aplicación: {e}"
            self.escribir_log(msg)
            QMessageBox.critical(self.ventana, "Error de Lectura", msg)
            self.ruta_excel = ""
            self.ui.txt_ruta_archivo.setText("")
            return

        # 1. Armamos el nuevo HTML manteniendo el centrado y cambiando la imagen
        nuevo_html = f"""
        <html>
          <head/>
          <body>
            <p align="center">
             <span style=" font-size:32pt; font-weight:400;">⚡
              <span style=" font-size:9pt; font-weight:400; color:grey">
                  <br/>¡ Archivo cargado !
              </span>
            </p>
          </body>
        </html>
        """
        
        # 2. Se lo inyectamos al Dropzone
        self.ui.lbl_dropzone.setText(nuevo_html)
        
        self.escribir_log(f"📄 Archivo cargado: {nombre_corto}")

    def _precargar_grid_excel(self, df, metodo):
        """Lee el DataFrame completo a memoria y renderiza la primera página"""
        self.datos_grid = []
        self.resultados_grid = {}
        self.pagina_actual = 0
        self.usuario_navego = False
        
        for _, row in df.iterrows():
            if metodo == 1:
                fila = [
                    str(row.get('sociedad', '')),
                    str(row.get('id_cliente', '')).replace('.0', '').strip(),
                    str(row.get('no_doc', '')).replace('.0', '').strip(),
                    str(row.get('clase_pago', '')).replace('.0', '').strip(),
                    str(row.get('cuenta_banco', '')).replace('.0', '').strip(),
                    str(row.get('fecha_deposito', ''))
                ]
            else:
                fila = [
                    str(row.get('sociedad', '')),
                    str(row.get('id_cliente', '')).replace('.0', '').strip(),
                    str(row.get('no_boleta', '')).replace('.0', '').strip(),
                    str(row.get('clase_pago', '')).replace('.0', '').strip(),
                    str(row.get('cuenta_banco', '')).replace('.0', '').strip(),
                    str(row.get('fecha_documento', ''))
                ]
            self.datos_grid.append(fila)
        
        # Leer filas por página del combobox
        if hasattr(self.ui, 'cmb_filas_por_pagina'):
            try: self.filas_por_pagina = int(self.ui.cmb_filas_por_pagina.currentText())
            except: self.filas_por_pagina = 50
        
        self._renderizar_pagina()
    
    def _renderizar_pagina(self):
        """Dibuja en tbl_archivo únicamente las filas de la página actual"""
        if not hasattr(self.ui, 'tbl_archivo'): return
        tabla = self.ui.tbl_archivo
        
        total = len(self.datos_grid)
        inicio = self.pagina_actual * self.filas_por_pagina
        fin = min(inicio + self.filas_por_pagina, total)
        filas_visibles = fin - inicio
        
        tabla.setRowCount(filas_visibles)
        
        for i in range(filas_visibles):
            idx_absoluto = inicio + i
            datos_fila = self.datos_grid[idx_absoluto]
            
            # Columnas de datos (0-5)
            for col, txt in enumerate(datos_fila):
                item = QTableWidgetItem(txt)
                item.setTextAlignment(Qt.AlignCenter)
                item.setForeground(QColor('#8b949e'))
                tabla.setItem(i, col, item)
            
            # Columna resultado (6)
            if idx_absoluto in self.resultados_grid:
                estado_txt, color_hex = self.resultados_grid[idx_absoluto]
                item_res = QTableWidgetItem(estado_txt)
                item_res.setForeground(QColor(color_hex))
            else:
                item_res = QTableWidgetItem('')
                item_res.setForeground(QColor('#8b949e'))
            item_res.setTextAlignment(Qt.AlignCenter)
            tabla.setItem(i, 6, item_res)
        
        self._actualizar_label_paginacion()
    
    def _pagina_anterior(self):
        if self.pagina_actual > 0:
            self.pagina_actual -= 1
            self.usuario_navego = True
            self._renderizar_pagina()
    
    def _pagina_siguiente(self):
        total = len(self.datos_grid)
        total_paginas = max(1, (total + self.filas_por_pagina - 1) // self.filas_por_pagina)
        if self.pagina_actual < total_paginas - 1:
            self.pagina_actual += 1
            self.usuario_navego = True
            self._renderizar_pagina()
    
    def _cambio_filas_pagina(self):
        if hasattr(self.ui, 'cmb_filas_por_pagina'):
            try: self.filas_por_pagina = int(self.ui.cmb_filas_por_pagina.currentText())
            except: return
        self.pagina_actual = 0
        self.usuario_navego = False
        if self.datos_grid:
            self._renderizar_pagina()

    def _actualizar_label_paginacion(self):
        if not hasattr(self.ui, 'lbl_paginacion'): return
        total = len(self.datos_grid)
        if total == 0:
            self.ui.lbl_paginacion.setText('Mostrando 0 - 0 de 0')
            if hasattr(self.ui, 'btn_anterior'): self.ui.btn_anterior.setEnabled(False)
            if hasattr(self.ui, 'btn_siguiente'): self.ui.btn_siguiente.setEnabled(False)
            return
        
        inicio = self.pagina_actual * self.filas_por_pagina
        fin = min(inicio + self.filas_por_pagina, total)
        total_paginas = max(1, (total + self.filas_por_pagina - 1) // self.filas_por_pagina)
        
        self.ui.lbl_paginacion.setText(f'Mostrando {inicio + 1} - {fin} de {total}')
        if hasattr(self.ui, 'btn_anterior'): self.ui.btn_anterior.setEnabled(self.pagina_actual > 0)
        if hasattr(self.ui, 'btn_siguiente'): self.ui.btn_siguiente.setEnabled(self.pagina_actual < total_paginas - 1)


    # --- LÓGICA DE CONSOLA / AUDITORÍA JSON ---
    def escribir_log(self, mensaje):
        ts = datetime.now().strftime("%H:%M:%S")
        texto = f"[{ts}] {mensaje}"
        if hasattr(self.ui, "txt_consola"):
            self.ui.txt_consola.append(texto)
        
        # Guardar en memoria JSON si la auditoría está encendida
        if self.registro_json is not None:
            self.registro_json["eventos_detallados"].append({
                "timestamp": ts,
                "tipo": "SISTEMA",
                "semaforo": "NEUTRAL",
                "mensaje": mensaje
            })

    def limpiar_consola(self):
        if hasattr(self.ui, "txt_consola"):
            self.ui.txt_consola.clear()
        if hasattr(self.ui, "tbl_archivo"):
            self.ui.tbl_archivo.setRowCount(0)
        self.datos_grid = []
        self.resultados_grid = {}
        self.pagina_actual = 0
        self.usuario_navego = False
        self.ruta_excel = ""
        self.metodo_auto_detectado = None
        self.fila_actual_progreso = 0
        
        if hasattr(self.ui, "txt_ruta_archivo"):
            self.ui.txt_ruta_archivo.setText("")
            
        if hasattr(self.ui, "lbl_dropzone"):
            self.ui.lbl_dropzone.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:28pt;\">\U0001f4c1</span><br/><span style=\" font-size:9pt; color:#3A5080;\">\U000000a1 Arrastra y suelta un archivo Excel aqu\u00ed !</span></p></body></html>")
            
        self._actualizar_label_paginacion()
        
    # --- MOSTRAR ABOUT ---    
    def mostrar_about(self):
        # Evitar abrir múltiples ventanas si ya está abierta
        if hasattr(self, "ventana_about") and self.ventana_about.isVisible():
            self.ventana_about.activateWindow()
            return

        from PySide6.QtWidgets import QMainWindow
        from formularios.ui_about import Ui_about
        
        self.ventana_about = QMainWindow()
        self.ab_ui = Ui_about()
        self.ab_ui.setupUi(self.ventana_about)
        
        # Heredar el ícono de la aplicación principal
        if hasattr(self, "ruta_icono") and os.path.exists(self.ruta_icono):
            self.ventana_about.setWindowIcon(QIcon(self.ruta_icono))
            
        self.ventana_about.show()    

    # --- LÓGICA DEL PROCESO RPA ---
    def iniciar_proceso(self):
        if not self.ruta_excel:
            QMessageBox.warning(self.ventana, "Atención", "Debes seleccionar o arrastrar un archivo Excel primero.")
            return

        nombre_archivo = os.path.basename(self.ruta_excel).lower()
        modulo_seleccionado = None

        # Validación de Método autodetectado (La UI ya no tiene los RadioButtons)
        if getattr(self, "metodo_auto_detectado", None) == 1:
            modulo_seleccionado = metodo_01
            
        elif getattr(self, "metodo_auto_detectado", None) == 2:
            modulo_seleccionado = metodo_02
            
        else:
            QMessageBox.warning(self.ventana, "Atención", "El archivo Excel insertado no cuenta con el formato correcto del Método 1 o Método 2.")
            return
            
        # Opciones avanzadas (Los RadioButtons pasaron a ser CheckBoxes)
        modo_silencioso = self.ui.chk_mod_silencioso.isChecked() if hasattr(self.ui, 'chk_mod_silencioso') else False
        registro_detallado = self.ui.chk_reg_detallado.isChecked() if hasattr(self.ui, 'chk_reg_detallado') else False

        # Bloquear UI para evitar dobles clics
        self.ui.btn_iniciar.setEnabled(False)
        self.ui.btn_select_excel.setEnabled(False)
        self.ui.btn_detener.setEnabled(True)
        # Limpiar solo la consola (no la tabla precargada)
        if hasattr(self.ui, "txt_consola"):
            self.ui.txt_consola.clear()
        self.hora_inicio_proceso = datetime.now()  # Capturar hora de inicio para métricas de tiempo
        
        # Resetear progreso sin borrar los datos precargados del grid
        self.resultados_grid = {}
        self.pagina_actual = 0
        self.usuario_navego = False
        self.fila_actual_progreso = 0 # Iniciar contador de progreso para el Grid
        if self.datos_grid:
            self._renderizar_pagina()  # Redibujar primera página sin resultados
        if registro_detallado:
            # Intentar obtener el usuario de Windows o Sistema Operativo
            operador_sys = os.getlogin() if hasattr(os, 'getlogin') else 'desconocido'
            self.registro_json = {
                "ejecucion_info": {
                    "fecha": datetime.now().strftime("%d.%m.%Y"),
                    "hora_inicio": datetime.now().strftime("%H:%M:%S"),
                    "hora_fin": "",
                    "archivo_procesado": self.ruta_excel,
                    "metodo_detectado": getattr(self, "metodo_auto_detectado", 0),
                    "operador": operador_sys
                },
                "eventos_detallados": [],
                "resumen_final": {}
            }
        else:
            self.registro_json = None
            

        self.escribir_log(f"🚀 >>> INICIANDO PROCESO RPA (Silencioso={modo_silencioso}, Logs={registro_detallado}) <<<")

        # Iniciar el Hilo Seguro pasándole los flags
        self.hilo_worker = HiloRPA(modulo_seleccionado, self.ruta_excel)
        self.hilo_worker.silencioso = modo_silencioso
        self.hilo_worker.detallado = registro_detallado
        
        # Conectar "Cables" (Señales)
        self.hilo_worker.senal_log.connect(self.escribir_log)
        self.hilo_worker.senal_log_tabla.connect(self.agregar_log_tabla)
        self.hilo_worker.senal_fin.connect(self.proceso_terminado)
        
        self.hilo_worker.start()

        # --- INICIAR WATCHDOG DE RED ---
        self.hilo_watchdog = HiloWatchdog()
        self.hilo_watchdog.senal_red_caida.connect(self._on_red_caida)
        self.hilo_watchdog.senal_red_ok.connect(self._on_red_ok)
        self.hilo_watchdog.start()

    def detener_proceso(self):
        if self.hilo_worker and self.hilo_worker.isRunning():
            self.escribir_log("🛑 Deteniendo proceso de forma segura...")
            self.ui.btn_detener.setEnabled(False)
            self.hilo_worker.detener()
        if self.hilo_watchdog and self.hilo_watchdog.isRunning():
            self.hilo_watchdog.detener()
            self.hilo_watchdog.wait()
        self.toast.cerrar()

    def proceso_terminado(self, stats, fue_detenido):
        # Detener el watchdog cuando el proceso termina
        if self.hilo_watchdog and self.hilo_watchdog.isRunning():
            self.hilo_watchdog.detener()
            self.hilo_watchdog.wait()
        self.toast.cerrar()

        hora_fin = datetime.now().strftime("%H:%M:%S")
        if fue_detenido:
            self.escribir_log("--- PROCESO DETENIDO POR EL USUARIO ---")
        else:
            self.escribir_log("--- \u2705 PROCESO COMPLETADO ---")
            
        # 1. Actualizar resumen acumulado (siempre, sin depender de Registro Detallado)
        eventos = self.registro_json.get("eventos_detallados") if self.registro_json else None
        metodo  = getattr(self, "metodo_auto_detectado", 0) or 0
        # Calcular duración real de la ejecución
        duracion_s = (datetime.now() - getattr(self, "hora_inicio_proceso", datetime.now())).total_seconds()
        actualizar_resumen_acumulado(stats, metodo, duracion_s, eventos)

        # 2. Cerrar y Grabar el Archivo JSON de Telemetría (Si estaba activo)
        if self.registro_json is not None:
            self.registro_json["ejecucion_info"]["hora_fin"] = hora_fin
            self.registro_json["resumen_final"] = {
                "exitosos": stats.get("ok", 0),
                "errores": stats.get("errores", 0),
                "omitidos": stats.get("omitidos", 0),
                "monto_total_q": stats.get("monto", 0)
            }
            
            marca_tiempo = datetime.now().strftime("%d-%m-%Y_%H%M%S")
            ruta_out = os.path.join("logs", f"ejecucion_{marca_tiempo}.json")
            try:
                with open(ruta_out, 'w', encoding='utf-8') as f:
                    json.dump(self.registro_json, f, indent=4, ensure_ascii=False)
                self.escribir_log(f"\U0001f4c1 Telemetr\u00eda JSON guardada en: {ruta_out}")
            except Exception as e:
                self.escribir_log(f"\u274c Error guardando JSON: {e}")
            
        try:
            if not stats.get("abortado_red", False):
                self.mostrar_resumen(stats)
            else:
                self.escribir_log("--- PROCESO ABORTADO POR SIN CONEXIÓN A INTERNET ---")
        except Exception:
            # --- INICIO BLOQUE TELEMETRÍA (DATAVERSE & THREADING) ---
            try:
                with open('config/config.json', 'r', encoding='utf-8') as f:
                    config = json.load(f)

                config_remoto = config.get("remoto", {})

                try:
                    with open('version.txt', 'r', encoding='utf-8') as f:
                        version_actual = f.read().strip()
                except FileNotFoundError:
                    version_actual = "1.0.0"

                perfil = obtener_perfil_activo()
                operador = perfil["usuario_sap"] if perfil else "DESCONOCIDO"

                # Validar que config tiene URL de Dataverse
                if config_remoto.get("dataverse_url") and config_remoto.get("azure_client_secret") and "PEGA_AQUI" not in config_remoto.get("azure_client_secret"):
                    lista_tx = stats.get('transacciones_detalle', [])
                    
                    # LA MAGIA: Mover la inyección lenta a un hilo fantasma para que la UI no se congele NI UN MILISEGUNDO.
                    import threading
                    from metodos.api_telemetria import enviar_telemetria_dataverse
                    
                    # Función envoltorio para atrapar el resultado dentro del hilo
                    def hilo_dataverse(cfg, op, ver, st, txs, j_ctx):
                        exito, msj = enviar_telemetria_dataverse(cfg, op, ver, st, txs, j_ctx)
                        if not exito:
                            # Si algo falla en el fondo, escribimos al log (la señal de la UI podría estar muerta o ocupada, pero al menos lo intentamos)
                            print(f"[BACKGROUND THREAD] Error Dataverse: {msj}")
                            
                    hilo_inyector = threading.Thread(
                        target=hilo_dataverse, 
                        args=(config_remoto, operador, version_actual, stats, lista_tx, self.registro_json),
                        daemon=False # IMPORTANTE: daemon=False garantiza que Python no asesine este hilo mid-flight si el usuario cierra el programa de golpe.
                    )
                    hilo_inyector.start()
                    
                    self.escribir_log(f"✅ Lote enviado a Dataverse (HILO ASÍNCRONO INICIADO)")
                else:
                    self.escribir_log(f"⚠️ Telemetría apagada: Falta configuración Dataverse/Azure.")
                        
            except Exception as e:
                import traceback
                tb = traceback.format_exc()
                self.escribir_log(f"⚠️ Excepción crítica al preparar Dataverse: {e}")
                print(tb)
            # --- FIN BLOQUE TELEMETRÍA ---

        # Desbloquear UI
        self.ui.btn_iniciar.setEnabled(True)
        self.ui.btn_select_excel.setEnabled(True)
        self.ui.btn_detener.setEnabled(False)

    # --- NETWORK TOAST HANDLERS ---
    def _on_red_caida(self):
        """Llamado desde el Watchdog cuando detecta caída de red."""
        self.toast.mostrar("Sin conexión. Esperando que regrese la red...", icono="📵")

    def _on_red_ok(self):
        """Llamado desde el Watchdog cuando detecta que la red se recuperó."""
        import os, time as _time
        # Matar cualquier instancia zombie de SAP que se haya quedado colgada con popups nativos
        # Hacemos esto AHORA (al recuperar la red) para que el hilo RPA pueda relanzar limpiamente
        os.system("taskkill /F /IM saplogon.exe")
        _time.sleep(2)  # Dar 2 segundos a Windows para liberar el proceso
        self.toast.mostrar("✅ Conexión restaurada. Relanzando SAP...", icono="🌐")

    def mostrar_resumen(self, stats):
        from PySide6.QtWidgets import QMainWindow, QSizeGrip
        from formularios.ui_resumen import Ui_resumen

        if hasattr(self, "ventana_resumen") and self.ventana_resumen.isVisible():
            self.ventana_resumen.close()

        self.ventana_resumen = QMainWindow(self.ventana) # Padre para que sea modal correctamente
        self.ui_resumen = Ui_resumen()
        self.ui_resumen.setupUi(self.ventana_resumen)
        
        # Heredar el ícono de la aplicación principal
        if hasattr(self, "ruta_icono") and os.path.exists(self.ruta_icono):
            self.ventana_resumen.setWindowIcon(QIcon(self.ruta_icono))

        self.ventana_resumen.setWindowTitle("Resumen - Magnus")
        self.ventana_resumen.setMinimumSize(440, 400)
        
        # Configuración Frameless como en menu.ui
        self.ventana_resumen.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)
        self.ventana_resumen.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.ventana_resumen.setWindowModality(Qt.WindowModality.ApplicationModal) # Bloquea la principal hasta que se cierre

        # Asignar valores a los labels, conservando el estilo
        self.ui_resumen.lbl_procesados.setText(f'<html><head/><body><p align="right"><span style=" font-size:14pt; font-weight:700;">{stats.get("ok", 0)}</span></p></body></html>')
        self.ui_resumen.lbl_omitidos.setText(f'<html><head/><body><p align="right"><span style=" font-size:14pt; font-weight:700;">{stats.get("omitidos", 0)}</span></p></body></html>')
        self.ui_resumen.lbl_errores.setText(f'<html><head/><body><p align="right"><span style=" font-size:14pt; font-weight:700;">{stats.get("errores", 0)}</span></p></body></html>')
        
        # Formatear la moneda
        monto_str = f"Q. {stats.get('monto', 0):,.2f}"
        self.ui_resumen.lbl_monto_procesado.setText(f'<html><head/><body><p align="center"><span style=" font-size:20pt; font-weight:700;">{monto_str}</span></p></body></html>')

        # Vínculo del botón cerrar
        self.ui_resumen.btn_cerrar.clicked.connect(self.ventana_resumen.close)

        # Botones de la barra de título superior
        if hasattr(self.ui_resumen, 'pushButton'):
            self.ui_resumen.pushButton.clicked.connect(self.ventana_resumen.close)
            
        # Deshabilitar botones de maximizar y minimizar
        if hasattr(self.ui_resumen, 'pushButton_2'):
            self.ui_resumen.pushButton_2.hide()
        if hasattr(self.ui_resumen, 'pushButton_3'):
            self.ui_resumen.pushButton_3.hide()

        # Redimensionado deshabilitado para el modal resumen
        # if hasattr(self.ui_resumen, 'hl_footer'):
        #     self.grip_resumen = QSizeGrip(self.ventana_resumen)
        #     self.ui_resumen.hl_footer.addWidget(self.grip_resumen)

        # Dragging del encabezado
        self._start_pos_resumen = None
        
        def header_mouse_press(event):
            if event.button() == Qt.MouseButton.LeftButton:
                self._start_pos_resumen = event.globalPosition().toPoint()
        
        def header_mouse_move(event):
            if self._start_pos_resumen is not None:
                delta = event.globalPosition().toPoint() - self._start_pos_resumen
                self.ventana_resumen.move(self.ventana_resumen.x() + delta.x(), self.ventana_resumen.y() + delta.y())
                self._start_pos_resumen = event.globalPosition().toPoint()
                
        def header_mouse_release(event):
            if event.button() == Qt.MouseButton.LeftButton:
                self._start_pos_resumen = None

        if hasattr(self.ui_resumen, 'header_frame'):
            self.ui_resumen.header_frame.mousePressEvent = header_mouse_press
            self.ui_resumen.header_frame.mouseMoveEvent = header_mouse_move
            self.ui_resumen.header_frame.mouseReleaseEvent = header_mouse_release

        # Mostrar la ventana de resumen personalizada
        self.ventana_resumen.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Arrancar la aplicación
    mi_app = MagnusApp()
    mi_app.ventana.show()
    
    sys.exit(app.exec())