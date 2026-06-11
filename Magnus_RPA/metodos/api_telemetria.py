import requests
import msal
from datetime import datetime
import json
import socket
import os

def obtener_token_dataverse(tenant_id, client_id, client_secret, env_url):
    """Obtiene el token de acceso desde Microsoft Entra ID para Dataverse"""
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    app = msal.ConfidentialClientApplication(
        client_id, authority=authority, client_credential=client_secret
    )
    # Scope: environment url with trailing slash
    clean_env_url = env_url.rstrip('/')
    scopes = [f"{clean_env_url}/.default"]
    result = app.acquire_token_for_client(scopes=scopes)
    
    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception(f"Error MSAL Dataverse: {result.get('error_description', result.get('error'))}")

def enviar_telemetria_dataverse(config_remoto, operador, version, stats, lista_transacciones, json_contexto):
    """Envío de lote multi-agente hacia esquema Dataverse"""
    try:
        tenant = config_remoto.get("azure_tenant_id")
        client_id = config_remoto.get("azure_client_id")
        secret = config_remoto.get("azure_client_secret")
        env_url = config_remoto.get("dataverse_url")
        prefix = config_remoto.get("dataverse_prefix")
        
        if not all([tenant, client_id, secret, env_url, prefix]):
            return False, "Faltan datos core (tenant/client/secret/env/prefix) en config_remoto"

        # Sanear URL y auth
        clean_env_url = env_url.rstrip('/')
        token = obtener_token_dataverse(tenant, client_id, secret, clean_env_url)
        api_base = f"{clean_env_url}/api/data/v9.2"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "OData-MaxVersion": "4.0",
            "OData-Version": "4.0",
            "Accept": "application/json"
        }
        
        info_ejec = json_contexto.get("ejecucion_info", {})
        ahora = datetime.now()
        id_lote = f"{ahora.strftime('%Y%m%d-%H%M%S')}-{operador}"
        
        exitosos = int(stats.get("ok", 0))
        errores = int(stats.get("errores", 0))
        omitidos = int(stats.get("omitidos", 0))
        total_filas = exitosos + errores + omitidos
        monto_tot = float(stats.get("monto", 0.0))
        
        tasa_exito = 0.0
        if (exitosos + errores) > 0:
            tasa_exito = (exitosos / (exitosos + errores)) * 100
        
        # Calcular duración
        str_inicio = info_ejec.get("hora_inicio", "00:00:00")
        try:
            h_ini = datetime.strptime(str_inicio, "%H:%M:%S")
            h_fin = datetime.strptime(ahora.strftime("%H:%M:%S"), "%H:%M:%S")
            duracion_segs = int((h_fin - h_ini).total_seconds())
            if duracion_segs < 0: duracion_segs = 1
        except:
            duracion_segs = 1
            
        vel_promedio = 0.0
        if total_filas > 0:
            vel_promedio = duracion_segs / total_filas

        operador_win = os.getlogin() if hasattr(os, 'getlogin') else 'desconocido'
        hostname = socket.gethostname()
        modo_silencioso = bool(info_ejec.get("silencioso", False))
        
        # Mapeo a Fechas Reales para OData (ISO-8601 Z)
        str_hoy = ahora.strftime("%Y-%m-%d")
        
        try:
            h_ini_raw = str(info_ejec.get("hora_inicio", ahora.strftime("%H:%M:%S")))
            h_fin_dt = datetime.strptime(f"{str_hoy} {h_ini_raw}", "%Y-%m-%d %H:%M:%S")
            odata_fecha_inicio = h_fin_dt.isoformat() + "Z"
        except:
            odata_fecha_inicio = ahora.isoformat() + "Z"
            
        odata_fecha_fin = ahora.isoformat() + "Z"

        # 1. EJECUCIÓN MAESTRA
        payload_maestro = {
            f"{prefix}id_lote": id_lote,
            f"{prefix}fecha_inicio": odata_fecha_inicio,
            f"{prefix}fecha_fin": odata_fecha_fin,
            f"{prefix}duracion_segundos": duracion_segs,
            f"{prefix}operador": operador,
            f"{prefix}operador_windows": operador_win,
            f"{prefix}hostname": hostname,
            f"{prefix}version_agente": version,
            f"{prefix}metodo_utilizado": int(info_ejec.get("metodo_detectado", 0)),
            f"{prefix}archivo_procesado": str(info_ejec.get("archivo_procesado", ""))[-50:], # Trunc
            f"{prefix}total_filas": total_filas,
            f"{prefix}exitosos": exitosos,
            f"{prefix}errores": errores,
            f"{prefix}omitidos": omitidos,
            f"{prefix}monto_total": monto_tot,
            f"{prefix}tipo_finalizacion": "COMPLETADO",
            f"{prefix}modo_silencioso": str(modo_silencioso),
            f"{prefix}registro_detallado": "True",
            f"{prefix}tasa_exito": float(tasa_exito),
            f"{prefix}velocidad_promedio": float(vel_promedio)
        }
        
        # Test pluralización de Dataverse
        tabla_ejec = f"{prefix}magnus_ejecuciones"
        res_ejec = requests.post(f"{api_base}/{tabla_ejec}", json=payload_maestro, headers=headers, timeout=15)
        if res_ejec.status_code == 404:
            tabla_ejec = f"{prefix}magnus_ejecucioneses"
            res_ejec = requests.post(f"{api_base}/{tabla_ejec}", json=payload_maestro, headers=headers, timeout=15)
            
        if res_ejec.status_code not in (200, 201, 204):
            print(f"Error Creado Maestro DW: {res_ejec.text}")
            return False, f"Error Creado Maestro DW: {res_ejec.text}"

        try:
            ejecucion_id = res_ejec.headers.get("OData-EntityId", "").split("(")[1].replace(")", "")
        except:
            ejecucion_id = None


        # 2. TRANSACCIONES
        session = requests.Session()
        session.headers.update(headers)
        
        tabla_trans = f"{prefix}magnus_transacciones"
        tabla_err = f"{prefix}magnus_errores"
        if session.get(f"{api_base}/{tabla_trans}?$top=1").status_code == 404:
            tabla_trans = f"{prefix}magnus_transaccioneses"
            tabla_err = f"{prefix}magnus_erroreses"
            
        for i, t in enumerate(lista_transacciones):
            monto_crudo = str(t.get("monto_total", "0")).replace(",", "").strip()
            if not monto_crudo: monto_crudo = "0"
            try: monto_limpio = float(monto_crudo)
            except: monto_limpio = 0.0

            res_status = str(t.get("resultado", "OMITIDO"))
            msg_res = str(t.get("observaciones", "OK"))[:400]

            # Bind de llave foránea (LookUp). Si Dataverse lo rechaza por falta de relación, solo omitimos
            payload_trans = {
                f"{prefix}id_lote": id_lote,
                f"{prefix}numero_fila": i + 1,
                f"{prefix}sociedad": str(t.get("sociedad", ""))[:10],
                f"{prefix}id_cliente": str(t.get("id_cliente", ""))[:20],
                f"{prefix}no_doc": str(t.get("no_doc", ""))[:30],
                f"{prefix}monto": monto_limpio,
                f"{prefix}clase_pago": str(t.get("clase_pago", ""))[:10],
                f"{prefix}cuenta_banco": str(t.get("cuenta_banco", ""))[:30],
                f"{prefix}fecha_deposito": str(t.get("fecha_deposito", ""))[:20],
                f"{prefix}txt_cab_doc": str(t.get("txt_cab_doc", ""))[:100],
                f"{prefix}no_boleta": str(t.get("no_boleta", ""))[:30],
                f"{prefix}concepto": str(t.get("concepto", ""))[:100],
                f"{prefix}observaciones": str(t.get("observaciones", ""))[:200],
                f"{prefix}resultado": res_status[:20],
                f"{prefix}mensaje_resultado": msg_res,
                f"{prefix}usuario_sap": str(t.get("usuario_sap", operador))[:20]
            }
            
            # Dataverse Navigation Binding para el ForeignKey (Lookup) de tabla maestro
            if ejecucion_id:
                payload_trans[f"{prefix}ejecucion_id@odata.bind"] = f"/{tabla_ejec}({ejecucion_id})"
                
            payload_trans[f"{prefix}timestamp"] = datetime.now().isoformat() + "Z"

            session.post(f"{api_base}/{tabla_trans}", json=payload_trans, timeout=10)
            
            if "error" in res_status.lower() or "error" in msg_res.lower():
                payload_err = {
                    f"{prefix}id_lote": id_lote,
                    f"{prefix}categoria": "SAP_ERROR",
                    f"{prefix}mensaje": msg_res[:400],
                    f"{prefix}no_doc": str(t.get("no_doc", ""))[:30],
                    f"{prefix}sociedad": str(t.get("sociedad", ""))[:10],
                    f"{prefix}numero_fila": i + 1,
                    f"{prefix}es_critico": "False",
                    f"{prefix}timestamp": datetime.now().isoformat() + "Z"
                }

                if ejecucion_id:
                    payload_err[f"{prefix}ejecucion_id@odata.bind"] = f"/{tabla_ejec}({ejecucion_id})"
                    
                session.post(f"{api_base}/{tabla_err}", json=payload_err, timeout=10)

        return True, "Bot Farm Dataverse: Transacciones Insertadas"

    except requests.exceptions.HTTPError as err:
        return False, f"Dataverse HTTP Error: {err.response.text}"
    except Exception as e:
        return False, f"Dataverse Internal: {str(e)}"