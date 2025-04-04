import os
import yaml
from pathlib import Path
from importlib import resources
from rich.console import Console

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

SERVER_TEMPLATES_PATH = get_template_path('react/server')
CLIENT_TEMPLATES_PATH = get_template_path('react/client')

def create_client_files(client_dir:str, fonts:bool = False):
    os.chdir(client_dir)
    for template_file in os.listdir(CLIENT_TEMPLATES_PATH):
        if template_file.endswith('.yaml'):
            with open(os.path.join(CLIENT_TEMPLATES_PATH, template_file), 'r') as file:
                templates = yaml.safe_load(file)

                # Geist fonts
                if template_file == 'fonts.css.yaml':
                    if fonts:
                        filename = templates['filename']
                        content = templates['content']
                        create_file(filename, content)
                        console.print(f"✔ Created {filename}")
                    else:
                        continue

                # All other files
                else:
                    filename = templates['filename']
                    content = templates['content']
                    create_file(filename, content)
                    console.print(f"✔ Created {filename}")
