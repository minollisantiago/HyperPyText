import os
import subprocess
from rich.console import Console
from .npm_utils import check_system, update_package_json

console = Console()

def update_package_json_for_tailwind(project_dir):
    updates = {
        'scripts': {
            'dev': 'vite',
            'build': 'vite build',
            'preview': 'vite preview'
        }
    }
    update_package_json(project_dir, updates)

def setup_tailwind_npm(project_dir, fonts:bool = False):
    os.chdir(project_dir)
    npm_ = "npm.cmd" if check_system() == "windows" else "npm"

    # Install tailwind and vite plugin
    console.print("Installing Tailwind CSS and Vite plugin...")
    subprocess.run(
        [npm_, "install", "tailwindcss", "@tailwindcss/vite"],
        check=True
    )

    # Install Geist fonts if specified
    if fonts:
        console.print(f"Installing Geist Fonts...")
        subprocess.run([npm_, "install", "-D", "geist"], check=True)

    update_package_json_for_tailwind(project_dir)

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
