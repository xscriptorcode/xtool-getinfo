import subprocess

def install_and_show_output(package):
    try:
        print(f"Instalando {package}...")
        subprocess.check_call(["apt", "install", package])
        print(f"{package} instalado correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al instalar {package}: {e}")

