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

def limpiar_string(valor):
    if pd.isna(valor):
        return ""
    return str(valor).strip()

# ==============================================================================
# CONFIGURACIÓN INTERNA Y CONSTANTES
# ==============================================================================
COL_RES_01 = "resultado_01" # Para FACTURAS
COL_RES_02 = "resultado_02" # Para CAPITAL

# IDs Técnicos del Grid SAP (Ajustar si tu SAP tiene otra configuración)
COL_ID_IMPORTE = "DMBTR"    # Monto
COL_ID_CUOTA = "ZTERM"      # Cuota / Condición pago
COL_ID_FECHA = "ZFBDT"      # Fecha base
COL_ID_REFERENCIA = "XBLNR" # Campo Referencia
COL_ID_DOC = "BELNR"        # Número de Documento (Para detectar 97...)
COL_ID_TEXTO = "SGTXT"      # Texto (Para buscar la operación financiera)

# ==============================================================================
# FUNCIONES AUXILIARES DE LIMPIEZA
# ==============================================================================
# ==============================================================================

def limpiar_fecha(valor):
    valor_str = str(valor).strip()
    if isinstance(valor, (pd.Timestamp, datetime)):
        return valor.strftime("%d.%m.%Y")
    if " " in valor_str:
        valor_str = valor_str.split(" ")[0]
    return valor_str

def extraer_operacion_de_texto(texto_sap):
    """Obtiene la referencia numérica al final del texto (quita ceros izq)."""
    try:
        if not texto_sap: return ""
        fragmentos = texto_sap.strip().split(" ")
        ultimo_valor = fragmentos[-1]
        return ultimo_valor.lstrip("0")
    except:
        return ""

# ==============================================================================
# LÓGICA DE NAVEGACIÓN Y POSTEO (REUTILIZABLE)
# ==============================================================================
def ir_a_transaccion_y_cargar_cliente(session, id_cliente, dato_sociedad, sociedad_actual_sap):
    """Reinicia la transacción e ingresa el cliente, optimizando con botón Crear."""
    try:
        if sociedad_actual_sap != dato_sociedad:
            # 1. FLUJO COMPLETO: Llamado a rutina principal de apertura de CAJA
            abrir_caja_sap(session, dato_sociedad)
            
        else:
            # 2. FLUJO OPTIMIZADO (Misma sociedad)
            try: 
                session.findById("wnd[0]/tbar[1]/btn[13]").press()
                session.findById("wnd[0]/usr/tabsTABCONTROL/tabpTABBTN1").select()
            except: pass

        # Ingresar Cliente
        input_id = "wnd[0]/usr/tabsTABCONTROL/tabpTABBTN1/ssubWORK_SCREEN:/DBM/MT_TILL:2002/subWORKING_AREA:/DBM/MT_TILL:2004/ctxt/DBM/T_WA_SEARCH-PARTNER"
        esperar_elemento(session, input_id, timeout=3)
        session.findById(input_id).text = id_cliente
        session.findById(input_id).setFocus()
        session.findById("wnd[0]").sendVKey(0)
        esperar_elemento(session, "wnd[0]/usr/tabsTABCONTROL/tabpTABBTN1/ssubWORK_SCREEN:/DBM/MT_TILL:2002/subWORKING_AREA:/DBM/MT_TILL:2004/cntlOPEN_ITEM_CON/shellcont/shell", timeout=5)
        return True
    except Exception as e:
        return False

def postear_pago(session, filas_a_seleccionar, monto_a_pagar, datos_cabecera):
    """
    Realiza la acción de seleccionar filas, llenar montos y guardar.
    Retorna (True/False, Mensaje_SAP)
    """
    try:
        grid_id = "wnd[0]/usr/tabsTABCONTROL/tabpTABBTN1/ssubWORK_SCREEN:/DBM/MT_TILL:2002/subWORKING_AREA:/DBM/MT_TILL:2004/cntlOPEN_ITEM_CON/shellcont/shell"
        grid = session.findById(grid_id)

        # 1. Seleccionar filas
        seleccion_str = ",".join(filas_a_seleccionar)
        grid.SelectedRows = seleccion_str
        
        # 2. Activar partidas
        session.findById("wnd[0]/usr/tabsTABCONTROL/tabpTABBTN1/ssubWORK_SCREEN:/DBM/MT_TILL:2002/subWORKING_AREA:/DBM/MT_TILL:2004/btnBT_HANDLE").press()
        base_pago = "wnd[0]/usr/tabsTABCONTROL/tabpTABBTN1/ssubWORK_SCREEN:/DBM/MT_TILL:2002/subWORKING_AREA:/DBM/MT_TILL:2004"
        esperar_elemento(session, f"{base_pago}/txt/DBM/T_WA_WORK_LINE-AM_GET", timeout=5)

        # 3. Llenar cabecera
        base_pago = "wnd[0]/usr/tabsTABCONTROL/tabpTABBTN1/ssubWORK_SCREEN:/DBM/MT_TILL:2002/subWORKING_AREA:/DBM/MT_TILL:2004"
        try: session.findById(f"{base_pago}/cmb/DBM/T_WA_WORK_LINE-PAYMENT_TYPE").key = datos_cabecera['clase_pago']
        except: pass

        # Asegurar máximo 2 decimales para evitar rechazo de SAP por inexactitud del float de Python
        monto_str = str(round(float(monto_a_pagar), 2))
        session.findById(f"{base_pago}/txt/DBM/T_WA_WORK_LINE-AM_GET").text = monto_str
        
        try: session.findById(f"{base_pago}/txt/DBM/T_WA_WORK_LINE-HEADER_TXT").text = datos_cabecera['no_boleta']
        except: pass
        
        session.findById(f"{base_pago}/txt/DBM/T_WA_WORK_LINE-HEADER_TXT").setFocus()
        session.findById("wnd[0]").sendVKey(0) 
        time.sleep(1)

        # 4. Popup Datos Adicionales (Si sale)
        if session.Children.Count > 1:
            popup_id = "wnd[1]/usr/sub:SAPLSPO4:0300"
            try:
                session.findById(f"{popup_id}/txtSVALD-VALUE[0,21]").text = datos_cabecera['nota_credito']
                session.findById(f"{popup_id}/ctxtSVALD-VALUE[1,21]").text = datos_cabecera['cuenta_banco']
                session.findById(f"{popup_id}/ctxtSVALD-VALUE[2,21]").text = datos_cabecera['fecha_doc']
                session.findById("wnd[1]/tbar[0]/btn[0]").press()
            except:
                try: session.findById("wnd[1]/tbar[0]/btn[0]").press()
                except: pass
        
        # 5. Guardar / Contabilizar
        session.findById("wnd[0]/tbar[1]/btn[17]").press()

        # 6. Capturar mensaje
        msg_out = "Exito (Sin msg)"
        
        # Validar si SAP tiró un Error en Popup Secundario wnd[2]
        if session.Children.Count > 2:
            try:
                txt1 = session.findById("wnd[2]/usr/txtMESSTXT1").text
                txt2 = session.findById("wnd[2]/usr/txtMESSTXT2").text
                if txt1 or txt2:
                    msg_out = f"Error Popup: {txt1} {txt2}".strip()
                    try: session.findById("wnd[2]").sendVKey(0)
                    except: pass
                    try: session.findById("wnd[1]").sendVKey(0)
                    except: pass
                    return False, msg_out
            except: pass

        # Validar Popup de validación (wnd[1]) que puede ser Error o Info
        if session.Children.Count > 1:
            try:
                # Comprobar si existe el texto de error grave en SPOP
                txt_error = session.findById("wnd[1]/usr/txtSPOP-TEXTLINE1").text
                if txt_error:
                    try: session.findById("wnd[1]").sendVKey(0) # Intentar cerrar popup
                    except: pass
                    return False, f"Error SAP: {txt_error}"
            except: pass

            try:
                txt1 = session.findById("wnd[1]/usr/txtMESSTXT1").text
                txt2 = session.findById("wnd[1]/usr/txtMESSTXT2").text
                if txt1 or txt2:
                    msg_popup = f"{txt1} {txt2}".strip()
                    try: session.findById("wnd[1]").sendVKey(0) # Cerrar popup info/error
                    except: pass
                    
                    if "error" in msg_popup.lower() or "incorrecto" in msg_popup.lower() or "invalido" in msg_popup.lower():
                        return False, f"Error: {msg_popup}"
                    else:
                        msg_out = msg_popup # Era un popup de éxito
            except: pass
        
        # Si NO hubo popup o fue de éxito, leemos la barra de estado general de SAP
        try: 
            sbar = session.findById("wnd[0]/sbar/pane[0]").text
            if sbar: 
                if "error" in sbar.lower() or "incorrecto" in sbar.lower() or "invalido" in sbar.lower() or "zbol" in sbar.lower() or "nota de cr" in sbar.lower():
                    return False, sbar
                else:
                    if "Exito" in msg_out: msg_out = sbar
                    else: msg_out = f"{msg_out} | {sbar}"
        except: pass

        # 7. Impresión (Opcional)
        # Esperar a que la ventana cambie (aparezca popup)
        for _ in range(15):
            if session.Children.Count > 1: break
            time.sleep(0.2)
            
        if session.Children.Count > 1:
            # Pausa inteligente para asegurar que los elementos del spool ya cargaron
            if esperar_elemento(session, "wnd[1]/tbar[0]/btn[86]", timeout=3):
                try: session.findById("wnd[1]/usr/chkSSFPP-TDNEWID").selected = True
                except: pass
                try: session.findById("wnd[1]/tbar[0]/btn[86]").press()
                except: pass

        return True, msg_out

    except Exception as e:
        return False, str(e)

# ==============================================================================
# FUNCIÓN PRINCIPAL
# ==============================================================================
def ejecutar(ruta_excel, log_callback, check_stop, progress_callback, summary_callback, tabla_callback=None, silencioso=False, detallado=False):
    # --- GANCHO PARA DEPURADOR DE VS CODE ---
    # Fuerza a VS Code a rastrear esta función aunque corra en un QThread de fondo
    try:
        import debugpy
        debugpy.debug_this_thread()
    except Exception:
        pass

    def print_log(msg):
        log_callback(str(msg))

    stats = {
        'ok': 0,
        'omitidos': 0,
        'errores': 0,
        'monto': 0.0
    }

    # 1. CONEXIÓN SAP CON AUTO-LOGIN
    if not hay_internet():
        print_log("❌ Error crítico: Se requiere conexión a Internet para iniciar.")
        stats['abortado_red'] = True
        summary_callback(stats)
        return
        
    sap_user = "DESCONOCIDO"
    try:
        session = conectar_sap_autologin()
        if silencioso:
            pass # Deshabilitado según requerimiento
        print_log(f"--- INICIANDO SCRIPT DE COBROS (MÉTODO 2 OPTIMIZADO) ---")
        try: sap_user = session.Info.User
        except: pass
    except Exception as e:
        print_log(f"ERROR CRÍTICO: {e}")
        summary_callback(stats)
        return

    marca_tiempo = datetime.now().strftime("%d.%m.%Y_%H%M%S")
    ruta_csv = ruta_excel.replace(".xlsx", f"_resultados_{marca_tiempo}.csv")
    sep_sys = obtener_separador_sistema()

    # 2. LEER EXCEL O CSV
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
            df = pd.read_excel(ruta_excel, header=0, dtype=str)
        
        # Limpieza inicial y orden estricto de columnas
        columnas_finales = [
            'sociedad', 'id_cliente', 'fecha_documento', 'no_boleta', 
            'cuenta_banco', 'monto_total', 'clase_pago', 'comentario', 'nota_credito',
            'usuario_sap', 'fecha', 'hora', COL_RES_01, COL_RES_02
        ]
        for i in range(1, 11): columnas_finales.append(f"cobro_{i:02d}")
        
        for col in columnas_finales:
            if col not in df.columns: df[col] = ""
            
        df = df[columnas_finales]

        total_filas = len(df)
        print_log(f"Registros cargados: {total_filas}")
    except Exception as e:
        print_log(f"Error Excel: {e}")
        summary_callback(stats)
        return

    # 3. BUCLE POR CLIENTE
    sociedad_actual_sap = None
    for index, row in df.iterrows():
        try:
            if not hay_internet(timeout=1):
                raise Exception("com_error_preventivo: Desconexión de red detectada antes de ejecutar SAP.")
            
            porcentaje = (index + 1) / total_filas
            progress_callback(porcentaje)

            if check_stop():
                print_log("[!!!] DETENIDO POR USUARIO")
                break 

            # --- VARIABLES DE RESULTADO PARA ESTA FILA ---
            txt_res_facturas = ""
            txt_res_capital = ""
            capital_pagado_monto = 0.0

            # Validar si ya se procesó (Checamos COL_RES_01 o COL_RES_02)
            ya_procesado_1 = str(row[COL_RES_01]).strip() not in ["", "nan"]
            ya_procesado_2 = str(row[COL_RES_02]).strip() not in ["", "nan"]
            
            if ya_procesado_1 or ya_procesado_2:
                stats['omitidos'] += 1
                continue

            id_cliente = str(row['id_cliente']).replace(".0", "").strip()
            if not id_cliente or id_cliente.lower() == "nan":
                stats['omitidos'] += 1
                if tabla_callback:
                    tabla_callback(datetime.now().strftime("%H:%M:%S"), "SIN CLIENTE", "-", "Omitido: Datos faltantes", str(row['sociedad']), str(row['clase_pago']), str(row['cuenta_banco']), "")
                continue

            # Datos Financieros
            try: monto_inicial = float(str(row['monto_total']).replace(",", ""))
            except: monto_inicial = 0.0
            
            monto_disponible = monto_inicial

            # Datos SAP Header
            datos_cabecera = {
                'sociedad': str(row['sociedad']).strip().upper(),
                'clase_pago': str(row['clase_pago']).replace(".0", "").strip().zfill(2),
                'no_boleta': str(row['no_boleta']).replace(".0", "").strip().replace("nan", ""),
                'cuenta_banco': str(row['cuenta_banco']).replace(".0", "").strip().replace("nan", ""),
                'nota_credito': str(row['nota_credito']).replace(".0", "").strip().replace("nan", ""),
                'fecha_doc': limpiar_fecha(row['fecha_documento']).replace("nan", "")
            }

            # Referencia (Operación Financiera)
            dato_referencia = str(row['comentario']).replace(".0", "").strip()
            dato_referencia_clean = dato_referencia.lstrip("0")
            if dato_referencia.lower() == "nan": dato_referencia_clean = ""

            if detallado: print_log(f"[{index+1}] Cte: {id_cliente} | Disp: {monto_disponible} | Ref: {dato_referencia}")

            # ==================================================================
            # FASE 1: FACTURAS (RESULTADO A COL_RES_01)
            # ==================================================================
            facturas_pagadas_monto = 0.0
            
            # a) Cargar Cliente (Devuelve el nuevo estado de la sociedad y True/False)
            if ir_a_transaccion_y_cargar_cliente(session, id_cliente, datos_cabecera['sociedad'], sociedad_actual_sap):
                sociedad_actual_sap = datos_cabecera['sociedad']
                
                # b) Analizar Grid para Facturas
                grid = session.findById("wnd[0]/usr/tabsTABCONTROL/tabpTABBTN1/ssubWORK_SCREEN:/DBM/MT_TILL:2002/subWORKING_AREA:/DBM/MT_TILL:2004/cntlOPEN_ITEM_CON/shellcont/shell")
                
                lista_facturas = []
                if grid.RowCount > 0:
                    for r in range(grid.RowCount):
                        doc_sap = str(grid.GetCellValue(r, COL_ID_DOC)).strip()

                        # Condición: Empieza con 97 Y coincide el texto con la Op. Financiera
                        if doc_sap.startswith("97"):
                            texto_sap = str(grid.GetCellValue(r, COL_ID_TEXTO)).strip()
                            op_fin = extraer_operacion_de_texto(texto_sap)
                            
                            if op_fin and (op_fin == dato_referencia_clean):
                                importe = sap_str_to_float(grid.GetCellValue(r, COL_ID_IMPORTE))
                                lista_facturas.append({'fila': str(r), 'monto': importe, 'doc_sap': doc_sap})

                # c) Ejecutar Pago Facturas (Si existen)
                total_facturas = sum(f['monto'] for f in lista_facturas)

                if len(lista_facturas) > 0:
                    print_log(f"   [SAP] Facturas idóneas: {len(lista_facturas)} | Total a cubrir: Q.{round(total_facturas, 2)}")
                    for f in lista_facturas:
                        print_log(f"         > Fila {f['fila']} | Doc: {f['doc_sap']} | Monto: Q.{f['monto']}")
                
                if total_facturas > 0:
                    if monto_disponible >= (total_facturas - 0.01):
                        if detallado: print_log(f"   -> Pagando Facturas: {total_facturas} (Exclusivo)")
                        filas_fact = [f['fila'] for f in lista_facturas]
                        
                        exito, msg = postear_pago(session, filas_fact, total_facturas, datos_cabecera)
                        
                        if exito:
                            facturas_pagadas_monto = total_facturas
                            monto_disponible -= total_facturas
                            txt_res_facturas = f"Facturas OK ({total_facturas})" # RESULTADO 1
                            stats['monto'] += total_facturas
                        else:
                            txt_res_facturas = f"Err Facturas: {msg}" # RESULTADO 1
                    else:
                        # BLOQUEO DE SEGURIDAD
                        txt_res_facturas = "Saldo insuficiente Facturas" # RESULTADO 1
                        monto_disponible = 0 
                else:
                    # No hay facturas
                    txt_res_facturas = "" # O "Sin Facturas", dejaremos vacio si no hay acción
                    pass

            # ==================================================================
            # FASE 2: CAPITAL (RESULTADO A COL_RES_02)
            # ==================================================================
            
            if monto_disponible > 0.01:
                
                # RECARGAR GRID (Solo si se operó en Fase 1 y se guardó/salió de la pantalla de partidas)
                if facturas_pagadas_monto > 0:
                    if ir_a_transaccion_y_cargar_cliente(session, id_cliente, datos_cabecera['sociedad'], sociedad_actual_sap):
                        sociedad_actual_sap = datos_cabecera['sociedad']
                
                grid = session.findById("wnd[0]/usr/tabsTABCONTROL/tabpTABBTN1/ssubWORK_SCREEN:/DBM/MT_TILL:2002/subWORKING_AREA:/DBM/MT_TILL:2004/cntlOPEN_ITEM_CON/shellcont/shell")
                
                lista_capital = []
                if grid.RowCount > 0:
                    for r in range(grid.RowCount):
                        doc_sap = str(grid.GetCellValue(r, COL_ID_DOC)).strip()
                        
                        # Solo procesar si NO es factura
                        if not doc_sap.startswith("97"):
                            ref_sap = str(grid.GetCellValue(r, COL_ID_REFERENCIA)).strip()
                            if dato_referencia != "" and dato_referencia == ref_sap:
                                cuota = str(grid.GetCellValue(r, COL_ID_CUOTA)).strip()
                                fecha = str(grid.GetCellValue(r, COL_ID_FECHA)).strip()
                                importe = sap_str_to_float(grid.GetCellValue(r, COL_ID_IMPORTE))
                                
                                lista_capital.append({
                                    'fila': r,
                                    'cuota': cuota,
                                    'fecha': fecha,
                                    'monto': importe,
                                    'doc_sap': doc_sap
                                })
                    
                    lista_capital.sort(key=lambda x: (x['cuota'], x['fecha']))
                    
                    # --- REPORTE DE MATRIZ SAP (FACTURAS + CAPITAL) ---
                    docs_sel = [f['doc_sap'] for f in lista_facturas] + [c['doc_sap'] for c in lista_capital]
                    grid_id = "wnd[0]/usr/tabsTABCONTROL/tabpTABBTN1/ssubWORK_SCREEN:/DBM/MT_TILL:2002/subWORKING_AREA:/DBM/MT_TILL:2004/cntlOPEN_ITEM_CON/shellcont/shell"
                    log_matriz_sap(session, grid_id, print_log, docs_seleccionados=docs_sel)

                    filas_a_pagar = []
                    detalles_cobro = {}
                    idx_cobro = 1
                    monto_a_procesar_cap = 0.0
                    temp_disponible = monto_disponible

                    for item in lista_capital:
                        if temp_disponible > 0.01:
                            pagar = round(min(item['monto'], temp_disponible), 2)
                            filas_a_pagar.append(str(item['fila']))
                            monto_a_procesar_cap = round(monto_a_procesar_cap + pagar, 2)
                            temp_disponible = round(temp_disponible - pagar, 2)
                            
                            col_name = f"cobro_{idx_cobro:02d}"
                            detalles_cobro[col_name] = pagar
                            idx_cobro += 1
                        else:
                            break
                    
                    if filas_a_pagar:
                        print_log(f"   -> Pagando Capital: {monto_a_procesar_cap}")
                        exito, msg = postear_pago(session, filas_a_pagar, monto_a_procesar_cap, datos_cabecera)
                        
                        if exito:
                            txt_res_capital = msg # RESULTADO 2
                            stats['monto'] += monto_a_procesar_cap
                            capital_pagado_monto = monto_a_procesar_cap
                            
                            for k, v in detalles_cobro.items():
                                df.at[index, k] = v
                        else:
                            txt_res_capital = f"Err Capital: {msg}" # RESULTADO 2
                    else:
                        if facturas_pagadas_monto == 0:
                            txt_res_capital = "Sin partidas pendientes" # RESULTADO 2 (Si no hubo facturas tampoco)
                        else:
                            txt_res_capital = "Sin Capital pendiente"
                else:
                    if facturas_pagadas_monto == 0:
                        txt_res_capital = "Grid Vacio"
                    else:
                        txt_res_capital = "Grid Vacio (Post-Factura)"

            # --- ESCRITURA FINAL DE RESULTADOS ---
            # --- CIERRE DEMOSTRATIVO ---
            monto_total_cobrado = facturas_pagadas_monto + capital_pagado_monto
            txt_cierre = ""
            if monto_total_cobrado > 0:
                datos_cierre = {
                    'sociedad': datos_cabecera['sociedad'],
                    'cuenta_banco': datos_cabecera['cuenta_banco'],
                    'clase_pago': datos_cabecera['clase_pago'],
                    'monto_total': str(round(monto_total_cobrado, 2)),
                    'no_doc_deposito': datos_cabecera['nota_credito']
                }
                print_log("Iniciando cierre demostrativo...")
                cierre_ok, msj_cierre = ejecutar_cierre(session, datos_cierre, print_log)
                if cierre_ok:
                    txt_cierre = f"Cierre OK: {msj_cierre}"
                else:
                    txt_cierre = f"Err Cierre: {msj_cierre}"
            # ---------------------------

            df.at[index, 'fecha'] = datetime.now().strftime("%d.%m.%Y")
            df.at[index, 'hora'] = datetime.now().strftime("%H:%M:%S")
            df.at[index, 'usuario_sap'] = sap_user

            # --- EVALUACIÓN DE ESTADO Y CONTADORES ---
            txt_res_facturas = "N/A" if not txt_res_facturas else txt_res_facturas
            txt_res_capital = "N/A" if not txt_res_capital else txt_res_capital
            txt_cierre = "" if not txt_cierre else txt_cierre
            
            res_01 = f"F: {txt_res_facturas} | C: {txt_res_capital}".strip(" | ")
            res_02 = txt_cierre
            
            combinado = f"{res_01} | {res_02}".strip(" | ")
            combinado_lower = combinado.lower()
            
            df.at[index, COL_RES_01] = res_01
            df.at[index, COL_RES_02] = res_02
            
            # Limpiamos el prefijo 'Err ' si es un caso especial de Omitido
            mensaje_limpio = combinado
            if "zbol" in combinado_lower or "nota de cr" in combinado_lower:
                mensaje_limpio = combinado.replace("Err Capital: ", "").replace("Err Factura: ", "")
                estado_visual = f"Omitido: {mensaje_limpio}"
                stats['omitidos'] += 1
            # Evitamos que la palabra 'Cierre' dispare el substring 'err'
            elif "err " in combinado_lower or "err:" in combinado_lower or "error" in combinado_lower or "fall" in combinado_lower:
                estado_visual = f"Error: {combinado}"
                stats['errores'] += 1
            elif "sin " in txt_res_facturas.lower() and ("sin " in txt_res_capital.lower() or "vacio" in txt_res_capital.lower() or "vacío" in txt_res_capital.lower()):
                estado_visual = "Omitido: Sin partidas"
                stats['omitidos'] += 1
            else:
                estado_visual = combinado
                stats['ok'] += 1
            
            # --- MANDAR DATOS A LA TABLA VISUAL ---
            if tabla_callback:
                tabla_callback(
                    datetime.now().strftime("%H:%M:%S"), 
                    id_cliente, 
                    datos_cabecera['no_boleta'], 
                    estado_visual, 
                    datos_cabecera['sociedad'], 
                    datos_cabecera['clase_pago'], 
                    datos_cabecera['cuenta_banco'], 
                    datos_cabecera['fecha_doc']
                )

            # Autoguardado Súper Rápido en CSV incremental
            try: df.to_csv(ruta_csv, index=False, sep=sep_sys, encoding='utf-8-sig')
            except: pass

        except Exception as e_gral:
            err_msg = str(e_gral).lower()
            err_class = e_gral.__class__.__name__
            # Detectar errores COM típicos de PyWin32 cuando SAP cae
            if err_class == "com_error" or "com_error_preventivo" in err_msg or "-2147" in err_msg or "rpc" in err_msg or "desconect" in err_msg or "disconnect" in err_msg:
                print_log(f"⚠️ DETECTADA CAÍDA DE RED: {e_gral}")
                estado_duda = "⚠️ REVISIÓN MANUAL: Caída de Red"
                df.at[index, COL_RES_01] = estado_duda
                stats['errores'] += 1
                if tabla_callback:
                    tabla_callback(datetime.now().strftime("%H:%M:%S"), id_cliente, "-", estado_duda, datos_cabecera['sociedad'], datos_cabecera['clase_pago'], datos_cabecera['cuenta_banco'], datos_cabecera['fecha_doc'])
                # RECONNECT LOOP GENTIL
                print_log("Intentando restablecer sesión de SAP...")
                reintentos = 0
                timeout_red = False
                while not hay_internet():
                    if check_stop(): break
                    if reintentos >= 120: # 10 minutos (120 * 5s)
                        timeout_red = True
                        break
                    if reintentos % 12 == 0: # Cada minuto
                        print_log("⏳ Esperando conexión a Internet para reconectar...")
                    time.sleep(5)
                    reintentos += 1
                
                if timeout_red:
                    print_log("❌ Abortando: Se superó el límite de 10 minutos sin conexión.")
                    break
                
                if check_stop(): break
                try:
                    session = conectar_sap_autologin()
                    print_log("✅ Sesión recuperada. Continuando con el siguiente registro...")
                    sociedad_actual_sap = None
                    continue
                except Exception as rec_err:
                    print_log(f"❌ Fallo crítico: No se pudo recuperar la conexión ({rec_err}).")
                    break
            else:
                print_log(f"Error Fila: {e_gral}")
                df.at[index, COL_RES_01] = f"Error Script: {e_gral}"
                df.at[index, 'usuario_sap'] = sap_user
                df.at[index, 'fecha'] = datetime.now().strftime("%d.%m.%Y")
                df.at[index, 'hora'] = datetime.now().strftime("%H:%M:%S")
                stats['errores'] += 1
                if tabla_callback:
                    if 'id_cliente' not in locals(): id_cliente = "Desconocido"
                    tabla_callback(datetime.now().strftime("%H:%M:%S"), id_cliente, "-", f"Error Crítico: {e_gral}", "", "", "", "")

    # GUARDADO FINAL AL TERMINAR EL BUCLE (1 sola vez)
    print_log("Guardando archivo CSV definitivo...")
    try: df.to_csv(ruta_csv, index=False, sep=sep_sys, encoding='utf-8-sig')
    except Exception as e: print_log(f"Error al guardar CSV final: {e}")

    summary_callback(stats)
    print_log("\n--- FIN DEL SCRIPT ---")