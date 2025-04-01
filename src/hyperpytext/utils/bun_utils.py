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

def check_bun(verbose=False):
    """Check if bun is installed and available in the system."""
    try:
        result = subprocess.run(["bun", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if verbose:
            console.print(f"bun version: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        if verbose:
            console.print(f"Error running bun: {e}")
            console.print(f"Stderr: {e.stderr}")
        return False
    except FileNotFoundError:
        if verbose:
            console.print("🚩 bun command not found in PATH...")
        return False

def bun_install_instructions():
    """Display instructions for installing bun."""
    console.print("bun is not installed on your system.")
    console.print("Please install bun by following these steps:")
    console.print("1. Visit https://bun.sh/")
    console.print("2. Run the installation command for your operating system:")
    console.print("   - macOS/Linux: curl -fsSL https://bun.sh/install | bash")
    console.print("   - Windows: Use WSL2 and follow the Linux instructions")
    console.print("3. After installation, restart your terminal/command prompt")
    console.print("4. Verify the installation by running 'bun --version'")
    console.print("Once bun is installed, please run this script again.")

def check_bun_package(package):
    """Check if a package is installed in the current project."""
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
    Universal package.json updater for bun projects

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

def setup_vite_bun(app_dir, template='react', use_typescript=True):
    """Setup a new Vite project using bun."""
    client_dir = os.path.join(app_dir, 'client')
    os.makedirs(client_dir, exist_ok=True)
    os.chdir(client_dir)

    # Create a new Vite project
    cmd = ["bun", "create", "vite", ".", "--template", "react-ts" if use_typescript else "react"]
    subprocess.run(cmd, check=True)

    # Install dependencies
    subprocess.run(["bun", "install"], check=True)

    # Update package.json with bun-specific scripts
    updates = {
        "scripts": {
            "start": "bun run dev",
            "dev": "bun run --bun vite",
            "build": "bun run build",
            "preview": "bun run preview"
        }
    }
    update_package_json(client_dir, updates)

    os.chdir(app_dir)

def setup_tailwind_bun(client_dir, plugins=None, fonts=False):
    """Setup Tailwind CSS using bun."""
    os.chdir(client_dir)

    # Install Tailwind and its dependencies
    cmd = ["bun", "add", "-d", "tailwindcss", "postcss", "autoprefixer"]
    subprocess.run(cmd, check=True)

    # Install plugins if specified
    if plugins:
        for plugin in plugins:
            subprocess.run(["bun", "add", "-d", f"@tailwindcss/{plugin}"], check=True)

    # Install Geist fonts if specified
    if fonts:
        subprocess.run(["bun", "add", "@vercel/fonts"], check=True)

    # Initialize Tailwind
    subprocess.run(["bunx", "tailwindcss", "init", "-p"], check=True)

    os.chdir(os.path.dirname(client_dir))

def setup_shadcn_bun(client_dir):
    """Setup Shadcn UI using bun."""
    os.chdir(client_dir)

    # Install shadcn-ui CLI
    subprocess.run(["bun", "add", "-d", "shadcn-ui"], check=True)

    # Initialize shadcn-ui
    subprocess.run(["bunx", "shadcn-ui@latest", "init"], check=True)

    os.chdir(os.path.dirname(client_dir)) 