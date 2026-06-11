import sys
from metodos.sap_conexion import conectar_sap_autologin, esperar_elemento, sap_str_to_float, abrir_caja_sap, log_matriz_sap, hay_internet
import pandas as pd
import time
from datetime import datetime
import winreg
from mod_cierre import ejecutar_cierre

# --- FUNCIONES AUXILIARES ---
def obtener_separador_sistema():
    try:
        llave = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\International")
        separador, _ = winreg.QueryValueEx(llave, "sList")
        winreg.CloseKey(llave)
        return separador
    except Exception:
        return ";"

def limpiar_fecha(valor):
    valor_str = str(valor).strip()
    if isinstance(valor, (pd.Timestamp, datetime)):
        return valor.strftime("%d.%m.%Y")
    if " " in valor_str:
        valor_str = valor_str.split(" ")[0]
    return valor_str

def es_negativo_sap(valor_texto):
    v = str(valor_texto).strip()
    if "-" in v: return True
    return False

# --- FUNCIÓN PRINCIPAL ---
def ejecutar(ruta_excel, log_callback, check_stop, progress_callback, summary_callback, tabla_callback=None, silencioso=False, detallado=False):
    
    def print_log(msg):
        log_callback(str(msg))

    # --- GANCHO PARA DEPURADOR DE VS CODE ---
    try:
        pass
    except Exception:
        pass
        pass

    print_log(f"--- INICIANDO SCRIPT DE PAGOS (MÉTODO 1 OPTIMIZADO) ---")
    
    marca_tiempo = datetime.now().strftime("%d.%m.%Y_%H%M%S")
    ruta_csv = ruta_excel.replace(".xlsx", f"_resultados_{marca_tiempo}.csv")
    sep_sys = obtener_separador_sistema()
    
    stats = {
        'ok': 0,
        'omitidos': 0,
        'errores': 0,
        'monto': 0.0
    }

    # 1. LEER EXCEL O CSV
    try:
        if ruta_excel.endswith('.csv'):
            # Intento primero con punto y coma
            try: df = pd.read_csv(ruta_excel, sep=';', dtype=str, encoding='utf-8-sig')
            except: df = pd.read_csv(ruta_excel, sep=',', dtype=str, encoding='utf-8-sig')
            # Forzamos re-validación por si leyó mal las comas
            if len(df.columns) == 1 and ',' in df.columns[0]:
                df = pd.read_csv(ruta_excel, sep=',', dtype=str, encoding='utf-8-sig')
            
            # Limpiar posibles 'nan' literales leidos del CSV
            df.replace(to_replace=['nan', 'NaN'], value='', inplace=True)
            df.fillna('', inplace=True)
        else:
            df = pd.read_excel(ruta_excel, header=0, dtype={
                'cuenta_banco': str, 
                'clase_pago': str,
                'id_cliente': str,
                'no_doc': str,
                'no_boleta': str
            })
        
        # Inyección dinámica de columnas virtuales con orden estricto
        columnas_finales = [
            'sociedad', 'id_cliente', 'no_doc', 'monto_total', 'clase_pago',
            'txt_cab_doc', 'no_boleta', 'cuenta_banco', 'fecha_deposito',
            'concepto', 'observaciones', 'usuario_sap', 'fecha', 'hora', 'resultado'
        ]
        
        for col in columnas_finales:
            if col not in df.columns:
                df[col] = ""
        
        df['resultado'] = df['resultado'].astype(str)
        df = df[columnas_finales]
        
        total_filas = len(df)
        print_log(f"Registros cargados: {total_filas}")
    except Exception as e:
        print_log(f"Error leyendo Excel: {e}")
        summary_callback(stats)
        return 

    # 2. CONEXIÓN SAP CON AUTO-LOGIN
    if not hay_internet():
        print_log("❌ Error crítico: Se requiere conexión a Internet para iniciar.")
        stats['abortado_red'] = True
        summary_callback(stats)
        return
        
    sap_user = "DESCONOCIDO"
    try:
        session = conectar_sap_autologin()
        try: sap_user = session.Info.User
        except: pass
        
        if silencioso:
            pass # Deshabilitado según solicitud del usuario
    except Exception as e:
        print_log(f"Error SAP: {e}")
        summary_callback(stats)
        return

    # 3. BUCLE PRINCIPAL
    sociedad_actual_sap = None
    
    for index, row in df.iterrows():
        
        porcentaje = (index + 1) / total_filas
        progress_callback(porcentaje)

        if check_stop():
            print_log("\n[!!!] PROCESO DETENIDO POR EL USUARIO.")
            break 
        
        estado_actual = "" 
        monto_actual = 0.0

        try:
            if not hay_internet(timeout=1):
                raise Exception("com_error_preventivo: Desconexión de red detectada antes de ejecutar SAP.")
                
            # A. VALIDACIÓN PREVIA
            res_previo = str(row['resultado']).strip()
            if res_previo != "" and res_previo.lower() != "nan":
                stats['omitidos'] += 1
                continue 

            # LECTURA DE DATOS
            dato_sociedad = str(row['sociedad']).strip().upper()
            
            # Como ahora leemos como TEXTO, el .replace(".0", "") es preventivo
            primer_cliente = str(row['id_cliente']).replace(".0", "").strip()
            documento_buscar = str(row['no_doc']).replace(".0", "").strip()
            dato_monto_total = str(row['monto_total']).strip()
            
            monto_actual = sap_str_to_float(row['monto_total'])

            # CLASE DE PAGO: Manejo robusto de ceros
            dato_clase_pago = str(row['clase_pago']).replace(".0", "").strip()
            if len(dato_clase_pago) == 1: 
                dato_clase_pago = "0" + dato_clase_pago

            dato_texto = str(row['txt_cab_doc']).strip()
            if dato_texto == "nan": dato_texto = ""

            # Datos Popup
            dato_popup_G = str(row['no_boleta']).replace(".0", "").strip() 
            if dato_popup_G == "nan": dato_popup_G = ""
            
            dato_popup_H = str(row['cuenta_banco']).replace(".0", "").strip()    
            if dato_popup_H == "nan": dato_popup_H = ""
            
            dato_popup_I = limpiar_fecha(row['fecha_deposito'])                  
            if dato_popup_I == "nan": dato_popup_I = ""
            dato_popup_J = str(row['concepto']).replace(".0", "").strip()        
            if dato_popup_J == "nan": dato_popup_J = ""
            dato_popup_K = str(row['observaciones']).replace(".0", "").strip()   
            if dato_popup_K == "nan": dato_popup_K = ""

            if dato_sociedad == "NAN" or primer_cliente == "NAN": 
                stats['omitidos'] += 1
                if tabla_callback:
                    tabla_callback(datetime.now().strftime("%H:%M:%S"), primer_cliente, documento_buscar, "Omitido: Datos en blanco", dato_sociedad, dato_clase_pago, dato_popup_H, dato_popup_I)
                continue

            print_log(f"[{index+1}/{total_filas}] Cliente: {primer_cliente} | Doc: {documento_buscar}")

            # B. NAVEGACIÓN Y SELECCIÓN DE SOCIEDAD (MEMORIA DE ESTADO)
            if sociedad_actual_sap != dato_sociedad:
                # 1. FLUJO COMPLETO: Llamado limpio a la rutina de apertura
                abrir_caja_sap(session, dato_sociedad, print_log)
                sociedad_actual_sap = dato_sociedad
            
            else:
                # 2. FLUJO OPTIMIZADO (Misma sociedad, solo limpiar pantalla)
                try: 
                    session.findById("wnd[0]/tbar[1]/btn[13]").press() # Botón "Crear"
                    session.findById("wnd[0]/usr/tabsTABCONTROL/tabpTABBTN1").select() # Asegurar ubicarnos en la Pestaña 1
                except Exception as e: 
                    print_log(f"   [AVISO] No se pudo limpiar la pantalla para la siguiente fila: {e}")
            
            # D. BUSCAR CLIENTE
            input_id = "wnd[0]/usr/tabsTABCONTROL/tabpTABBTN1/ssubWORK_SCREEN:/DBM/MT_TILL:2002/subWORKING_AREA:/DBM/MT_TILL:2004/ctxt/DBM/T_WA_SEARCH-PARTNER"
            
            # LA ESPERA INTELIGENTE VA AQUÍ, DESPUÉS DE LOS POPUPS Y EL BOTÓN CREAR
            if not esperar_elemento(session, input_id, timeout=5):
                raise Exception(f"Timeout o ID no encontrado en esta pantalla (Esperando el campo Cliente). ID: {input_id}")
            
            session.findById(input_id).text = primer_cliente
            session.findById(input_id).setFocus()
            session.findById("wnd[0]").sendVKey(0)
            
            # ESPERA INTELIGENTE GRID
            grid_id = "wnd[0]/usr/tabsTABCONTROL/tabpTABBTN1/ssubWORK_SCREEN:/DBM/MT_TILL:2002/subWORKING_AREA:/DBM/MT_TILL:2004/cntlOPEN_ITEM_CON/shellcont/shell"
            grid_obj = None
            if esperar_elemento(session, grid_id, timeout=10):
                grid_tmp = session.findById(grid_id)
                if grid_tmp.RowCount >= 0:
                    grid_obj = grid_tmp
            
            if grid_obj is None:
                estado_actual = "Error: Grid no cargó (TimeOut)"
                print_log(f"   [ERROR] {estado_actual}")
                stats['errores'] += 1
            else:
                # --- VISUALIZACIÓN DE MATRIZ SAP ---
                grid_id = "wnd[0]/usr/tabsTABCONTROL/tabpTABBTN1/ssubWORK_SCREEN:/DBM/MT_TILL:2002/subWORKING_AREA:/DBM/MT_TILL:2004/cntlOPEN_ITEM_CON/shellcont/shell"
                log_matriz_sap(session, grid_id, print_log, docs_seleccionados=[documento_buscar])

                if grid_obj.RowCount > 0:
                    encontrado = False
                    
                    # === FRANCOTIRADOR ESTRICTO ===
                    COL_ID_DOC = "BELNR" 
                    COL_ID_MONTO = "DMBTR"
                    
                    # Quitamos ceros a la izquierda del Excel
                    doc_buscar_limpio = documento_buscar.lstrip("0")
                    
                    for r in range(grid_obj.RowCount):
                        
                        # Leemos SAP y quitamos ceros a la izquierda
                        try:
                            valor_celda_sap = str(grid_obj.GetCellValue(r, COL_ID_DOC)).strip()
                            valor_celda_sap_limpio = valor_celda_sap.lstrip("0")
                        except:
                            valor_celda_sap_limpio = ""
                        
                        # Comparación exacta
                        if valor_celda_sap_limpio == doc_buscar_limpio:
                            
                            # Validación Negativo (Lectura perezosa)
                            val_monto = str(grid_obj.GetCellValue(r, COL_ID_MONTO)).strip()
                            if es_negativo_sap(val_monto):
                                estado_actual = "Omitido: Saldo Negativo"
                                print_log(f"   -> {estado_actual}")
                                stats['omitidos'] += 1
                                encontrado = True
                                if tabla_callback:
                                    tabla_callback(datetime.now().strftime("%H:%M:%S"), primer_cliente, documento_buscar, estado_actual, dato_sociedad, dato_clase_pago, dato_popup_H, dato_popup_I)
                                break # Termina el bucle del grid

                            # PROCESO POSITIVO
                            grid_obj.CurrentCellRow = r
                            grid_obj.SelectedRows = str(r)
                            session.findById("wnd[0]/usr/tabsTABCONTROL/tabpTABBTN1/ssubWORK_SCREEN:/DBM/MT_TILL:2002/subWORKING_AREA:/DBM/MT_TILL:2004/btnBT_HANDLE").press()
                            
                            # SOLUCIÓN ERROR <unknown>.key (ESPERA INTELIGENTE)
                            base_pago = "wnd[0]/usr/tabsTABCONTROL/tabpTABBTN1/ssubWORK_SCREEN:/DBM/MT_TILL:2002/subWORKING_AREA:/DBM/MT_TILL:2004"
                            campos_listos = False
                            
                            for intento in range(4): 
                                try:
                                    monto_str = str(round(float(dato_monto_total), 2))
                                    session.findById(f"{base_pago}/txt/DBM/T_WA_WORK_LINE-AM_GET").text = monto_str
                                    session.findById(f"{base_pago}/cmb/DBM/T_WA_WORK_LINE-PAYMENT_TYPE").key = dato_clase_pago
                                    session.findById(f"{base_pago}/txt/DBM/T_WA_WORK_LINE-HEADER_TXT").text = dato_texto
                                    session.findById(f"{base_pago}/txt/DBM/T_WA_WORK_LINE-HEADER_TXT").setFocus()
                                    campos_listos = True
                                    
                                    if detallado: print_log(f"   [DETALLE] Insertando monto_total: {dato_monto_total} y clase: {dato_clase_pago}")
                                    break 
                                except:
                                    time.sleep(1) 
                            
                            if not campos_listos:
                                raise Exception("TimeOut: No se pudieron llenar los campos de pago (SAP Lento)")

                            session.findById("wnd[0]").sendVKey(0) 

                            # POPUP DATOS BANCARIOS
                            if session.Children.Count > 1:
                                base_popup = "wnd[1]/usr/sub:SAPLSPO4:0300"
                                try:
                                    session.findById(f"{base_popup}/txtSVALD-VALUE[0,21]").text = dato_popup_G
                                    session.findById(f"{base_popup}/ctxtSVALD-VALUE[1,21]").text = dato_popup_H
                                    c_I = f"{base_popup}/ctxtSVALD-VALUE[2,21]"
                                    session.findById(c_I).text = "" 
                                    session.findById(c_I).text = dato_popup_I
                                    session.findById(f"{base_popup}/ctxtSVALD-VALUE[3,21]").text = dato_popup_J
                                    session.findById(f"{base_popup}/txtSVALD-VALUE[4,21]").text = dato_popup_K
                                    session.findById("wnd[1]/tbar[0]/btn[0]").press()
                                except Exception as err_popup:
                                    print_log(f"   [AVISO] Fallo introduciendo datos al popup: {err_popup}")
                                    try: session.findById("wnd[1]/tbar[0]/btn[0]").press()
                                    except Exception as err_cierre: print_log(f"   [ERROR] No se pudo cerrar popup: {err_cierre}")
                            
                            session.findById("wnd[0]/tbar[1]/btn[17]").press()
                            
                            hubo_error = False
                            
                            # Validar Errores Popup (wnd[2] y wnd[1])
                            if session.Children.Count > 2:
                                try:
                                    txt1 = session.findById("wnd[2]/usr/txtMESSTXT1").text
                                    txt2 = session.findById("wnd[2]/usr/txtMESSTXT2").text
                                    if txt1 or txt2:
                                        estado_actual = f"Error Popup: {txt1} {txt2}".strip()
                                        print_log(f"   [ERROR] -> {estado_actual}")
                                        stats['errores'] += 1
                                        try: session.findById("wnd[2]").sendVKey(0)
                                        except: pass
                                        try: session.findById("wnd[1]").sendVKey(0)
                                        except: pass
                                        hubo_error = True
                                except: pass

                            if not hubo_error and session.Children.Count > 1:
                                try:
                                    txt_error = session.findById("wnd[1]/usr/txtSPOP-TEXTLINE1").text
                                    if txt_error:
                                        estado_actual = f"Error SAP: {txt_error}"
                                        print_log(f"   [ERROR] -> {estado_actual}")
                                        stats['errores'] += 1
                                        try: session.findById("wnd[1]").sendVKey(0)
                                        except: pass
                                        hubo_error = True
                                except: pass

                                if not hubo_error:
                                    try:
                                        txt1 = session.findById("wnd[1]/usr/txtMESSTXT1").text
                                        txt2 = session.findById("wnd[1]/usr/txtMESSTXT2").text
                                        if txt1 or txt2:
                                            msg_popup = f"{txt1} {txt2}".strip()
                                            try: session.findById("wnd[1]").sendVKey(0)
                                            except: pass
                                            
                                            if "error" in msg_popup.lower() or "incorrecto" in msg_popup.lower() or "invalido" in msg_popup.lower():
                                                estado_actual = f"Error: {msg_popup}"
                                                print_log(f"   [ERROR] -> {estado_actual}")
                                                stats['errores'] += 1
                                                hubo_error = True
                                            else:
                                                estado_actual = msg_popup # Era un éxito
                                    except: pass
                            
                            if hubo_error:
                                encontrado = True
                                break # Termina el bucle del Grid
                            
                            try:
                                mensaje_sap = session.findById("wnd[0]/sbar/pane[0]").text
                                print_log(f"   -> {mensaje_sap}")
                                
                                # VERIFICAR ERROR EN LA BARRA DE ESTADO DE SAP
                                msg_low = mensaje_sap.lower()
                                if any(x in msg_low for x in ["error", "incorrecto", "invalido", "zbol", "nota de cr", "no existe"]):
                                    estado_actual = f"Error SAP: {mensaje_sap}"
                                    stats['errores'] += 1
                                    hubo_error = True
                                else:
                                    estado_actual = mensaje_sap
                                    stats['ok'] += 1
                                    stats['monto'] += monto_actual
                            except:
                                estado_actual = "Contabilizado (Sin leer barra)"
                                stats['ok'] += 1
                                stats['monto'] += monto_actual
                            
                            if hubo_error:
                                encontrado = True
                                break # Termina el bucle del Grid y evita el Cierre Contable    
                            
                            # Polling Dinámico: Esperar a que la ventana cambie (aparezca popup)
                            for _ in range(15):
                                if session.Children.Count > 1: break
                                time.sleep(0.3)
                            
                            if session.Children.Count > 1:
                                # Pausa inteligente para asegurar que los elementos del spool ya cargaron
                                if esperar_elemento(session, "wnd[1]/tbar[0]/btn[86]", timeout=3):
                                    try: session.findById("wnd[1]/usr/chkSSFPP-TDNEWID").selected = True
                                    except Exception as e_chk: print_log(f"   [AVISO] Checkbox de impresión no hallado: {e_chk}")
                                    
                                    try: session.findById("wnd[1]/tbar[0]/btn[86]").press()
                                    except Exception as e_btn: print_log(f"   [AVISO] Botón de impresión no pulsado: {e_btn}")
                            
                            # --- CIERRE CONTABLE ---
                            datos_cierre = {
                                'sociedad': dato_sociedad,
                                'cuenta_banco': dato_popup_H,
                                'clase_pago': dato_clase_pago,
                                'monto_total': dato_monto_total,
                                'no_doc_deposito': dato_popup_G
                            }
                            print_log("Iniciando cierre demostrativo...")
                            cierre_ok, msj_cierre = ejecutar_cierre(session, datos_cierre, print_log)
                            if cierre_ok:
                                estado_actual += f" | Cierre OK: {msj_cierre}"
                            else:
                                estado_actual += f" | Err Cierre: {msj_cierre}"
                            # ---------------------------

                            encontrado = True
                            break # Termina el bucle del Grid al encontrar y procesar el documento
                    
                    if not encontrado:
                        estado_actual = "Doc no encontrado en Grid"
                        print_log(f"   [AVISO] {estado_actual}")
                        stats['omitidos'] += 1

        except Exception as e_row:
            err_msg = str(e_row).lower()
            err_class = e_row.__class__.__name__
            # Detectar errores COM típicos de PyWin32 o nuestros chequeos preventivos
            if err_class == "com_error" or "com_error_preventivo" in err_msg or "-2147" in err_msg or "rpc" in err_msg or "desconect" in err_msg or "disconnect" in err_msg:
                print_log(f"⚠️ DETECTADA CAÍDA DE RED: {e_row}")
                estado_duda = "⚠️ REVISIÓN MANUAL: Caída de Red"
                df.at[index, 'resultado'] = estado_duda
                stats['errores'] += 1
                if tabla_callback:
                    tabla_callback(datetime.now().strftime("%H:%M:%S"), primer_cliente, documento_buscar, estado_duda, dato_sociedad, dato_clase_pago, dato_popup_H, dato_popup_I)
                # RECONNECT LOOP GENTIL
                print_log("Intentando restablecer sesión de SAP...")
                reintentos = 0
                timeout_red = False
                while not hay_internet():
                    if check_stop(): break
                    if reintentos >= 120: # 10 minutos (120 * 5s)
                        timeout_red = True
                        break
                    if reintentos % 12 == 0: # Cada minuto loguea
                        print_log("⏳ Esperando conexión a Internet para reconectar...")
                    time.sleep(5)
                    reintentos += 1
                
                if timeout_red:
                    print_log("❌ Abortando: Se superó el límite de 10 minutos sin conexión.")
                    break
                    
                if check_stop(): break
                
                # Damos 5 segundos adicionales para que el Watchdog cierre el SAP zombie
                # y Windows libere los sockets antes de intentar relanzar SAP
                print_log("⏳ Estabilizando red (5s)...")
                time.sleep(5)
                
                if not hay_internet():
                    print_log("❌ La red no es estable. Esperando un ciclo más...")
                    continue  # Volver al inicio del for con el mismo index saltado
                
                try:
                    session = conectar_sap_autologin()
                    print_log("✅ Sesión recuperada. Continuando con el siguiente registro...")
                    sociedad_actual_sap = None
                    continue
                except Exception as rec_err:
                    print_log(f"❌ Fallo crítico: No se pudo recuperar la conexión ({rec_err}).")
                    break
            else:
                estado_actual = f"Error crítico: {e_row}"
                print_log(f"Error fila {index}: {e_row}")
                stats['errores'] += 1

        if estado_actual != "":
            df.at[index, 'resultado'] = estado_actual
            df.at[index, 'usuario_sap'] = sap_user
            df.at[index, 'fecha'] = datetime.now().strftime("%d.%m.%Y")
            df.at[index, 'hora'] = datetime.now().strftime("%H:%M:%S")
            if tabla_callback:
                if "Omitido" not in estado_actual: 
                    tabla_callback(datetime.now().strftime("%H:%M:%S"), primer_cliente, documento_buscar, estado_actual, dato_sociedad, dato_clase_pago, dato_popup_H, dato_popup_I)

            # Autoguardado Súper Rápido en CSV incremental
            try: df.to_csv(ruta_csv, index=False, sep=sep_sys, encoding='utf-8-sig')
            except: pass
    
    # GUARDADO FINAL AL TERMINAR EL BUCLE (1 sola vez)
    # GUARDA EL CSV DEFINITIVO
    print_log("Guardando archivo CSV definitivo...")
    try: df.to_csv(ruta_csv, index=False, sep=sep_sys, encoding='utf-8-sig')
    except Exception as e: print_log(f"Error al guardar CSV final: {e}")

    # ---------------- ENVIAR TELEMETRÍA A LA UI PRINCIPAL ----------------
    stats['transacciones_detalle'] = df.to_dict(orient='records')
    # --------------------------------------------------------------

    summary_callback(stats)
    print_log("--- FIN DEL SCRIPT ---")