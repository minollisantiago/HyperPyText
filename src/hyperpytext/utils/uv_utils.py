import click
import subprocess


def check_uv():
    try:
        result = subprocess.run(["uv", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        click.echo(f"uv is installed. Version: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        click.echo(f"Error running uv: {e}")
        click.echo(f"Stderr: {e.stderr}")
        return False
    except FileNotFoundError:
        click.echo("uv command not found in PATH.")
        return False


def uv_install_instructions():
    """Display instructions for installing uv."""
    click.echo("uv is not installed on your system.")
    click.echo("Please install uv by following these steps:")
    click.echo("1. Visit https://github.com/astral-sh/uv")
    click.echo("2. Follow the installation instructions for your operating system")
    click.echo("3. After installation, restart your terminal/command prompt")
    click.echo("4. Verify the installation by running 'uv --version'")


def setup_uv_environment(dependencies: list[str] | None = None):
    click.echo("Setting up environment...")
    try:
        click.echo("Initializing project...")
        subprocess.run(["uv", "init"], check=True)

        if dependencies:
            click.echo("Adding project dependencies...")
            for package in dependencies:
                uv_add_dependency(package)

        click.echo("Syncing environment...")
        subprocess.run(["uv", "sync"], check=True)

        click.echo("✔ Environment set up successfully!")
    except subprocess.CalledProcessError:
        click.echo("🚩 Failed to set up environment. Please make sure uv is installed and try again.")
    except FileNotFoundError:
        click.echo("🚩 uv not found. Please install uv and try again.")


def uv_add_dependency(package: str, dev: bool = False):
    try:
        cmd = ["uv", "add"]
        if dev:
            cmd.append("--dev")
        cmd.append(package)
        subprocess.run(cmd, check=True)
        click.echo(f"✔ Successfully added {package}")
    except subprocess.CalledProcessError:
        click.echo(f"🚩 Failed to add dependency: {package}")


def uv_remove_dependency(package: str):
    try:
        subprocess.run(["uv", "remove", package], check=True)
        click.echo(f"✔ Successfully removed {package}")
    except subprocess.CalledProcessError:
        click.echo(f"🚩 Failed to remove dependency: {package}")
