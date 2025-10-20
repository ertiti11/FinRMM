from cx_Freeze import setup, Executable
import sys

# Si es consola o GUI
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Para GUI, o None si es consola

executables = [Executable("main.py", base=base, icon="icon.ico")]

build_options = {
    "includes": [
        "OpenSSL.SSL",
        "OpenSSL.crypto",
        "psutil._psutil_posix",  # sólo si usas psutil en Linux/WSL
        "psutil._psutil_windows",  # renombrar según plataforma
        "socket",
        "sqlite3",
        "hashlib",
        "time",
        "tkinter",
        "pocketbase",
    ],
    "packages": [
        "requests",
        "cryptography",
        "tkinter",
        "pocketbase",
        "socket",
        "sqlite3",
        "hashlib",
        "time",
        "psutil",
    ],
    "excludes": ["IPython", "matplotlib", "pytest", "pyopenssl"],  # todo lo que no uses
}

setup(
    name="MiApp",
    version="1.0",
    description="Descripción de la app",
    options={"build_exe": build_options},
    executables=executables,
)
