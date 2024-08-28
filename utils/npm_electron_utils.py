import subprocess
import os
import json
import click
from .npm_utils import check_system, check_npm


def check_electron_npm():
    package_json_ = os.path.join(os.getcwd(), 'package.json')
    if os.path.exists(package_json_):
        with open(package_json_, 'r') as file:
            package_json = json.load(file)
            dependencies = package_json.get('dependencies', {})
            dev_dependencies = package_json.get('devDependencies', {})
            if any(['electron' in dep for dep in [dependencies, dev_dependencies]]):
                return True
    return False


def setup_electron_npm(project_dir):
    os.chdir(project_dir)
    npm_ = "npm.cmd" if check_system() == "windows" else "npm"
    if not check_electron_npm():
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
