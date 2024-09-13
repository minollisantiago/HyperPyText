import subprocess
import sys
import click


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
            print(f"npm version: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        if verbose:
            print(f"Error running npm: {e}")
            print(f"Stderr: {e.stderr}")
        return False
    except FileNotFoundError:
        if verbose:
            click.echo("npm command not found in PATH...")
        return False


def npm_install_instructions():
    click.echo("npm is not installed on your system.")
    click.echo("Please install Node.js and npm by following these steps:")
    click.echo("1. Visit https://nodejs.org/")
    click.echo("2. Download the appropriate version for your operating system")
    click.echo("3. Run the installer and follow the installation prompts")
    click.echo("4. After installation, restart your terminal/command prompt")
    click.echo("5. Verify the installation by running 'node --version' and 'npm --version'")
    click.echo("Once npm is installed, please run this script again.")
