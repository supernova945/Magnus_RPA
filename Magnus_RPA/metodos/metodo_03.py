import time
import winreg
from datetime import datetime

import pandas as pd

from metodos.sap_conexion import (
    abrir_caja_sap,
    conectar_sap_autologin,
    esperar_elemento,
    hay_internet,
    sap_str_to_float,
)


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


def extraer_operacion_de_texto(texto_sap):
    try:
        if not texto_sap:
            return ""
        fragmentos = texto_sap.strip().split(" ")
        ultimo_valor = fragmentos[-1]
        return ultimo_valor.lstrip("0")
    except:
        return ""


# ==============================================================================
# LÓGICA DE NAVEGACIÓN Y POSTEO (ADAPTADA PARA EL SALVADOR SV17)
# ==============================================================================
def ir_a_transaccion_y_cargar_cliente(
    session, id_cliente, dato_sociedad, sociedad_actual_sap
):
    try:
        if sociedad_actual_sap != dato_sociedad:
            abrir_caja_sap(session, dato_sociedad)
        else:
            try:
                session.findById("wnd[0]/tbar[1]/btn[13]").press()
                session.findById("wnd[0]/usr/tabsTABCONTROL/tabpTABBTN1").select()
            except:
                pass

        input_id = "wnd[0]/usr/tabsTABCONTROL/tabpTABBTN1/ssubWORK_SCREEN:/DBM/MT_TILL:2002/subWORKING_AREA:/DBM/MT_TILL:2004/ctxt/DBM/T_WA_SEARCH-PARTNER"
        esperar_elemento(session, input_id, timeout=3)
        session.findById(input_id).text = id_cliente
        session.findById(input_id).setFocus()
        session.findById("wnd[0]").sendVKey(0)
        esperar_elemento(
            session,
            "wnd[0]/usr/tabsTABCONTROL/tabpTABBTN1/ssubWORK_SCREEN:/DBM/MT_TILL:2002/subWORKING_AREA:/DBM/MT_TILL:2004/cntlOPEN_ITEM_CON/shellcont/shell",
            timeout=5,
        )
        return True
    except Exception:
        return False


def postear_pago_sv(
    session, filas_a_seleccionar, monto_a_pagar, datos_cabecera, es_factura=True
):
    try:
        grid_id = "wnd[0]/usr/tabsTABCONTROL/tabpTABBTN1/ssubWORK_SCREEN:/DBM/MT_TILL:2002/subWORKING_AREA:/DBM/MT_TILL:2004/cntlOPEN_ITEM_CON/shellcont/shell"
        grid = session.findById(grid_id)

        # 1. Seleccionar filas
        seleccion_str = ",".join(filas_a_seleccionar)
        if len(filas_a_seleccionar) > 1:
            filas_int = sorted([int(x) for x in filas_a_seleccionar])
            if filas_int == list(range(min(filas_int), max(filas_int) + 1)):
                grid.SelectedRows = f"{min(filas_int)}-{max(filas_int)}"
            else:
                grid.SelectedRows = seleccion_str
        else:
            grid.SelectedRows = seleccion_str

        # 2. Activar partidas (Botón Tratar)
        session.findById(
            "wnd[0]/usr/tabsTABCONTROL/tabpTABBTN1/ssubWORK_SCREEN:/DBM/MT_TILL:2002/subWORKING_AREA:/DBM/MT_TILL:2004/btnBT_HANDLE"
        ).press()
        base_pago = "wnd[0]/usr/tabsTABCONTROL/tabpTABBTN1/ssubWORK_SCREEN:/DBM/MT_TILL:2002/subWORKING_AREA:/DBM/MT_TILL:2004"
        esperar_elemento(
            session, f"{base_pago}/txt/DBM/T_WA_WORK_LINE-AM_GET", timeout=5
        )

        # 3. Llenar cabecera (Monto y Clase de pago)
        try:
            session.findById(
                f"{base_pago}/cmb/DBM/T_WA_WORK_LINE-PAYMENT_TYPE"
            ).key = datos_cabecera["clase_pago"]
        except:
            pass

        monto_str = str(round(float(monto_a_pagar), 2))
        session.findById(f"{base_pago}/txt/DBM/T_WA_WORK_LINE-AM_GET").text = monto_str

        session.findById(f"{base_pago}/cmb/DBM/T_WA_WORK_LINE-PAYMENT_TYPE").setFocus()
        session.findById("wnd[0]").sendVKey(0)
        time.sleep(1)

        # 4. PRIMER POPUP: Datos Adicionales (Efectivo SV17)
        if session.Children.Count > 1:
            popup_id = "wnd[1]/usr/sub:SAPLSPO4:0300"
            try:
                if es_factura:
                    # Pago 1: Concepto y Fecha
                    try:
                        session.findById(
                            f"{popup_id}/ctxtSVALD-VALUE[0,21]"
                        ).text = datos_cabecera["comentario"]
                    except:
                        pass
                    try:
                        session.findById(
                            f"{popup_id}/txtSVALD-VALUE[1,21]"
                        ).text = datos_cabecera["asesor"]
                    except:
                        pass
                else:
                    # Pago 2: Observaciones
                    try:
                        session.findById(
                            f"{popup_id}/txtSVALD-VALUE[3,21]"
                        ).text = datos_cabecera["asesor"]
                    except:
                        pass

                session.findById("wnd[1]/tbar[0]/btn[0]").press()
            except Exception:
                try:
                    session.findById("wnd[1]/tbar[0]/btn[0]").press()
                except:
                    pass

        # 5. Contabilizar (btn[5] en SV17)
        try:
            session.findById("wnd[0]/tbar[1]/btn[5]").press()
        except:
            session.findById("wnd[0]/tbar[1]/btn[17]").press()
        time.sleep(1)

        # 6. SEGUNDO POPUP: Serie y Recibo (Específico de SV17)
        if session.Children.Count > 1:
            popup_id2 = "wnd[1]/usr/sub:SAPLSPO4:0300"
            try:
                # Ponemos "1" y "1"
                try:
                    session.findById(f"{popup_id2}/txtSVALD-VALUE[0,21]").text = "1"
                except:
                    pass
                try:
                    session.findById(f"{popup_id2}/txtSVALD-VALUE[1,21]").text = "1"
                except:
                    pass

                session.findById("wnd[1]/tbar[0]/btn[0]").press()
            except Exception:
                try:
                    session.findById("wnd[1]/tbar[0]/btn[0]").press()
                except:
                    pass

        msg_out = "Exito (Sin msg)"

        # Manejo de Errores de SAP
        if session.Children.Count > 1:
            try:
                txt_error = session.findById("wnd[1]/usr/txtSPOP-TEXTLINE1").text
                if txt_error:
                    try:
                        session.findById("wnd[1]").sendVKey(0)
                    except:
                        pass
                    return False, f"Error SAP: {txt_error}"
            except:
                pass

        try:
            sbar = session.findById("wnd[0]/sbar/pane[0]").text
            if sbar:
                if (
                    "error" in sbar.lower()
                    or "incorrecto" in sbar.lower()
                    or "invalido" in sbar.lower()
                ):
                    return False, sbar
                else:
                    msg_out = sbar
        except:
            pass

        return True, msg_out

    except Exception as e:
        return False, str(e)


def contabilizar_cuenta_mayor_sv(session, datos, print_log):
    """
    Función que postea a cuenta de mayor (Pestaña 3).
    Se ha eliminado la orden de "Cerrar Caja" (btn[7]) a petición del usuario.
    """
    try:
        print_log("Navegando a pestaña 3 (Pago cuenta de mayor SV)...")
        session.findById("wnd[0]/usr/tabsTABCONTROL/tabpTABBTN3").select()
        time.sleep(0.5)

        base_work = (
            "wnd[0]/usr/tabsTABCONTROL/tabpTABBTN3/ssubWORK_SCREEN:/DBM/MT_TILL:2006"
        )

        # Tipo de Transacción (2151)
        busitrans = datos.get("nota_credito", "2151")
        if not busitrans or busitrans == "nan":
            busitrans = "2151"
        session.findById(f"{base_work}/cmb/DBM/T_WA_DOC_LINE-BUSITRANS").key = busitrans

        # Importe Total a Cortar
        session.findById(f"{base_work}/txt/DBM/T_WA_DOC_LINE-AMOUNT").text = datos[
            "monto_total"
        ]

        # Texto Contable
        fecha_hoy = datetime.now().strftime("%d.%m.%Y")
        session.findById(
            f"{base_work}/txt/DBM/T_WA_DOC_LINE-ITEM_TEXT"
        ).text = f"CORTE DE CAJA {fecha_hoy}"

        # Añadir Partida (ADD_POSS)
        session.findById(f"{base_work}/btnADD_POSS").press()
        time.sleep(1)

        # Clase Pago y Texto de Cabecera
        session.findById(
            f"{base_work}/cmb/DBM/T_WA_WORK_LINE-PAYMENT_TYPE"
        ).key = datos["clase_pago"]

        fecha_header = datetime.now().strftime("%d%m%Y")
        session.findById(
            f"{base_work}/txt/DBM/T_WA_WORK_LINE-HEADER_TXT"
        ).text = fecha_header
        session.findById(f"{base_work}/txt/DBM/T_WA_WORK_LINE-HEADER_TXT").setFocus()

        # Contabilizar el Corte (btn[5] en SV17)
        print_log("Contabilizando en cuenta de mayor SV...")
        try:
            session.findById("wnd[0]/tbar[1]/btn[5]").press()
        except:
            session.findById("wnd[0]/tbar[1]/btn[17]").press()
        time.sleep(1)

        # Confirmaciones de impresión/salida
        try:
            session.findById("wnd[1]/tbar[0]/btn[0]").press()
        except:
            pass
        try:
            session.findById("wnd[1]/tbar[0]/btn[0]").press()
        except:
            pass
        try:
            session.findById("wnd[1]/usr/btnBUTTON_1").press()
        except:
            pass

        try:
            mensaje_sap = session.findById("wnd[0]/sbar/pane[0]").text
            if not mensaje_sap:
                mensaje_sap = "Cuenta Mayor Contabilizada"
        except:
            mensaje_sap = "Cuenta Mayor Contabilizada (Sin leer barra)"

        print_log(f"Resultado Cuenta Mayor: {mensaje_sap}")
        return True, mensaje_sap

    except Exception as e:
        print_log(f"❌ Error Cuenta Mayor SV: {e}")
        return False, f"Error: {e}"


# ==============================================================================
# FUNCIÓN PRINCIPAL
# ==============================================================================
def ejecutar(
    ruta_excel,
    log_callback,
    check_stop,
    progress_callback,
    summary_callback,
    tabla_callback=None,
    silencioso=False,
    detallado=False,
):
    def print_log(msg):
        log_callback(str(msg))

    stats = {"ok": 0, "omitidos": 0, "errores": 0, "monto": 0.0}

    if not hay_internet():
        print_log("❌ Error crítico: Se requiere conexión a Internet para iniciar.")
        stats["abortado_red"] = True
        summary_callback(stats)
        return

    sap_user = "DESCONOCIDO"
    try:
        session = conectar_sap_autologin()
        print_log("--- INICIANDO SCRIPT DE COBROS (MÉTODO 3 SV) ---")
        try:
            sap_user = session.Info.User
        except:
            pass
    except Exception as e:
        print_log(f"ERROR CRÍTICO: {e}")
        summary_callback(stats)
        return

    marca_tiempo = datetime.now().strftime("%d.%m.%Y_%H%M%S")
    ruta_csv = ruta_excel.replace(".xlsx", f"_resultados_sv_{marca_tiempo}.csv")
    sep_sys = obtener_separador_sistema()

    try:
        if ruta_excel.endswith(".csv"):
            try:
                df = pd.read_csv(ruta_excel, sep=";", dtype=str, encoding="utf-8-sig")
            except:
                df = pd.read_csv(ruta_excel, sep=",", dtype=str, encoding="utf-8-sig")
            df.replace(to_replace=["nan", "NaN"], value="", inplace=True)
            df.fillna("", inplace=True)
        else:
            df = pd.read_excel(ruta_excel, header=0, dtype=str)

        columnas_finales = [
            "sociedad",
            "id_cliente",
            "fecha_documento",
            "monto_total",
            "clase_pago",
            "comentario",
            "asesor",
            "nota_credito",
            "usuario_sap",
            "fecha",
            "hora",
            "resultado_01",
            "resultado_02",
        ]
        for i in range(1, 11):
            columnas_finales.append(f"cobro_{i:02d}")

        for col in columnas_finales:
            if col not in df.columns:
                df[col] = ""

        df = df[columnas_finales]
        total_filas = len(df)
        print_log(f"Registros cargados: {total_filas}")
    except Exception as e:
        print_log(f"Error Excel: {e}")
        summary_callback(stats)
        return

    SOCIEDAD_SV = "SV17"
    CLASE_PAGO_SV = "01"

    sociedad_actual_sap = None

    # --- VARIABLES PARA EL CORTE GLOBAL ---
    gran_total_cierre = 0.0
    cierre_clase_pago = CLASE_PAGO_SV
    cierre_nota_credito = "2151"

    for index, row in df.iterrows():
        try:
            if not hay_internet(timeout=1):
                raise Exception("com_error_preventivo: Desconexión de red detectada.")

            porcentaje = (index + 1) / total_filas
            progress_callback(porcentaje)

            if check_stop():
                print_log("[!!!] DETENIDO POR USUARIO")
                break

            txt_res_facturas = ""
            txt_res_capital = ""
            capital_pagado_monto = 0.0

            ya_procesado_1 = str(row["resultado_01"]).strip() not in ["", "nan"]
            ya_procesado_2 = str(row["resultado_02"]).strip() not in ["", "nan"]

            if ya_procesado_1 or ya_procesado_2:
                stats["omitidos"] += 1
                continue

            id_cliente = str(row["id_cliente"]).replace(".0", "").strip()
            if not id_cliente or id_cliente.lower() == "nan":
                stats["omitidos"] += 1
                if tabla_callback:
                    tabla_callback(
                        datetime.now().strftime("%H:%M:%S"),
                        "SIN CLIENTE",
                        "-",
                        "Omitido: Datos faltantes",
                        SOCIEDAD_SV,
                        CLASE_PAGO_SV,
                        "N/A",
                        "",
                    )
                continue

            try:
                monto_inicial = float(str(row["monto_total"]).replace(",", ""))
            except:
                monto_inicial = 0.0
            monto_disponible = monto_inicial

            datos_cabecera = {
                "clase_pago": str(row["clase_pago"]).strip().zfill(2)
                if str(row["clase_pago"]).strip() != "nan"
                else CLASE_PAGO_SV,
                "comentario": str(row["comentario"])
                .strip()
                .replace("nan", "COBRO PAGARE"),
                "asesor": str(row["asesor"]).strip().replace("nan", "PX 22.09.2026"),
                "nota_credito": str(row["nota_credito"]).strip().replace("nan", "2151"),
            }

            if detallado:
                print_log(
                    f"[{index + 1}] Cte: {id_cliente} | Disp: {monto_disponible} | Ref: {datos_cabecera['comentario']}"
                )

            # ==================================================================
            # FASE 1: PRIMER PAGO (Facturas / 00MS)
            # ==================================================================
            facturas_pagadas_monto = 0.0
            if ir_a_transaccion_y_cargar_cliente(
                session, id_cliente, SOCIEDAD_SV, sociedad_actual_sap
            ):
                sociedad_actual_sap = SOCIEDAD_SV
                grid = session.findById(
                    "wnd[0]/usr/tabsTABCONTROL/tabpTABBTN1/ssubWORK_SCREEN:/DBM/MT_TILL:2002/subWORKING_AREA:/DBM/MT_TILL:2004/cntlOPEN_ITEM_CON/shellcont/shell"
                )

                lista_facturas = []
                if grid.RowCount > 0:
                    for r in range(grid.RowCount):
                        doc_sap = str(grid.GetCellValue(r, "BELNR")).strip()

                        try:
                            cpag = str(grid.GetCellValue(r, "ZTERM")).strip().upper()
                        except:
                            cpag = ""

                        # CRITERIO EL SALVADOR: Es factura si CPag es "00MS" o el doc empieza con 54 o 97
                        if (
                            cpag == "00MS"
                            or doc_sap.startswith("54")
                            or doc_sap.startswith("97")
                        ):
                            importe = sap_str_to_float(grid.GetCellValue(r, "DMBTR"))
                            lista_facturas.append(
                                {"fila": str(r), "monto": importe, "doc_sap": doc_sap}
                            )

                total_facturas = sum(f["monto"] for f in lista_facturas)

                if total_facturas > 0 and monto_disponible >= (total_facturas - 0.01):
                    if detallado:
                        print_log(
                            f"   -> Pagando Primer Registro (00MS): Q.{total_facturas}"
                        )
                    filas_fact = [f["fila"] for f in lista_facturas]

                    exito, msg = postear_pago_sv(
                        session,
                        filas_fact,
                        total_facturas,
                        datos_cabecera,
                        es_factura=True,
                    )

                    if exito:
                        facturas_pagadas_monto = total_facturas
                        monto_disponible -= total_facturas
                        txt_res_facturas = f"Pago 1 OK ({total_facturas})"
                        stats["monto"] += total_facturas
                    else:
                        txt_res_facturas = f"Err Pago 1: {msg}"
                else:
                    if total_facturas > 0:
                        txt_res_facturas = "Saldo insuficiente"
                        monto_disponible = 0

            # ==================================================================
            # FASE 2: SEGUNDO PAGO (Capital / Restante)
            # ==================================================================
            if monto_disponible > 0.01:
                if facturas_pagadas_monto > 0:
                    if ir_a_transaccion_y_cargar_cliente(
                        session, id_cliente, SOCIEDAD_SV, sociedad_actual_sap
                    ):
                        sociedad_actual_sap = SOCIEDAD_SV

                grid = session.findById(
                    "wnd[0]/usr/tabsTABCONTROL/tabpTABBTN1/ssubWORK_SCREEN:/DBM/MT_TILL:2002/subWORKING_AREA:/DBM/MT_TILL:2004/cntlOPEN_ITEM_CON/shellcont/shell"
                )

                lista_capital = []
                if grid.RowCount > 0:
                    for r in range(grid.RowCount):
                        doc_sap = str(grid.GetCellValue(r, "BELNR")).strip()

                        try:
                            cpag = str(grid.GetCellValue(r, "ZTERM")).strip().upper()
                        except:
                            cpag = ""

                        # CRITERIO EL SALVADOR: Procesamos el resto (Lo que NO sea 00MS ni empiece con 54)
                        if (
                            cpag != "00MS"
                            and not doc_sap.startswith("54")
                            and not doc_sap.startswith("97")
                        ):
                            importe = sap_str_to_float(grid.GetCellValue(r, "DMBTR"))
                            lista_capital.append(
                                {"fila": r, "monto": importe, "doc_sap": doc_sap}
                            )

                    filas_a_pagar = []
                    monto_a_procesar_cap = 0.0
                    temp_disponible = monto_disponible

                    for item in lista_capital:
                        if temp_disponible > 0.01:
                            pagar = round(min(item["monto"], temp_disponible), 2)
                            filas_a_pagar.append(str(item["fila"]))
                            monto_a_procesar_cap = round(
                                monto_a_procesar_cap + pagar, 2
                            )
                            temp_disponible = round(temp_disponible - pagar, 2)
                        else:
                            break

                    if filas_a_pagar:
                        if detallado:
                            print_log(
                                f"   -> Pagando Restante (Capital): Q.{monto_a_procesar_cap}"
                            )
                        exito, msg = postear_pago_sv(
                            session,
                            filas_a_pagar,
                            monto_a_procesar_cap,
                            datos_cabecera,
                            es_factura=False,
                        )
                        if exito:
                            txt_res_capital = f"Pago 2 OK ({monto_a_procesar_cap})"
                            stats["monto"] += monto_a_procesar_cap
                            capital_pagado_monto = monto_a_procesar_cap
                        else:
                            txt_res_capital = f"Err Pago 2: {msg}"
                    else:
                        txt_res_capital = "Sin registros restantes"
                else:
                    txt_res_capital = "Grid Vacio"

            # --- ACUMULAR PARA LA CUENTA DE MAYOR FINAL ---
            monto_total_cobrado = facturas_pagadas_monto + capital_pagado_monto
            txt_cierre = ""
            if monto_total_cobrado > 0:
                gran_total_cierre += monto_total_cobrado
                cierre_clase_pago = datos_cabecera["clase_pago"]
                cierre_nota_credito = datos_cabecera["nota_credito"]
                txt_cierre = "En espera de contab. mayor"

            # --- ESCRITURA EN EXCEL DE ESTA FILA ---
            df.at[index, "fecha"] = datetime.now().strftime("%d.%m.%Y")
            df.at[index, "hora"] = datetime.now().strftime("%H:%M:%S")
            df.at[index, "usuario_sap"] = sap_user

            txt_res_facturas = "N/A" if not txt_res_facturas else txt_res_facturas
            txt_res_capital = "N/A" if not txt_res_capital else txt_res_capital

            res_01 = f"1: {txt_res_facturas} | 2: {txt_res_capital}".strip(" | ")
            res_02 = txt_cierre

            # Guardamos los resultados
            df.at[index, "resultado_01"] = res_01
            df.at[index, "resultado_02"] = res_02

            # EVALUACIÓN DE LAS MÉTRICAS DE ÉXITO O ERROR (Ignorando la "Espera")
            estado_visual = res_01
            if "err " in estado_visual.lower() or "error" in estado_visual.lower():
                stats["errores"] += 1
            else:
                stats["ok"] += 1

            if tabla_callback:
                tabla_callback(
                    datetime.now().strftime("%H:%M:%S"),
                    id_cliente,
                    str(row.get("asesor", "")),
                    estado_visual,
                    SOCIEDAD_SV,
                    CLASE_PAGO_SV,
                    "N/A",
                    datos_cabecera["fecha_doc"],
                )

        except Exception as e_gral:
            err_msg = str(e_gral).lower()
            if "com_error" in err_msg or "desconect" in err_msg:
                df.at[index, "resultado_01"] = "⚠️ Caída de Red"
                stats["errores"] += 1
                time.sleep(5)
                try:
                    session = conectar_sap_autologin()
                    sociedad_actual_sap = None
                    continue
                except:
                    break
            else:
                df.at[index, "resultado_01"] = f"Error: {e_gral}"
                stats["errores"] += 1

    # ==================================================================
    # CONTABILIZACIÓN A CUENTA DE MAYOR FINAL (POR EL GRAN TOTAL ACUMULADO)
    # ==================================================================
    if gran_total_cierre > 0 and not check_stop():
        gran_total_cierre = round(gran_total_cierre, 2)
        print_log(
            f"--- EJECUTANDO CONTABILIZACIÓN A CUENTA DE MAYOR POR GRAN TOTAL: Q.{gran_total_cierre} ---"
        )

        datos_cuenta_mayor = {
            "monto_total": str(gran_total_cierre),
            "clase_pago": cierre_clase_pago,
            "nota_credito": cierre_nota_credito,
        }

        cierre_ok, msj_cierre = contabilizar_cuenta_mayor_sv(
            session, datos_cuenta_mayor, print_log
        )
        resultado_cierre_global = (
            f"Cuenta Mayor OK: {msj_cierre}"
            if cierre_ok
            else f"Err Mayor: {msj_cierre}"
        )

        # Actualizamos masivamente el Excel de los clientes que estaban en espera
        df["resultado_02"] = df["resultado_02"].replace(
            "En espera de contab. mayor", resultado_cierre_global
        )

    print_log("Guardando archivo CSV definitivo...")
    try:
        df.to_csv(ruta_csv, index=False, sep=sep_sys, encoding="utf-8-sig")
    except Exception as e:
        print_log(f"Error al guardar CSV final: {e}")

    stats["transacciones_detalle"] = df.to_dict(orient="records")
    summary_callback(stats)
    print_log("--- FIN DEL SCRIPT ---")
