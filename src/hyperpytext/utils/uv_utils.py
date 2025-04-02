import subprocess
from rich.console import Console

SERVER_DEPENDENCIES = [
    "uvicorn~=0.32.0",
    "fastapi~=0.115.0",
    "python-dotenv~=1.0.0",
    "piccolo[all]~=1.22.0",
    "piccolo-api~=1.5.2",
    "yagmail~=0.15.293"
]

console = Console()

def check_uv():
    try:
        result = subprocess.run(["uv", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        console.print(f"uv is installed. Version: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"Error running uv: {e}")
        console.print(f"Stderr: {e.stderr}")
        return False
    except FileNotFoundError:
        console.print("uv command not found in PATH.")
        return False


def uv_install_instructions():
    """Display instructions for installing uv."""
    console.print("uv is not installed on your system.")
    console.print("Please install uv by following these steps:")
    console.print("1. Visit https://github.com/astral-sh/uv")
    console.print("2. Follow the installation instructions for your operating system")
    console.print("3. After installation, restart your terminal/command prompt")
    console.print("4. Verify the installation by running 'uv --version'")


def setup_uv_environment(dependencies: list[str] | None = None):
    console.print("Setting up environment...")
    try:
        console.print("Initializing project...")
        subprocess.run(["uv", "init"], check=True)

        if dependencies:
            console.print("Adding project dependencies...")
            for package in dependencies:
                uv_add_dependency(package)

        console.print("Syncing environment...")
        subprocess.run(["uv", "sync"], check=True)

        console.print("✔ Environment set up successfully!")
    except subprocess.CalledProcessError:
        console.print("🚩 Failed to set up environment. Please make sure uv is installed and try again.")
    except FileNotFoundError:
        console.print("🚩 uv not found. Please install uv and try again.")


def uv_add_dependency(package: str, dev: bool = False):
    try:
        cmd = ["uv", "add"]
        if dev:
            cmd.append("--dev")
        cmd.append(package)
        subprocess.run(cmd, check=True)
        console.print(f"✔ Successfully added {package}")
    except subprocess.CalledProcessError:
        console.print(f"🚩 Failed to add dependency: {package}")


def uv_remove_dependency(package: str):
    try:
        subprocess.run(["uv", "remove", package], check=True)
        console.print(f"✔ Successfully removed {package}")
    except subprocess.CalledProcessError:
        console.print(f"🚩 Failed to remove dependency: {package}")
