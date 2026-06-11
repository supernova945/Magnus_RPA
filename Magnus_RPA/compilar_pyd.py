import os
import sys
import shutil
from setuptools import setup
from Cython.Build import cythonize

def compilar():
    print("=====================================================")
    print("   COMPILADOR DE MÉTODOS MAGNUS (.PY -> .PYD)   ")
    print("=====================================================")
    
    directorio_metodos = "metodos"
    if not os.path.exists(directorio_metodos):
        print(f"[ERROR]: No se encontró la carpeta {directorio_metodos}")
        return

    # Listar archivos .py en la carpeta metodos (excluyendo __init__.py)
    archivos = [os.path.join(directorio_metodos, f) for f in os.listdir(directorio_metodos) 
                if f.endswith(".py") and f != "__init__.py"]

    if not archivos:
        print("[INFO]: No hay archivos para compilar en 'metodos/'.")
        return

    print(f"[INFO]: Compilando {len(archivos)} archivos...")

    try:
        # Ejecutar la compilación
        setup(
            ext_modules=cythonize(archivos, compiler_directives={'language_level': "3"}),
            script_args=['build_ext', '--inplace']
        )
        
        # Limpieza de archivos temporales (.c y carpetas de build)
        print("\n[INFO]: Limpiando archivos temporales...")
        for f in archivos:
            c_file = f.replace(".py", ".c")
            if os.path.exists(c_file):
                os.remove(c_file)
        
        if os.path.exists("build"):
            shutil.rmtree("build")
            
        print("\n" + "=" * 50)
        print("[OK] ¡COMPILACIÓN DE MÉTODOS EXITOSA!")
        print("=====================================================")
        print("Ahora tus métodos están protegidos en archivos .pyd.")
        
    except Exception as e:
        print("\n[ERROR]: Ocurrió un fallo durante la compilación.")
        print(f"Detalle: {e}")
        print("\n[NOTA]: Asegúrate de tener instalado 'Visual Studio Build Tools' con el componente de C++.")

if __name__ == "__main__":
    compilar()
