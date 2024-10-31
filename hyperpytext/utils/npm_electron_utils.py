import os
import json
import click
import subprocess
from .npm_utils import check_system, check_npm_package


def setup_electron_npm(project_dir):
    os.chdir(project_dir)
    npm_ = "npm.cmd" if check_system() == "windows" else "npm"
    if not check_npm_package('electron'):
        click.echo("Installing Electron...")
        subprocess.run([npm_, "init", "-y"], check=True)
        subprocess.run([npm_, "install", "--save-dev", "electron@latest"], check=True)


def update_package_json_for_electron(project_dir, app_name):
    os.chdir(project_dir)
    with open('package.json', 'r') as f:
        package = json.load(f)
    
    package['main'] = 'main.js'
    package['scripts']['start'] = 'electron .'
    package['scripts']['package'] = f'electron-packager . {app_name} --platform=win32,darwin,linux --arch=x64 --out=dist'

    with open('package.json', 'w') as f:
        json.dump(package, f, indent=2)
