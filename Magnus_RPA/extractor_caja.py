import win32com.client
import ctypes

def obtener_datos_sesion(session):
    try:
        id_texto = "/app/con[0]/ses[0]/wnd[0]/usr/subINFO_SCREEN:/DBM/MT_TILL:2001/cntlSESSION_CON/shellcont/shell"
        
        # Extraemos todo el texto de SAP
        texto_crudo = session.findById(id_texto).text
        
        # Estandarizamos los saltos de línea y cortamos el texto línea por línea
        lineas = texto_crudo.replace('\r', '\n').split('\n')
        
        val_caja = "CAJA_NO_ENCONTRADA"
        val_sesion = "SESION_NO_ENCONTRADA"
        
        for linea in lineas:
            linea_limpia = linea.strip()
            
            # Si la línea empieza con "Caja", le borramos esa palabra y guardamos el resto
            if linea_limpia.startswith("Caja"):
                val_caja = linea_limpia.replace("Caja", "").strip()
                
            # Si la línea empieza con "Sesión" (con o sin tilde), hacemos lo mismo
            elif linea_limpia.startswith("Sesión") or linea_limpia.startswith("Sesion"):
                val_sesion = linea_limpia.replace("Sesión", "").replace("Sesion", "").strip()
        
        # Armamos el string final
        return f"{val_caja} SESION# {val_sesion}"
        
    except Exception as e:
        return f"Error: {e}"

def main():
    try:
        # Conexión a SAP
        SapGuiAuto = win32com.client.GetObject("SAPGUI")
        application = SapGuiAuto.GetScriptingEngine
        connection = application.Children(0)
        session = connection.Children(0)
        
        # Obtener el dato formateado
        mensaje_final = obtener_datos_sesion(session)
        
        # Mostrar el MessageBox (0 = OK, 64 = Icono de Información)
        ctypes.windll.user32.MessageBoxW(0, mensaje_final, "Validación Magnus", 64)
        
    except Exception as e:
        ctypes.windll.user32.MessageBoxW(0, f"No hay conexión con SAP: {e}", "Error", 16)

if __name__ == "__main__":
    main()