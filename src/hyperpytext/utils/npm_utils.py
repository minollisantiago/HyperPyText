import os
import sys
import json
import subprocess
from rich.console import Console

console = Console()

def check_system():
    if sys.platform.startswith('win'):
        return "windows"
    elif sys.platform.startswith('darwin'):
        return "mac"
    elif sys.platform.startswith('linux'):
        return "linux"


def check_npm(verbose=False):
    npm_ = "npm.cmd" if check_system() == "windows" else "npm"
    try:
        result = subprocess.run([npm_, "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if verbose:
            console.print(f"npm version: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        if verbose:
            console.print(f"Error running npm: {e}")
            console.print(f"Stderr: {e.stderr}")
        return False
    except FileNotFoundError:
        if verbose:
            console.print("🚩 npm command not found in PATH...")
        return False


def npm_install_instructions():
    console.print("npm is not installed on your system.")
    console.print("Please install Node.js and npm by following these steps:")
    console.print("1. Visit https://nodejs.org/")
    console.print("2. Download the appropriate version for your operating system")
    console.print("3. Run the installer and follow the installation prompts")
    console.print("4. After installation, restart your terminal/command prompt")
    console.print("5. Verify the installation by running 'node --version' and 'npm --version'")
    console.print("Once npm is installed, please run this script again.")


def check_npm_package(package):
    package_json_ = os.path.join(os.getcwd(), 'package.json')
    if os.path.exists(package_json_):
        with open(package_json_, 'r') as file:
            package_json = json.load(file)
            dependencies = package_json.get('dependencies', {})
            dev_dependencies = package_json.get('devDependencies', {})
            if any([package in dep for dep in [dependencies, dev_dependencies]]):
                return True
    return False


def update_package_json(project_dir, updates, subdir=None):
    """
    Universal package.json updater

    Args:
        project_dir: Base project directory
        updates: Dict containing updates to merge into package.json
        subdir: Optional subdirectory (from root) where package.json is located (e.g., 'client')
    """
    target_dir = os.path.join(project_dir, subdir) if subdir else project_dir
    package_path = os.path.join(target_dir, 'package.json')

    if os.path.exists(package_path):
        with open(package_path, 'r') as f:
            package = json.load(f)

        # Deep merge the updates
        for key, value in updates.items():
            if isinstance(value, dict) and key in package:
                package[key].update(value)
            else:
                package[key] = value

        with open(package_path, 'w') as f:
            json.dump(package, f, indent=2)

        console.print(f"✔ Updated package.json in {target_dir}")
    else:
        console.print(f"🚩 package.json not found in {target_dir}. Skipping update.")
