import os
import sys
import click
import subprocess
from .npm_utils import check_system, check_npm_package, update_package_json


def check_tailwind_npm2():
    npx_ = "npx.cmd" if check_system() == "windows" else "npx"
    print(npx_)
    try:
        subprocess.run([npx_, "tailwindcss", "--help"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_tailwind_standalone():
    tailwind_exe = "tailwindcss.exe" if sys.platform.startswith('win') else "tailwindcss"
    return os.path.exists(tailwind_exe)


def update_package_json_for_tailwind(project_dir):
    updates = {
        'scripts': {
            'build-css': 'tailwindcss -i ./src/styles/globals.css -o ./src/styles/style.css',
            'watch-css': 'tailwindcss -i ./src/styles/globals.css -o ./src/styles/style.css --watch'
        }
    }
    update_package_json(project_dir, updates)


def setup_tailwind_npm(project_dir, plugins, fonts):
    os.chdir(project_dir)
    npm_ = "npm.cmd" if check_system() == "windows" else "npm"
    npx_ = "npx.cmd" if check_system() == "windows" else "npx"
    if not check_npm_package('tailwindcss'):
        click.echo("Installing Tailwind CSS...")
        subprocess.run([npm_, "init", "-y"], check=True)
        subprocess.run(
            [npm_, "install", "-D", "tailwindcss@latest", "autoprefixer@latest", "postcss@latest"],
            check=True
        )

    subprocess.run([npx_, "tailwindcss", "init", "-p"], check=True)

    for plugin in plugins:
        click.echo(f"Installing Tailwind {plugin} plugin...")
        subprocess.run([npm_, "install", "-D", f"@tailwindcss/{plugin}"], check=True)

    if fonts:
        click.echo(f"Installing Geist Fonts...")
        subprocess.run([npm_, "i", 'geist'], check=True)

    update_package_json_for_tailwind(project_dir)


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


def update_tailwind_config(filename, plugins, fonts):
    with open(filename, 'r') as f:
        config = f.read()
    # Plugins
    plugin_imports = ''.join([f"\n\t\trequire('@tailwindcss/{plugin}')," for plugin in plugins])
    updated_config = config.replace("plugins: [__PLUGINS__],", f"plugins: [{plugin_imports}\n\t],")
    # fonts
    if fonts:
        custom_fonts = [
            "\n\t\t\t\tmono: ['GeistMono', ...defaultTheme.fontFamily.mono],",
            "\n\t\t\t\tsans: ['GeistSans', ...defaultTheme.fontFamily.sans],",
        ]
        updated_config = updated_config.replace("fontFamily: {__FONTS__},", f"fontFamily: {{{''.join(custom_fonts)}\n\t\t\t}},")
    # Update the file
    with open(filename, 'w') as f:
        f.write(updated_config)
