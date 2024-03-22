import subprocess

def install_and_show_output(package):
    try:
        print(f"Installing {package}...")
        subprocess.check_call(["apt", "install", package])
        print(f"{package} Correcting installation.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing {package}: {e}")

