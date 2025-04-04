import os
import sys
import json
import subprocess
from rich.console import Console
from hyperpytext.utils.npm_utils import update_package_json
from hyperpytext.utils.npm_vite_utils import configure_vite, remove_default_styles
from hyperpytext.utils.npm_shadcnui_utils import update_tsconfig_json, update_tsconfig_app_json

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


def setup_tailwind_bun(client_dir, fonts:bool=False):
    """Setup Tailwind CSS using bun."""
    os.chdir(client_dir)
    try:
        # Install Tailwind and its dependencies
        cmd = ["bun", "add", "tailwindcss", "@tailwindcss/vite"]
        subprocess.run(cmd, check=True)
        console.print("✔ Installed Tailwind CSS and its dependencies")

        # Install Geist fonts if specified
        if fonts:
            try:
                subprocess.run(["bun", "add", "geist"], check=True)
                console.print("✔ Installed Geist fonts")
            except subprocess.CalledProcessError as e:
                console.print("🚩 Failed to install Geist fonts. Falling back to system fonts.")
                console.print(f"Error: {e}")

    except subprocess.CalledProcessError as e:
        console.print(f"🚩 Error setting up Tailwind: {e}")
    except Exception as e:
        console.print(f"🚩 Unexpected error: {e}")
    finally:
        os.chdir(os.path.dirname(client_dir))


def install_types_bun(project_dir):
    os.chdir(project_dir)
    try:
        subprocess.run(["bun", "add", "-D", "@types/node"], check=True)
        console.print("✔ Installed @types/node successfully.")
    except subprocess.CalledProcessError:
        console.print("🚩 Failed to install @types/node.")


def setup_shadcn_bun(project_dir):
    """Setup Shadcn UI using bun."""
    update_tsconfig_json(project_dir)
    update_tsconfig_app_json(project_dir)
    install_types_bun(project_dir)
    os.chdir(project_dir)
    console.print("Initializing Shadcn UI...")
    subprocess.run(["bun", "add", "-d", "shadcn"], check=True)
    subprocess.run(["bunx", "--bun", "shadcn@latest", "init"], check=True)
    os.chdir(project_dir)


def setup_vite_bun(project_dir, app_name='client', template='react', use_typescript=True, shadcn=False):
    """Setup a new Vite project using bun."""
    os.chdir(project_dir)
    console.print("Setting up Vite...")
    template_with_ts = f"{template}-ts" if use_typescript else template
    subprocess.run(
        ["bun", "create", "vite@latest", app_name, "--template", template_with_ts],
        check=True
    )

    # Install dependencies
    os.chdir(app_name)
    console.print("Running bun install...")
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
    update_package_json(project_dir, updates, subdir=app_name)
    configure_vite(project_dir, subdir=app_name, use_shadcn=shadcn)
    remove_default_styles(project_dir, subdir=app_name)

    os.chdir("..")
    console.print("✔ Vite setup complete.")

