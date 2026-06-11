import os
import subprocess
import sys

def crear_ejecutable():
    print("=====================================================")
    print("   COMPILADOR DE MAGNUS RPA A EJECUTABLE (.EXE)   ")
    print("=====================================================")
    
    # 1. Comprobar que PyInstaller esté instalado
    try:
        import PyInstaller
    except ImportError:
        print("[ERROR]: No tienes instalada la librería PyInstaller.")
        print("[INFO]: Por favor, ejecuta primero este comando en tu terminal:")
        print("   pip install pyinstaller")
        return

    # 2. Configuración del empaquetado
    # El punto de entrada será launcher.py (si ese es tu actualizador externo)
    # o main.py (si quieres arrancar directo la app sin pasar por el launcher).
    # Como tu proyecto en la Fase 1 usaba launcher.py como entry point, usaremos ese.
    archivo_principal = "launcher.py"
    
    if not os.path.exists(archivo_principal):
        print(f"[ERROR]: No se encontró {archivo_principal}")
        return

    ruta_ico = os.path.join("recursos", "magnus.ico")
    if not os.path.exists(ruta_ico):
        print(f"[AVISO]: No se encontró el ícono en '{ruta_ico}'. Se compilará sin ícono personalizado.")
        ruta_ico = None

    # Construir el comando como lista (SIN shell=True) para evitar problemas con espacios y comillas en Windows
    comando = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name", "Magnus",
        # Incluir carpetas de recursos para que resolver_ruta() las encuentre en el .exe
        "--add-data", f"recursos{os.pathsep}recursos",
        "--add-data", f"formularios{os.pathsep}formularios",
        "--add-data", f"vistas{os.pathsep}vistas",
        "--add-data", f"metodos{os.pathsep}metodos",
    ]

    # Solo si el .ico existe, incrustarlo en el .exe
    if ruta_ico:
        comando += ["--icon", ruta_ico]

    # Agregar version.txt si existe
    if os.path.exists("version.txt"):
        comando += ["--add-data", f"version.txt{os.pathsep}."]

    # Agregar mod_cierre.py si existe (módulo externo sin carpeta)
    if os.path.exists("mod_cierre.py"):
        comando += ["--add-data", f"mod_cierre.py{os.pathsep}."]

    comando.append(archivo_principal)

    print("Empaquetando tu aplicación... Esto puede tardar unos minutos la primera vez.")
    print("-" * 50)
    print(f"Comando: {' '.join(comando)}")
    print("-" * 50)

    resultado = subprocess.run(comando)  # Sin shell=True — más seguro y portable
    
    if resultado.returncode == 0:
        print("\n" + "=" * 50)
        print("[OK] ¡COMPILACIÓN EXITOSA!")
        print("=====================================================")
        print("Busca tu programa final en la nueva carpeta 'dist'.")
        print("-> Allí dentro habrá una carpeta llamada 'Magnus', que debes comprimir en .zip si se la quieres enviar a alguien.")
        print("-> El archivo que ellos deben hacer doble clic es 'Magnus.exe' que está adentro de esa carpeta.")
    else:
        print("\n[ERROR] Ocurrió un error inesperado al compilar.")
        print("Revisa los errores en tu terminal para más detalles.")

if __name__ == "__main__":
    crear_ejecutable()
