import os
import subprocess
import glob

def compilar_formularios():
    print("Iniciando compilación de interfaces UI a Python...")
    print("-" * 50)
    
    # 1. Buscar todos los archivos .ui en la carpeta formularios
    archivos_ui = glob.glob(os.path.join("formularios", "*.ui"))
    
    if not archivos_ui:
        print("No se encontraron archivos .ui en la carpeta 'formularios'.")
        return

    compilados_ok = 0
    errores = 0

    for ui_path in archivos_ui:
        # 2. Generar el nombre del archivo de salida
        nombre_base = os.path.basename(ui_path)
        nombre_sin_ext = os.path.splitext(nombre_base)[0]
        py_path = os.path.join("formularios", f"ui_{nombre_sin_ext}.py")
        
        print(f"Compilando: {nombre_base} -> ui_{nombre_sin_ext}.py", end="... ")
        
        # 3. Intentar diferentes variaciones del comando uic
        import sys, site
        base = site.getuserbase()
        scripts_dir = os.path.join(base, f"Python{sys.version_info.major}{sys.version_info.minor}", "Scripts")
        uic_exe = os.path.join(scripts_dir, "pyside6-uic.exe")
        
        comandos_posibles = [
            f'"{uic_exe}" "{ui_path}" -o "{py_path}"',
            f'pyside6-uic "{ui_path}" -o "{py_path}"',
            f'python -m PySide6.uic "{ui_path}" -o "{py_path}"',
            f'py -m PySide6.uic "{ui_path}" -o "{py_path}"'
        ]
        
        exito = False
        ultimo_error = ""
        
        for comando in comandos_posibles:
            try:
                resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
                if resultado.returncode == 0:
                    exito = True
                    break
                else:
                    ultimo_error = resultado.stderr
            except:
                pass
                
        if exito:
            print("[OK]")
            compilados_ok += 1
        else:
            print("[ERROR]")
            print(f"Detalle: {ultimo_error}")
            errores += 1

    print("-" * 50)
    print(f"Proceso finalizado. {compilados_ok} compilados con éxito, {errores} errores.")
    
    # 4. Parche opcional (si tu uic genera import recursos_rc incorrecto)
    print("\nAplicando parche de rutas de recursos...")
    for ui_path in archivos_ui:
        nombre_base = os.path.basename(ui_path)
        nombre_sin_ext = os.path.splitext(nombre_base)[0]
        py_path = os.path.join("formularios", f"ui_{nombre_sin_ext}.py")
        
        if os.path.exists(py_path):
            try:
                with open(py_path, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                
                # Reemplazar el import malo por el bueno
                contenido = contenido.replace('import recursos_rc', 'from recursos import recursos_rc')
                contenido = contenido.replace('import recursos.recursos_rc', 'from recursos import recursos_rc')
                
                with open(py_path, 'w', encoding='utf-8') as f:
                    f.write(contenido)
            except: pass

    print("¡Listo para ejecutar main.py!")

if __name__ == "__main__":
    compilar_formularios()
