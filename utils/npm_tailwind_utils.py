import subprocess
import sys
import click
import json
import os


def check_system():
    if sys.platform.startswith('win'):
        return "windows"
    elif sys.platform.startswith('darwin'):
        return "mac"
    elif sys.platform.startswith('linux'):
        return "linux"


def check_npm():
    npm_ = "npm.cmd" if check_system() == "windows" else "npm"
    try:
        result = subprocess.run([npm_, "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"npm version: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running npm: {e}")
        print(f"Stderr: {e.stderr}")
        return False
    except FileNotFoundError:
        click.echo("npm command not found in PATH...")
        return False


def check_tailwind_npm2():
    npx_ = "npx.cmd" if check_system() == "windows" else "npx"
    print(npx_)
    try:
        subprocess.run([npx_, "tailwindcss", "--help"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def check_tailwind_npm():
    package_json_ = os.path.join(os.getcwd(), 'package.json')
    if os.path.exists(package_json_):
        with open(package_json_, 'r') as file:
            package_json = json.load(file)
            dependencies = package_json.get('dependencies', {})
            dev_dependencies = package_json.get('devDependencies', {})
            if any(['tailwindcss' in dep for dep in [dependencies, dev_dependencies]]):
                return True
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


def setup_tailwind_npm(project_dir, plugins):
    os.chdir(project_dir)
    npm_ = "npm.cmd" if check_system() == "windows" else "npm"
    npx_ = "npx.cmd" if check_system() == "windows" else "npx"
    if not check_tailwind_npm():
        click.echo("Installing Tailwind CSS...")
        subprocess.run([npm_, "init", "-y"], check=True)
        subprocess.run([npm_, "install", "-D", "tailwindcss@latest", "autoprefixer@latest"], check=True)

    subprocess.run([npx_, "tailwindcss", "init", "-p"], check=True)

    for plugin in plugins:
        click.echo(f"Installing Tailwind {plugin} plugin...")
        subprocess.run([npm_, "install", "-D", f"@tailwindcss/{plugin}"], check=True)


def setup_tailwind_standalone(project_dir):
    os.chdir(project_dir)
    if not check_tailwind_standalone():
        click.echo("Downloading Tailwind CSS standalone CLI...")
        output=""
        if sys.platform.startswith('win'):
            url = "https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-windows-x64.exe"
        elif sys.platform.startswith('darwin'):
            url = "https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-macos-arm64"
            output = "tailwindcss-macos-arm64"
        elif sys.platform.startswith('linux'):
            url = "https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64"
            output = "tailwindcss-linux-x64"
        else:
            click.echo("Unsupported operating system for Tailwind CSS standalone CLI.")
            return

        subprocess.run(["curl", "-sLO", url], check=True)
        if not sys.platform.startswith('win'):
            subprocess.run(["chmod", "+x", output], check=True)
            subprocess.run(["mv", output, "tailwindcss"], check=True)

    subprocess.run([f"./tailwindcss", "init"], check=True)


def update_package_json(project_dir, new_scripts):
    os.chdir(project_dir)
    with open('package.json', 'r') as f:
        package = json.load(f)
    package['scripts'].update(json.loads('{' + new_scripts + '}'))
    with open('package.json', 'w') as f:
        json.dump(package, f, indent=2)


def update_tailwind_config(filename, plugins):
    with open(filename, 'r') as f:
        config = f.read()
    plugin_imports = ''.join([f"\n\t\trequire('@tailwindcss/{plugin}')," for plugin in plugins])
    updated_config = config.replace("plugins: [__PLUGINS__],", f"plugins: [{plugin_imports}\n\t],")
    with open(filename, 'w') as f:
        f.write(updated_config)
