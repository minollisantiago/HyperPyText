import os
import subprocess
from rich.console import Console
from .npm_utils import check_system, check_npm_package, update_package_json

console = Console()

def update_package_json_for_electron(project_dir, app_name):
    updates = {
        'main': 'main.js',
        'scripts': {
            'start': 'electron .',
            'package': f'electron-packager . {app_name} --platform=win32,darwin,linux --arch=x64 --out=dist'
        }
    }
    update_package_json(project_dir, updates)


def setup_electron_npm(project_dir, app_name):
    os.chdir(project_dir)
    npm_ = "npm.cmd" if check_system() == "windows" else "npm"
    if not check_npm_package('electron'):
        console.print("Installing Electron...")
        subprocess.run([npm_, "init", "-y"], check=True)
        subprocess.run([npm_, "install", "--save-dev", "electron@latest"], check=True)

    update_package_json_for_electron(project_dir, app_name)

