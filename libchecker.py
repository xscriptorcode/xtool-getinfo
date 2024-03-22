import importlib
import subprocess

def check_and_install_libraries():
    libraries = ['nmap', 'networkx', 'matplotlib']
    for lib in libraries:
        try:
            importlib.import_module(lib)
            print(f"{lib} está instalada.")
        except ImportError:
            print(f"{lib} no está instalada. Instalando...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
            print(f"{lib} instalada correctamente.")

