import os
import yaml
from pathlib import Path
from importlib import resources
from rich.console import Console
from hyperpytext.utils.npm_tailwind_utils import update_tailwind_config

console=Console()

def create_file(filename, content:str = ''):
    """Writes the template file"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        f.write(content)

def get_template_path(template_path: str) -> Path:
    """Get the absolute path to a template directory."""
    with resources.path('hyperpytext.templates', template_path) as path:
        return path

#SERVER_TEMPLATES_PATH = get_template_path('react/server')
#CLIENT_TEMPLATES_PATH = get_template_path('react/client')

BASE_DIR = Path(__file__).parent
SERVER_TEMPLATES_PATH = BASE_DIR / "templates/react/server"
CLIENT_TEMPLATES_PATH = BASE_DIR / "templates/react/client"

def create_client_files(plugins:list[str | None] | None = None, fonts:bool = False):
    for template_file in os.listdir(CLIENT_TEMPLATES_PATH):
        if template_file.endswith('.yaml'):
            with open(os.path.join(CLIENT_TEMPLATES_PATH, template_file), 'r') as file:
                templates = yaml.safe_load(file)

                # Tailwind config update
                if template_file == 'tailwind.config.js.yaml':
                    filename = templates['filename']
                    content = templates['content']
                    create_file(filename, content)
                    update_tailwind_config(filename, plugins, fonts)
                    console.print("✔ Updated tailwind.config.js")

                # Geist fonts
                if template_file == 'fonts.css.yaml':
                    if fonts:
                        filename = templates['filename']
                        console.print(f"✔ Created {filename}")
                        content = templates['content']
                        create_file(filename, content)
                    else:
                        continue

                # All files
                else:
                    filename = templates['filename']
                    console.print(f"✔ Created {filename}")
                    content = templates['content']
                    create_file(filename, content)
