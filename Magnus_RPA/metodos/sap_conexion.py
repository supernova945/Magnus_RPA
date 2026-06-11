import time
import os
import subprocess
import json
import socket
import subprocess
import win32com.client
import winreg
import keyring

APP_NAME_KEYRING = "Magnus_RPA"

def obtener_perfil_activo():
    import sqlite3
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'perfiles.db')
    if not os.path.exists(db_path):
        return None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT alias, usuario_sap, es_productivo FROM perfiles WHERE es_activo = 1")
        perfil = cursor.fetchone()
        conn.close()
        if perfil:
            return {"alias": perfil[0], "usuario_sap": perfil[1], "es_productivo": bool(perfil[2])}
        return None
    except:
        return None

def hay_internet(host="8.8.8.8", port=53, timeout=3):
    """
    Verifica rápidamente si hay conexión hacia afuera para evitar que SAP se quede colgado.
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except OSError:
        return False

def hay_servidor_sap(timeout=3):
    """
    Verifica si el servidor de aplicaciones SAP está accesible.
    Lee el perfil activo para determinar si es PRD o QAS y
    selecciona el servidor correspondiente desde config/config.json.
    """
    try:
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        cfg_sap = data.get("sap", {})
        
        # Determinar envíronment según perfil activo
        perfil = obtener_perfil_activo()
        es_prd = perfil.get("es_productivo", False) if perfil else False
        
        clave_servidor = "servidor_prd" if es_prd else "servidor_qas"
        servidor = cfg_sap.get(clave_servidor, {})
        ip = servidor.get("ip", "172.31.100.180")
        puerto = int(servidor.get("puerto", 3210))
    except Exception:
        ip, puerto = "172.31.100.180", 3210  # Fallback a QAS por defecto
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        resultado = s.connect_ex((ip, puerto))
        s.close()
        return resultado == 0
    except OSError:
        return False


def obtener_config_sap():
    """
    Lee los nombres de conexión SAP desde config/config.json.
    Si no existe el archivo o alguna clave, usa los valores por defecto.
    """
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'config.json')
    defaults = {"conexion_prd": "PRODUCTIVO", "conexion_qas": "AMBIENTE QAS"}
    if not os.path.exists(config_path):
        return defaults
    try:
        import json
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        cfg_sap = data.get("sap", {})
        return {
            "conexion_prd": cfg_sap.get("conexion_prd", defaults["conexion_prd"]),
            "conexion_qas": cfg_sap.get("conexion_qas", defaults["conexion_qas"])
        }
    except Exception:
        return defaults

def _buscar_saplogon_dinamico():
    """Busca saplogon.exe usando el Registro de Windows o Rutas Comunes."""
    # Intento 1: Registro de Windows x64
    try:
        k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\SAP\SAP Shared")
        sap_dir, _ = winreg.QueryValueEx(k, "SAPGUI")
        ruta_posible = os.path.join(sap_dir, "saplogon.exe")
        if os.path.exists(ruta_posible): return ruta_posible
    except: pass
    
    # Intento 2: Registro Windows x86
    try:
        k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\SAP\SAP Shared")
        sap_dir, _ = winreg.QueryValueEx(k, "SAPGUI")
        ruta_posible = os.path.join(sap_dir, "saplogon.exe")
        if os.path.exists(ruta_posible): return ruta_posible
    except: pass

    # Intento 3: Rutas quemadas (Hardcoded)
    rutas_comunes = [
        r"C:\Program Files (x86)\SAP\FrontEnd\SAPGUI\saplogon.exe",
        r"C:\Program Files\SAP\FrontEnd\SAPGUI\saplogon.exe"
    ]
    for ruta in rutas_comunes:
        if os.path.exists(ruta): return ruta
        
    return None

def conectar_sap_autologin():
    """
    Intenta obtener la sesión activa de SAP. Si no existe, lanza SAP e intenta
    hacer Auto-Login usando las credenciales seguras de Windows (keyring).
    Valida la barra de estado para evitar bloqueos por clave incorrecta.
    """
    # 1. Intentar conectar a un SAP ya abierto
    try:
        SapGuiAuto = win32com.client.GetObject("SAPGUI")
        application = SapGuiAuto.GetScriptingEngine
        connection = application.Children(0) # Toma la primer conexión
        session = connection.Children(0)     # Toma la primer sesión
        return session
    except Exception:
        pass # SAP no está abierto o no hay sesión activa
        
    # 2. Si llegamos aquí, SAP está cerrado. Intentamos Auto-Login.
    perfil_activo = obtener_perfil_activo()
    if not perfil_activo:
        raise Exception("No hay ningún perfil marcado como 'Activo'. Abra 'Credenciales SAP' y active la estrella en su perfil.")
        
    usuario = perfil_activo["usuario_sap"]
    clave = keyring.get_password(APP_NAME_KEYRING, perfil_activo["alias"])
    
    if not clave:
        raise Exception(f"No se encontró la clave guardada para el perfil '{perfil_activo['alias']}'.")
        
    # Lanzar SAP
    ruta_saplogon = _buscar_saplogon_dinamico()
    if not ruta_saplogon:
        raise Exception("No se encontró el ejecutable 'saplogon.exe' en este equipo.")
        
    subprocess.Popen(ruta_saplogon)
    
    tiempo_maximo = 25
    SapGuiAuto = None
    for intento in range(tiempo_maximo):
        try:
            time.sleep(0.5)
            # Volver a instanciar GetObject
            SapGuiAuto = win32com.client.GetObject("SAPGUI")
            break 
        except Exception:
            pass
    
    if not SapGuiAuto:
        raise Exception("Se agotó el tiempo esperando a SAP Logon.")

    application = SapGuiAuto.GetScriptingEngine
    
    # Leer los nombres de conexión desde config/config.json (no hardcodeados)
    cfg = obtener_config_sap()
    nombre_conexion = cfg["conexion_prd"] if perfil_activo["es_productivo"] else cfg["conexion_qas"]
    
    # Abre conexión
    connection = application.OpenConnection(nombre_conexion, True)
    session = connection.Children(0)
    
    # Inyectar las credenciales
    session.findById("wnd[0]/usr/txtRSYST-BNAME").text = usuario
    session.findById("wnd[0]/usr/pwdRSYST-BCODE").text = clave
    session.findById("wnd[0]").sendVKey(0) # ENTER para login
    
    # Manejo de Popups Post-Login (Sistema, Licencia)
    # Darle hasta 4 segundos a SAP para que cargue la pantalla principal o arroje popups
    for _ in range(8):
        if session.Children.Count > 1: break
        time.sleep(0.5)
    
    # 1. Resolver Popups Inteligente: Primero verificar si es Múltiple Logon
    if session.Children.Count > 1:
        try:
            # Si existe la opción de logon múltiple, seleccionarla ANTES de enviar ENTER
            es_multi = False
            try: 
                session.findById("wnd[1]/usr/radMULTI_LOGON_OPT1").selected = True
                es_multi = True
            except: 
                try: 
                    session.findById("wnd[1]/usr/radMULTI_LOGON_OPT2").selected = True
                    es_multi = True
                except: 
                    pass
            
            # Enviar Enter nativo
            session.findById("wnd[1]").sendVKey(0)
            time.sleep(0.5)
        except:
            pass

    # Darle a SAP la chance de que levante un segundo popup (ej: Sistema -> Licencia)
    for _ in range(4):
        if session.Children.Count > 1: break
        time.sleep(0.5)

    # 2. Intentar cerrar el segundo si aparece
    if session.Children.Count > 1:
        try:
            # Reintentar la misma lógica por si el orden fue al revés
            try: session.findById("wnd[1]/usr/radMULTI_LOGON_OPT1").selected = True
            except: 
                try: session.findById("wnd[1]/usr/radMULTI_LOGON_OPT2").selected = True
                except: pass
            
            # Aceptar popup
            session.findById("wnd[1]").sendVKey(0)
            time.sleep(0.5)
        except:
            pass
    
    # IMPORTANTE: Para evitar que se bloquee el usuario al tercer intento

    # Usamos time.sleep largo en caso de que SAP tarde en mostrar el error
    time.sleep(1.5)
    try:
        sbar = session.findById("wnd[0]/sbar/pane[0]", False) # False evita excepción si no existe
        if sbar:
            texto_error = getattr(sbar, "text", "")
            if "Nombre o clave de acceso incorrectos" in texto_error:
                # Cerramos la conexión para no acumular intentos fallidos
                connection.CloseConnection()
                raise Exception(f"Login fallido: {texto_error}\nRevise sus credenciales en el menú.")
    except Exception as e:
        if "Login fallido" in str(e):
            raise e # Relanzar nuestro propio error
        pass # Si hubo otro error consultando la barra, continuamos por las dudas
            
    # Si todo salió bien, devolvemos la sesión
    return session

def esperar_elemento(session, id_elemento, timeout=5, tiempo_espera=0.2):
    """
    Smart Polling: Espera a que un elemento exista en SAP en lugar de 
    usar time.sleep fijo. Devuelve True si aparece, False si no (timeout).
    """
    tiempo_transcurrido = 0
    while tiempo_transcurrido < timeout:
        try:
            elm = session.findById(id_elemento, False)
            if elm:
                return True
        except:
            pass
        time.sleep(tiempo_espera)
        tiempo_transcurrido += tiempo_espera
    return False

def sap_str_to_float(valor_str):
    """
    Convierte montos numéricos que provienen de SAP a float nativo en Python.
    Soporta negativos al final (ej. 100-) y separadores variables de miles.
    """
    if not valor_str: return 0.0
    valor_str = str(valor_str).strip()
    signo = -1 if valor_str.endswith("-") else 1
    v = valor_str.replace("-", "")
    
    # Caso 1.200,50
    if "." in v and "," in v:
        if v.rfind(".") < v.rfind(","):
            v = v.replace(".", "")
            v = v.replace(",", ".")
        else:
            v = v.replace(",", "")
    elif "," in v:
        partes = v.split(",")
        if len(partes) == 2 and len(partes[1]) in (1, 2):
            v = v.replace(",", ".")
        else:
            v = v.replace(",", "")
    elif "." in v:
        partes = v.split(".")
        if len(partes) > 2 or (len(partes) == 2 and len(partes[1]) == 3):
            v = v.replace(".", "")
            
    try:
        return float(v) * signo
    except Exception:
        return 0.0

def log_matriz_sap(session, grid_id, print_log, docs_seleccionados=None):
    """
    Lee todas las filas del grid de SAP y las imprime en formato tabla en el log.
    Identifica visualmente las filas que están marcadas para pago.
    """
    try:
        if docs_seleccionados is None: docs_seleccionados = []
        # Limpiar documentos seleccionados de ceros a la izquierda para comparación
        docs_seleccionados_clean = [str(d).lstrip("0") for d in docs_seleccionados]
        
        grid = session.findById(grid_id)
        rows = grid.RowCount
        if rows <= 0:
            print_log("   [INFO] El grid de SAP está vacío.")
            return

        print_log("   " + "="*75)
        print_log("   [MATRIZ SAP] Visualización de Partidas en Cuenta:")
        print_log("   " + "-"*75)
        header = f"   {'FILA':<6} | {'DOCUMENTO':<12} | {'MONTO':<12} | {'REF/TEXTO':<20} | {'ESTADO'}"
        print_log(header)
        print_log("   " + "-"*75)

        for r in range(rows):
            try:
                doc = str(grid.GetCellValue(r, "BELNR")).strip()
                doc_clean = doc.lstrip("0")
                monto = str(grid.GetCellValue(r, "DMBTR")).strip()
                # Dependiendo de la transacción, la referencia puede estar en XBLNR o SGTXT
                ref = str(grid.GetCellValue(r, "XBLNR")).strip()
                if not ref or ref == "nan":
                    ref = str(grid.GetCellValue(r, "SGTXT")).strip()
                
                marcado = "✅ SELECCIONADO" if doc_clean in docs_seleccionados_clean else "⬜ Ignorado"
                
                fila_msg = f"   {r:<6} | {doc:<12} | {monto:<12} | {ref[:20]:<20} | {marcado}"
                print_log(fila_msg)
            except:
                pass
        
        print_log("   " + "="*75)
    except Exception as e:
        print_log(f"   [AVISO] No se pudo generar la matriz visual de SAP: {e}")

def abrir_caja_sap(session, dato_sociedad, print_log=lambda x: None):
    """
    Inicia la transacción /n/DBM/CASHDESK y maneja de forma explícita 
    el popup de Selección de Sociedad y el de Apertura/Cierre de caja.
    """
    try:
        session.findById("wnd[0]/tbar[0]/okcd").text = "/n/DBM/CASHDESK"
        session.findById("wnd[0]").sendVKey(0)
    except Exception as e:
        raise Exception(f"No se pudo iniciar la transacción /n/DBM/CASHDESK. Error: {e}")

    time.sleep(1)

    # MANEJO DINÁMICO DE PANTALLAS (Hasta 5 pantallas consecutivas)
    for _ in range(5):
        if session.Children.Count > 1:
            popup_procesado = False
            
            # A) Popup "Contabilizar de nuevo" (Partidas erróneas)
            try:
                if session.findById("wnd[1]/usr/subSUBSCREEN:SAPLSPO1:0502", False):
                    session.findById("wnd[1]/usr/btnBUTTON_2").press() # NO
                    popup_procesado = True
            except: pass

            # B) Popup "Sociedad"
            if not popup_procesado:
                try:
                    radio_id = "wnd[1]/usr/subSUBSCREEN_STEPLOOP:SAPLSPO5:0150/sub:SAPLSPO5:0150/radSPOPLI-SELFLAG[0,0]"
                    if session.findById(radio_id, False):
                        if "GT03" in dato_sociedad:
                            session.findById(radio_id).selected = True
                        elif "GT09" in dato_sociedad:
                            session.findById("wnd[1]/usr/subSUBSCREEN_STEPLOOP:SAPLSPO5:0150/sub:SAPLSPO5:0150/radSPOPLI-SELFLAG[1,0]").selected = True
                        session.findById("wnd[1]/tbar[0]/btn[0]").press()
                        popup_procesado = True
                except: pass

            # C) Popup "Apertura/Cierre" o cualquier otro genérico bloqueante
            if not popup_procesado:
                try: session.findById("wnd[0]/tbar[0]/btn[0]").press()
                except: 
                    try: session.findById("wnd[0]").sendVKey(0)
                    except: pass
            
            time.sleep(0.8)
        else:
            # No hay popups. Verificamos si estamos en la pantalla principal listos para operar.
            pantalla_lista = False
            try:
                if session.findById("wnd[0]/tbar[1]/btn[7]", False):
                    session.findById("wnd[0]/tbar[1]/btn[7]").press()
                    pantalla_lista = True
            except: pass
            
            if pantalla_lista:
                break # Ya estamos en la caja listos
            else:
                # Pantalla intermedia de pantalla completa (wnd[0])
                try: session.findById("wnd[0]/tbar[0]/btn[0]").press()
                except: 
                    try: session.findById("wnd[0]").sendVKey(0)
                    except: pass
                time.sleep(0.8)


# ===========================================================
# DIAGNÓSTICO INDEPENDIENTE — Ejecutar este archivo directamente
# para verificar perfil, credenciales y conexión SAP.
# ===========================================================
if __name__ == "__main__":
    import sys
    # Asegurar que el directorio raíz del proyecto esté en el path
    # cuando se ejecuta este archivo directamente desde VS Code
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    print("=" * 55)
    print("  DIAGNÓSTICO: sap_conexion.py")
    print("=" * 55)

    # PASO 1 — Verificar base de datos de perfiles
    print("\n[PASO 1] Buscando perfil activo en la base de datos...")
    perfil = obtener_perfil_activo()
    if not perfil:
        print("  ❌ ERROR: No se encontró ningún perfil marcado como activo en perfiles.db")
        print("     -> Abre la sección 'Credenciales SAP' en Magnus y verifica que")
        print("        un perfil tenga la estrella (⭐) marcada.")
        sys.exit(1)

    entorno = "PRODUCTIVO (PRD)" if perfil["es_productivo"] else "CALIDAD (QAS)"
    print(f"  ✅ Perfil encontrado:")
    print(f"     Alias       : {perfil['alias']}")
    print(f"     Usuario SAP : {perfil['usuario_sap']}")
    print(f"     Entorno     : {entorno}")

    # PASO 2 — Verificar clave en el Llavero de Windows
    print(f"\n[PASO 2] Buscando clave en Keyring para alias '{perfil['alias']}'...")
    clave = keyring.get_password(APP_NAME_KEYRING, perfil["alias"])
    if not clave:
        print(f"  ❌ ERROR: No se encontró la clave para el alias '{perfil['alias']}' en el Llavero de Windows.")
        print("     -> Intenta guardar el perfil nuevamente desde la interfaz.")
        sys.exit(1)
    print(f"  ✅ Clave recuperada correctamente (longitud: {len(clave)} caracteres).")

    # PASO 3 — Intentar conexión SAP
    nombre_conexion = "PRODUCTIVO" if perfil["es_productivo"] else "QAS"
    print(f"\n[PASO 3] Intentando conectar a SAP (Conexión: '{nombre_conexion}')...")
    print("         Asegúrate de que SAP Logon esté cerrado para probar el auto-login completo.")
    print("         O déjalo abierto para probar la reconexión a sesión activa.")
    try:
        session = conectar_sap_autologin()
        sap_user = "N/A"
        try:
            sap_user = session.Info.User
        except:
            pass
        print(f"\n  ✅ CONEXIÓN EXITOSA")
        print(f"     Usuario SAP activo en sesión: {sap_user}")
    except Exception as e:
        print(f"\n  ❌ ERROR DE CONEXIÓN:")
        print(f"     {e}")

    print("\n" + "=" * 55)
