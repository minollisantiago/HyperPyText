import subprocess
import sys
import click
import json
import os

def check_npm():
    try:
        subprocess.run(["npm", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def check_tailwind_npm():
    try:
        subprocess.run(["npx", "tailwindcss", "--help"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def check_tailwind_standalone():
    tailwind_exe = "tailwindcss.exe" if sys.platform.startswith('win') else "tailwindcss"
    return os.path.exists(tailwind_exe)

def npm_install_instructions():
    click.echo("npm is not installed on your system.")
    click.echo("Please install Node.js and npm by following these steps:")
    click.echo("1. Visit https://nodejs.org/")
    click.echo("2. Download the appropriate version for your operating system")
    click.echo("3. Run the installer and follow the installation prompts")
    click.echo("4. After installation, restart your terminal/command prompt")
    click.echo("5. Verify the installation by running 'node --version' and 'npm --version'")
    click.echo("Once npm is installed, please run this script again.")

def setup_tailwind_npm(project_dir):
    os.chdir(project_dir)
    if not check_tailwind_npm():
        click.echo("Installing Tailwind CSS...")
        subprocess.run(["npm", "init", "-y"], check=True)
        subprocess.run(["npm", "install", "-D", "tailwindcss@latest", "postcss@latest", "autoprefixer@latest"], check=True)
    subprocess.run(["npx", "tailwindcss", "init", "-p"], check=True)

def setup_tailwind_standalone(project_dir):
    os.chdir(project_dir)
    if not check_tailwind_standalone():
        click.echo("Downloading Tailwind CSS standalone CLI...")
        if sys.platform.startswith('win'):
            url = "https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-windows-x64.exe"
            output = "tailwindcss-windows-x64.exe"
        elif sys.platform.startswith('darwin'):
            url = "https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-macos-x64"
            output = "tailwindcss"
        elif sys.platform.startswith('linux'):
            url = "https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64"
            output = "tailwindcss"
        else:
            click.echo("Unsupported operating system for Tailwind CSS standalone CLI.")
            return

        subprocess.run(["curl", "-sLO", url], check=True)
        if not sys.platform.startswith('win'):
            subprocess.run(["chmod", "+x", output], check=True)
    
    subprocess.run([f"./{output}", "init"], check=True)

def update_package_json(project_dir, new_scripts):
    os.chdir(project_dir)
    with open('package.json', 'r') as f:
        package = json.load(f)
    
    package['scripts'].update(json.loads('{' + new_scripts + '}'))
    
    with open('package.json', 'w') as f:
        json.dump(package, f, indent=2)