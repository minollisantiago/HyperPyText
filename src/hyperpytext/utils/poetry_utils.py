import click
import subprocess


def check_poetry():
    try:
        result = subprocess.run(["poetry", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        click.echo(f"Poetry is installed. Version: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        click.echo(f"Error running Poetry: {e}")
        click.echo(f"Stderr: {e.stderr}")
        return False
    except FileNotFoundError:
        click.echo("Poetry command not found in PATH.")
        return False


def poetry_install_instructions():
    click.echo("Poetry is not installed on your system.")
    click.echo("Please install Poetry by following these steps:")
    click.echo("1. Visit https://python-poetry.org/")
    click.echo("2. Follow the installation instructions for your operating system")
    click.echo("3. After installation, restart your terminal/command prompt")
    click.echo("4. Verify the installation by running 'poetry --version'")


def setup_poetry_environment():
    click.echo("Installing environment...")
    try:
        subprocess.run(["poetry", "install"], check=True)
        click.echo("Environment installed successfully!")
    except subprocess.CalledProcessError:
        click.echo("Failed to install environment. Please make sure Poetry is installed and try again.")
    except FileNotFoundError:
        click.echo("Poetry not found. Please install Poetry and try again.")
