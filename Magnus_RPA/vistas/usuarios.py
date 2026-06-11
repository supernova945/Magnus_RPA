import os
import sys
import sqlite3
import keyring

# Añadir el directorio raíz al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMessageBox, QLineEdit, QMainWindow, QTableWidgetItem
from formularios.ui_usuarios import Ui_credenciales

APP_NAME_KEYRING = "Magnus_RPA"
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'perfiles.db')

class ControladorUsuarios:
    def __init__(self):
        # 1. Cargar la interfaz desde el archivo compilado
        self.ventana = QMainWindow()
        self.ui = Ui_credenciales()
        self.ui.setupUi(self.ventana)
        
        # Bloquear el tamaño y maximizar
        self.ventana.setFixedSize(self.ventana.size())
        
        # 2. Configurar el campo de contraseña de SAP
        self.ui.txt_clave_sap.setEchoMode(QLineEdit.EchoMode.Password)
        
        # 3. Iniciar BD
        self.init_db()
        
        # 4. Conectar los botones
        self.ui.btn_nuevo_perfil.clicked.connect(self.nuevo_perfil)
        self.ui.btn_guardar.clicked.connect(self.guardar_perfil)
        self.ui.btn_eliminar_perfil.clicked.connect(self.eliminar_perfil)
        
        # 5. Conectar eventos de la tabla
        self.ui.tbl_usuarios.itemSelectionChanged.connect(self.seleccionar_perfil)
        
        # 6. Cargar los perfiles existentes
        self.cargar_tabla()
        self.cargar_tabla()

    def init_db(self):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS perfiles (
                alias TEXT PRIMARY KEY,
                usuario_sap TEXT,
                es_productivo BOOLEAN,
                es_activo BOOLEAN
            )
        ''')
        conn.commit()
        conn.close()

    def mostrar(self):
        self.ventana.show()

    def nuevo_perfil(self):
        # Limpia los campos para preparar un nuevo registro
        self.ui.txt_usuario.clear()
        self.ui.txt_clave.clear()
        self.ui.txt_clave_sap.clear()
        self.ui.radio_prd.setChecked(False)
        self.ui.radio_qas.setChecked(False)
        self.ui.chx_activo.setChecked(False)
        self.ui.txt_usuario.setFocus()
        self.ui.tbl_usuarios.clearSelection()

    def cargar_tabla(self):
        self.ui.tbl_usuarios.setRowCount(0)
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT alias, usuario_sap, es_productivo, es_activo FROM perfiles")
        perfiles = cursor.fetchall()
        conn.close()
        
        self.ui.lbl_conteo.setText(str(len(perfiles)))
        
        for idx, row in enumerate(perfiles):
            self.ui.tbl_usuarios.insertRow(idx)
            
            alias_item = QTableWidgetItem(row[0])
            alias_item.setFlags(alias_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.ui.tbl_usuarios.setItem(idx, 0, alias_item)
            
            user_item = QTableWidgetItem(row[1])
            user_item.setFlags(user_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.ui.tbl_usuarios.setItem(idx, 1, user_item)
            
            env_str = "PRD" if row[2] else "QAS"
            env_item = QTableWidgetItem(env_str)
            env_item.setFlags(env_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            env_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ui.tbl_usuarios.setItem(idx, 2, env_item)
            
            act_str = "⭐" if row[3] else ""
            act_item = QTableWidgetItem(act_str)
            act_item.setFlags(act_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            act_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ui.tbl_usuarios.setItem(idx, 3, act_item)

    def seleccionar_perfil(self):
        items = self.ui.tbl_usuarios.selectedItems()
        if not items:
            return
            
        # Extraemos el alias de la primera columna
        row = items[0].row()
        alias = self.ui.tbl_usuarios.item(row, 0).text()
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT usuario_sap, es_productivo, es_activo FROM perfiles WHERE alias=?", (alias,))
        perfil = cursor.fetchone()
        conn.close()
        
        if perfil:
            self.ui.txt_usuario.setText(alias)
            self.ui.txt_clave.setText(perfil[0])
            
            if perfil[1]:
                self.ui.radio_prd.setChecked(True)
            else:
                self.ui.radio_qas.setChecked(True)
                
            self.ui.chx_activo.setChecked(bool(perfil[2]))
            
            # Extraer la clave altamente encriptada desde Keyring local
            try:
                clave_guardada = keyring.get_password(APP_NAME_KEYRING, alias)
                if clave_guardada:
                    self.ui.txt_clave_sap.setText(clave_guardada)
                else:
                    self.ui.txt_clave_sap.clear()
            except Exception:
                self.ui.txt_clave_sap.clear()

    def guardar_perfil(self):
        alias = self.ui.txt_usuario.text().strip()
        usuario_sap = self.ui.txt_clave.text().strip()
        clave_sap = self.ui.txt_clave_sap.text().strip()
        
        es_prd = self.ui.radio_prd.isChecked()
        es_activo = self.ui.chx_activo.isChecked()
        
        if not alias or not usuario_sap or not clave_sap:
            QMessageBox.warning(self.ventana, "Error", "Debe completar Alias, Usuario SAP y Clave SAP.")
            return
            
        if not self.ui.radio_prd.isChecked() and not self.ui.radio_qas.isChecked():
            QMessageBox.warning(self.ventana, "Error", "Debe seleccionar el entorno (PRD o QAS).")
            return
            
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Si se le asigna activo para ejecucion automatica, quitamos el trono a los demas.
        if es_activo:
            cursor.execute("UPDATE perfiles SET es_activo = 0")
            
        cursor.execute('''
            INSERT OR REPLACE INTO perfiles (alias, usuario_sap, es_productivo, es_activo)
            VALUES (?, ?, ?, ?)
        ''', (alias, usuario_sap, es_prd, es_activo))
        
        conn.commit()
        conn.close()
        
        # Guardar en Windows Credential Manager LSA
        try:
            keyring.set_password(APP_NAME_KEYRING, alias, clave_sap)
            QMessageBox.information(self.ventana, "Éxito", f"Perfil '{alias}' enlazado y asegurado completamente.")
            self.cargar_tabla()
            
            # Dejamos remarcado el mismo perfil luego de guardar
            for row in range(self.ui.tbl_usuarios.rowCount()):
                if self.ui.tbl_usuarios.item(row, 0).text() == alias:
                    self.ui.tbl_usuarios.selectRow(row)
                    break
        except Exception as e:
            QMessageBox.critical(self.ventana, "Error de Seguridad", f"No se pudo guardar la contraseña localmente:\n{e}")

    def eliminar_perfil(self):
        alias = self.ui.txt_usuario.text().strip()
        if not alias:
            QMessageBox.warning(self.ventana, "Cuidado", "Seleccione un perfil primero antes de eliminarlo.")
            return
            
        resp = QMessageBox.question(self.ventana, "Confirmar", f"¿Desea destruir permanentemente el acceso del perfil '{alias}'?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if resp == QMessageBox.StandardButton.Yes:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM perfiles WHERE alias=?", (alias,))
            conn.commit()
            conn.close()
            
            try:
                keyring.delete_password(APP_NAME_KEYRING, alias)
            except Exception:
                pass
                
            self.nuevo_perfil()
            self.cargar_tabla()
            QMessageBox.information(self.ventana, "Eliminado", "Perfil purgado del archivo y llavero local.")

# Bloque de ejecución principal para pruebas
if __name__ == "__main__":
    app = QApplication(sys.argv)
    controlador = ControladorUsuarios()
    controlador.mostrar()
    sys.exit(app.exec())