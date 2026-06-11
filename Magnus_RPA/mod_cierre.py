import time

# ==============================================================================
# CATÁLOGO DE EQUIVALENCIAS (INCLUYE SOCIEDAD)
# ==============================================================================
CATALOGO_CUENTAS = [
    {"sociedad": "GT09", "cuenta_excel": "74655", "clase": "9I", "id_sap": "00265"},
    {"sociedad": "GT09", "cuenta_excel": "74655", "clase": "07", "id_sap": "00365"},
    {"sociedad": "GT09", "cuenta_excel": "4041",  "clase": "9I", "id_sap": "0076"},
    {"sociedad": "GT09", "cuenta_excel": "4041",  "clase": "07", "id_sap": "0176"},
    {"sociedad": "GT09", "cuenta_excel": "21937", "clase": "9I", "id_sap": "4394"},
    {"sociedad": "GT09", "cuenta_excel": "21937", "clase": "07", "id_sap": "4395"},
    {"sociedad": "GT09", "cuenta_excel": "0813",  "clase": "9I", "id_sap": "0078"},
    {"sociedad": "GT09", "cuenta_excel": "0813",  "clase": "07", "id_sap": "0178"},
    
    {"sociedad": "GT03", "cuenta_excel": "6259",  "clase": "9I", "id_sap": "0032"},
    {"sociedad": "GT03", "cuenta_excel": "6259",  "clase": "07", "id_sap": "0132"},
    {"sociedad": "GT03", "cuenta_excel": "64723", "clase": "9I", "id_sap": "4396"},
    {"sociedad": "GT03", "cuenta_excel": "64723", "clase": "07", "id_sap": "4397"},
    {"sociedad": "GT03", "cuenta_excel": "76148", "clase": "9I", "id_sap": "00274"},
    {"sociedad": "GT03", "cuenta_excel": "76148", "clase": "07", "id_sap": "00374"},
    {"sociedad": "GT03", "cuenta_excel": "9507",  "clase": "9I", "id_sap": "0095"},
    {"sociedad": "GT03", "cuenta_excel": "9507",  "clase": "07", "id_sap": "0195"}
]

def buscar_id_cuenta(sociedad_excel, cuenta_banco_excel, clase_pago_excel):
    soc_str = str(sociedad_excel).strip().upper()
    cta_str = str(cuenta_banco_excel).strip().upper()
    pag_str = str(clase_pago_excel).strip().upper()
    if pag_str == "7": pag_str = "07"

    for fila in CATALOGO_CUENTAS:
        if fila["sociedad"] == soc_str and fila["cuenta_excel"] == cta_str and fila["clase"] == pag_str:
            return fila["id_sap"]
    return cta_str 

def obtener_datos_sesion(session):
    try:
        id_texto = "/app/con[0]/ses[0]/wnd[0]/usr/subINFO_SCREEN:/DBM/MT_TILL:2001/cntlSESSION_CON/shellcont/shell"
        texto_crudo = session.findById(id_texto).text
        lineas = texto_crudo.replace('\r', '\n').split('\n')
        
        val_caja = "CAJA_NO_ENCONTRADA"
        val_sesion = "SESION_NO_ENCONTRADA"
        
        for linea in lineas:
            linea_limpia = linea.strip()
            if linea_limpia.startswith("Caja"):
                val_caja = linea_limpia.replace("Caja", "").strip()
            elif linea_limpia.startswith("Sesión") or linea_limpia.startswith("Sesion"):
                val_sesion = linea_limpia.replace("Sesión", "").replace("Sesion", "").strip()
                
        return f"{val_caja} SESION# {val_sesion}"
    except Exception as e:
        return f"Error Extracción: {e}"

def ejecutar_cierre(session, datos, log_callback):
    """
    Recibe el diccionario 'datos' y postea el cierre. Retorna (True/False, Mensaje_SAP).
    """
    def print_log(msg):
        if log_callback: log_callback(f"   [CIERRE] {msg}")

    try:
        print_log("Navegando a pestaña 3 (Pago cuenta de mayor)...")
        session.findById("wnd[0]/usr/tabsTABCONTROL/tabpTABBTN3").select()
        time.sleep(0.5)

        base_work = "wnd[0]/usr/tabsTABCONTROL/tabpTABBTN3/ssubWORK_SCREEN:/DBM/MT_TILL:2006"
        
        # 1. Banco (Cruce Triple)
        id_cuenta_sap = buscar_id_cuenta(datos['sociedad'], datos['cuenta_banco'], datos['clase_pago'])
        try: session.findById(f"{base_work}/cmb/DBM/T_WA_DOC_LINE-BUSITRANS").key = id_cuenta_sap
        except Exception as e: print_log(f"Aviso en Banco: ID {id_cuenta_sap} no encajó perfecto.")
        
        # 2. Importe
        session.findById(f"{base_work}/txt/DBM/T_WA_DOC_LINE-AMOUNT").text = datos['monto_total']
        
        # 3. Texto Contable
        texto_sesion = obtener_datos_sesion(session)
        session.findById(f"{base_work}/txt/DBM/T_WA_DOC_LINE-ITEM_TEXT").text = texto_sesion
        
        # 4. Añadir
        session.findById(f"{base_work}/btnADD_POSS").press()
        time.sleep(1)
        
        # 5. Clase Pago
        session.findById(f"{base_work}/cmb/DBM/T_WA_WORK_LINE-PAYMENT_TYPE").key = str(datos['clase_pago']).zfill(2)
        
        # 6. Header (No. Doc)
        session.findById(f"{base_work}/txt/DBM/T_WA_WORK_LINE-HEADER_TXT").text = datos['no_doc_deposito']
        session.findById(f"{base_work}/txt/DBM/T_WA_WORK_LINE-HEADER_TXT").setFocus()
        session.findById("wnd[0]").sendVKey(0)
        
        # 7. Contabilizar Cierre
        print_log("Contabilizando cierre...")
        session.findById("wnd[0]/tbar[1]/btn[17]").press()
        time.sleep(1.5)
        
        try:
            mensaje_sap = session.findById("wnd[0]/sbar/pane[0]").text
            if not mensaje_sap: mensaje_sap = "Contabilizado (Sin leer barra)"
        except:
            mensaje_sap = "Contabilizado (Sin leer barra)"
            
        print_log(f"Resultado: {mensaje_sap}")
        return True, mensaje_sap
        
    except Exception as e:
        print_log(f"❌ Error crítico: {e}")
        return False, f"Error Cierre: {e}"