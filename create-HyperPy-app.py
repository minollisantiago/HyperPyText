import os
import click
import yaml
from utils.npm_tailwind_utils import (
    check_npm, 
    check_tailwind_npm, 
    check_tailwind_standalone,
    npm_install_instructions, 
    setup_tailwind_npm, 
    setup_tailwind_standalone, 
    update_package_json
)

@click.command()
@click.argument('app_name')
@click.option('--templates_dir', default='templates', help='Path to the templates directory')
def create_app(app_name, templates_dir):

    # Prompt for HTML filename
    if click.confirm('Would you like to change the name of index.html?', default=False):
        html_filename = click.prompt('Enter the name for your HTML file (without .html extension)', default='index')
    else:
        html_filename = 'index'

    # Prompt for Tailwind CSS
    if click.confirm('Would you like to use Tailwind CSS?', default=False):
        tailwind = click.prompt('Choose Tailwind CSS setup option', type=click.Choice(['npm', 'standalone']), default='npm')
    else:
        tailwind = 'none'

    # Start creating
    click.echo(f"\nCreating a new HyperPy app in {os.path.join(os.getcwd(), app_name)}")

    if tailwind == 'npm':
        if not check_npm():
            npm_install_instructions()
            return
        if not check_tailwind_npm():
            click.echo("Tailwind CSS is not installed. It will be installed during app setup.")
    elif tailwind == 'standalone':
        if not check_tailwind_standalone():
            click.echo("Tailwind CSS standalone CLI is not found. It will be downloaded during app setup.")

    # Create main app directory
    os.makedirs(app_name, exist_ok=True)
    app_dir = os.path.abspath(app_name)
    os.chdir(app_dir)

    # Create folders
    folders = ['api', 'config', 'db', 'logs', 'notebooks', 'templates', 'utils']
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

    # Create 'routers' subfolder inside 'api'
    os.makedirs(os.path.join('api', 'routers'), exist_ok=True)

    # Create assets subfolders
    asset_subfolders = ['fonts', 'icons', 'images', 'svg-loaders', 'css', 'js', 'docs']
    for subfolder in asset_subfolders:
        os.makedirs(os.path.join('assets', subfolder), exist_ok=True)

    # Create files from templates
    for template_file in os.listdir(templates_dir):
        if template_file.endswith('.yaml'):
            with open(os.path.join(templates_dir, template_file), 'r') as file:
                templates = yaml.safe_load(file)
                
                if template_file == 'api_templates.yaml':
                    for template in templates:
                        filename = template['filename'].format(app_name=app_name)
                        content = template['content'].format(app_name=app_name, html_filename=html_filename)
                        create_file(filename, content)
                elif template_file == 'gitignore_template.yaml':
                    filename = templates['filename']
                    content = templates['content']
                    create_file(filename, content)
                else:
                    template = templates
                    filename = template['filename']
                    content = template['content']
                    
                    if template_file == 'html_template.yaml':
                        filename = filename.format(filename=html_filename)
                        content = content.format(title=html_filename)
                    else:
                        filename = filename.format(app_name=app_name)
                        content = content.format(app_name=app_name)
                    
                    create_file(filename, content)

    # Setup Tailwind if selected
    if tailwind == 'npm':
        setup_tailwind_npm(app_dir)
        update_package_json(app_dir, '"build-css": "tailwindcss -i ./assets/css/input.css -o ./assets/css/style.css --watch"')
    elif tailwind == 'standalone':
        setup_tailwind_standalone(app_dir)

    click.echo(f"App '{app_name}' has been created successfully!")

def create_file(filename, content=''):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        f.write(content)

if __name__ == '__main__':
    create_app()