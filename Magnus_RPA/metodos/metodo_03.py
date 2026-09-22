import winreg
from datetime import datetime

import pandas as pd

from metodos.sap_conexion import (
    abrir_caja_sap,
    conectar_sap_autologin,
    esperar_elemento,
    hay_internet,
    log_matriz_sap,
    sap_str_to_float,
)


GRID_PARTIDAS_ID = (
    "wnd[0]/usr/tabsTABCONTROL/tabpTABBTN1/ssubWORK_SCREEN:/DBM/MT_TILL:2002/"
    "subWORKING_AREA:/DBM/MT_TILL:2004/cntlOPEN_ITEM_CON/shellcont/shell"
)

CAMPO_CLIENTE_ID = (
    "wnd[0]/usr/tabsTABCONTROL/tabpTABBTN1/ssubWORK_SCREEN:/DBM/MT_TILL:2002/"
    "subWORKING_AREA:/DBM/MT_TILL:2004/ctxt/DBM/T_WA_SEARCH-PARTNER"
)


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


def limpiar_codigo(valor, default=""):
    valor_str = str(valor).replace(".0", "").strip()
    if valor_str.lower() == "nan":
        return default
    return valor_str or default


def limpiar_referencia(valor):
    valor_str = limpiar_codigo(valor)
    return " ".join(valor_str.upper().split())


def resultado_ya_procesado(valor):
    valor_str = str(valor).strip()
    valor_low = valor_str.lower()
    if valor_low in ("", "nan"):
        return False
    if "pendiente mapeo sap sv17" in valor_low:
        return False
    if "exito simulado sv17" in valor_low:
        return False
    return True


def cargar_cliente_en_caja(session, id_cliente):
    if not esperar_elemento(session, CAMPO_CLIENTE_ID, timeout=5):
        raise Exception("No se encontró el campo Cliente en la caja SV17.")

    session.findById(CAMPO_CLIENTE_ID).text = id_cliente
    session.findById(CAMPO_CLIENTE_ID).setFocus()
    session.findById("wnd[0]").sendVKey(0)

    if not esperar_elemento(session, GRID_PARTIDAS_ID, timeout=10):
        raise Exception("No cargó el grid de partidas para el cliente SV17.")

    return session.findById(GRID_PARTIDAS_ID)


def analizar_partidas_sv(grid, referencia):
    referencia_clean = limpiar_referencia(referencia)
    partidas = []

    for fila in range(grid.RowCount):
        try:
            doc_sap = str(grid.GetCellValue(fila, "BELNR")).strip()
        except:
            doc_sap = ""

        try:
            ref_sap = str(grid.GetCellValue(fila, "XBLNR")).strip()
        except:
            ref_sap = ""

        try:
            texto_sap = str(grid.GetCellValue(fila, "SGTXT")).strip()
        except:
            texto_sap = ""

        try:
            monto = sap_str_to_float(grid.GetCellValue(fila, "DMBTR"))
        except:
            monto = 0.0

        ref_texto = limpiar_referencia(f"{ref_sap} {texto_sap}")
        coincide = bool(referencia_clean and referencia_clean in ref_texto)
        if coincide:
            partidas.append(
                {
                    "fila": fila,
                    "doc_sap": doc_sap,
                    "monto": monto,
                    "referencia": ref_sap,
                    "texto": texto_sap,
                }
            )

    return partidas


# ==============================================================================
# FUNCIÓN PRINCIPAL MÉTODO 3 - EL SALVADOR
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

    print_log("--- INICIANDO SCRIPT DE COBROS (MÉTODO 3 - SV17) ---")

    marca_tiempo = datetime.now().strftime("%d.%m.%Y_%H%M%S")
    ruta_csv = ruta_excel.replace(".xlsx", f"_resultados_sv_{marca_tiempo}.csv")
    sep_sys = obtener_separador_sistema()

    stats = {"ok": 0, "omitidos": 0, "errores": 0, "monto": 0.0}

    # 1. CONEXIÓN SAP CON AUTO-LOGIN
    if not hay_internet():
        print_log("❌ Error crítico: Se requiere conexión a Internet para iniciar.")
        stats["abortado_red"] = True
        stats["errores"] += 1
        summary_callback(stats)
        return

    sap_user = "DESCONOCIDO"
    try:
        session = conectar_sap_autologin()
        try:
            sap_user = session.Info.User
        except:
            pass
    except Exception as e:
        print_log(f"ERROR CRÍTICO: {e}")
        stats["errores"] += 1
        stats["error_critico"] = str(e)
        summary_callback(stats)
        return

    # 2. LEER EXCEL
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
        # Agregamos las columnas de cobros como en método 2
        for i in range(1, 11):
            columnas_finales.append(f"cobro_{i:02d}")

        for col in columnas_finales:
            if col not in df.columns:
                df[col] = ""

        df = df[columnas_finales]
        total_filas = len(df)
        print_log(f"Registros cargados para El Salvador: {total_filas}")
    except Exception as e:
        print_log(f"Error Excel: {e}")
        stats["errores"] += 1
        stats["error_critico"] = str(e)
        summary_callback(stats)
        return

    # CONFIGURACIONES BASE DE EL SALVADOR
    SOCIEDAD_SV_DEFAULT = "SV17"
    CLASE_PAGO_SV_DEFAULT = "1"
    ESTADO_PENDIENTE_MAPEO = (
        "Omitido: Pendiente mapeo SAP SV17: falta registrar el flujo real de caja"
    )

    sociedad_actual_sap = None
    for index, row in df.iterrows():
        try:
            if not hay_internet(timeout=1):
                raise Exception("Desconexión de red detectada.")

            progress_callback((index + 1) / total_filas)
            if check_stop():
                break

            if resultado_ya_procesado(row["resultado_01"]):
                stats["omitidos"] += 1
                continue

            dato_sociedad = limpiar_codigo(row["sociedad"], SOCIEDAD_SV_DEFAULT).upper()
            dato_clase_pago = limpiar_codigo(
                row["clase_pago"], CLASE_PAGO_SV_DEFAULT
            ).zfill(1)

            id_cliente = limpiar_codigo(row["id_cliente"])
            if not id_cliente or id_cliente.lower() == "nan":
                stats["omitidos"] += 1
                if tabla_callback:
                    tabla_callback(
                        datetime.now().strftime("%H:%M:%S"),
                        "SIN CLIENTE",
                        "-",
                        "Omitido: Sin Cliente",
                        dato_sociedad,
                        dato_clase_pago,
                        "N/A",
                        "",
                    )
                continue

            # Extraer Datos
            try:
                monto_disponible = float(str(row["monto_total"]).replace(",", ""))
            except:
                monto_disponible = 0.0

            dato_referencia = str(row["comentario"]).replace(".0", "").strip()
            fecha_doc = limpiar_fecha(row["fecha_documento"]).replace("nan", "")

            print_log(
                f"[{index + 1}/{total_filas}] Cte: {id_cliente} | Monto: {monto_disponible}"
            )

            # ==================================================================
            # LÓGICA SAP (Adaptar para SV)
            # ==================================================================

            estado_actual = ""

            if sociedad_actual_sap != dato_sociedad:
                abrir_caja_sap(session, dato_sociedad, print_log)
                sociedad_actual_sap = dato_sociedad
            else:
                try:
                    session.findById("wnd[0]/tbar[1]/btn[13]").press()  # Botón Crear
                    session.findById("wnd[0]/usr/tabsTABCONTROL/tabpTABBTN1").select()
                except:
                    pass

            grid = cargar_cliente_en_caja(session, id_cliente)
            partidas_candidatas = analizar_partidas_sv(grid, dato_referencia)
            docs_candidatos = [p["doc_sap"] for p in partidas_candidatas]
            log_matriz_sap(session, GRID_PARTIDAS_ID, print_log, docs_candidatos)

            total_candidato = round(sum(p["monto"] for p in partidas_candidatas), 2)
            if partidas_candidatas:
                print_log(
                    "   [SV17] Partidas candidatas por comentario "
                    f"'{dato_referencia}': {len(partidas_candidatas)} | "
                    f"Total detectado: {total_candidato}"
                )
            else:
                print_log(
                    "   [SV17] No se detectaron partidas que coincidan con el "
                    f"comentario '{dato_referencia}'."
                )

            # ----------------------------------------------------
            # Pendiente: adaptar el posteo real de SV17 cuando se
            # tenga la grabación/capturas del flujo de caja de El Salvador.
            # No se marca como OK para evitar contabilizar cobros ficticios.
            # ----------------------------------------------------
            estado_actual = (
                f"{ESTADO_PENDIENTE_MAPEO} | "
                f"Partidas candidatas: {len(partidas_candidatas)} | "
                f"Total candidato: {total_candidato}"
            )
            stats["omitidos"] += 1

            # Guardado en tabla del UI y Excel
            df.at[index, "resultado_01"] = estado_actual
            df.at[index, "fecha"] = datetime.now().strftime("%d.%m.%Y")
            df.at[index, "hora"] = datetime.now().strftime("%H:%M:%S")
            df.at[index, "usuario_sap"] = sap_user

            if tabla_callback:
                tabla_callback(
                    datetime.now().strftime("%H:%M:%S"),
                    id_cliente,
                    row["asesor"],
                    estado_actual,
                    dato_sociedad,
                    dato_clase_pago,
                    "N/A",
                    fecha_doc,
                )

            try:
                df.to_csv(ruta_csv, index=False, sep=sep_sys, encoding="utf-8-sig")
            except:
                pass

        except Exception as e:
            print_log(f"Error Fila {index}: {e}")
            df.at[index, "resultado_01"] = f"Error: {e}"
            stats["errores"] += 1

    print_log("Guardando archivo CSV definitivo...")
    try:
        df.to_csv(ruta_csv, index=False, sep=sep_sys, encoding="utf-8-sig")
    except:
        pass

    stats["transacciones_detalle"] = df.to_dict(orient="records")
    summary_callback(stats)
    print_log("--- FIN MÉTODO 3 ---")
