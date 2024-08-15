import os
from typing import DefaultDict
import click
from click.termui import confirm
import yaml
from pkg_resources import resource_filename
from utils.npm_tailwind_utils import (
    check_npm,
    check_tailwind_npm,
    check_tailwind_standalone,
    npm_install_instructions,
    setup_tailwind_npm,
    setup_tailwind_standalone,
    update_tailwind_config,
    update_package_json
)

@click.command()
@click.argument('app_name')
def create_app(app_name):

    templates_dir = resource_filename('hyperpytext', 'templates')

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

    # Promp for Tailwind CSS plugins
    plugins = []
    if tailwind != 'none':
        for plugin in ['forms', 'typography', 'container-queries']:
            if click.confirm(f'Would you like to install the Tailwind {plugin} plugin?', default=False):
                plugins.append(plugin)

    # Pompt for custom fonts
    fonts = False
    if check_npm() and tailwind != 'none':
        if click.confirm(f'Would you like to install Geist fonts?', default=False):
           fonts = True

    # Start populating the project folder
    click.echo(f"\nCreating a new HyperPy app in {os.path.join(os.getcwd(), app_name)}")

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

    # Tailwind css
    if tailwind == 'npm':
        if not check_npm():
            npm_install_instructions()
            return
        if not check_tailwind_npm():
            click.echo("Tailwind CSS is not installed. It will be installed during app setup.")
    elif tailwind == 'standalone':
        if not check_tailwind_standalone():
            click.echo("Tailwind CSS standalone CLI is not found. It will be downloaded during app setup.")

    # Setup Tailwind if selected
    if tailwind == 'npm':
        setup_tailwind_npm(app_dir, plugins, fonts)
        update_package_json(app_dir, '"build-css": "tailwindcss -i ./assets/css/input.css -o ./assets/css/style.css --watch"')
    elif tailwind == 'standalone':
        setup_tailwind_standalone(app_dir)

    # Create files from templates
    for template_file in os.listdir(templates_dir):

        if template_file.endswith('.yaml'):

            with open(os.path.join(templates_dir, template_file), 'r') as file:

                templates = yaml.safe_load(file)

                # Api
                if template_file == 'api.yaml':
                    click.echo(f'Created fastApi scafolding')
                    for template in templates:
                        filename = template['filename'].format(app_name=app_name)
                        content = template['content'].format(app_name=app_name, html_filename=html_filename)
                        create_file(filename, content)

                # Index starter HTML5 template
                if template_file == 'index.yaml':
                    click.echo(f'Created {html_filename}.html file')
                    filename = templates['filename'].format(filename=html_filename)
                    content = templates['content'].format(title=html_filename)
                    create_file(filename, content)

                # Root files & tailwind input.css
                root_files = [
                    f'{filename}.yaml' for filename in [
                        'app', 'init', 'gitignore', 'env', 'install_env', 'readme', 'requirements', 'input_css'
                    ]
                ]
                if template_file in root_files:
                    click.echo(f'Created {template_file}')
                    filename = templates['filename']
                    content = templates['content']
                    create_file(filename, content)

                # Tailwind config update
                if template_file == 'tailwind_config.yaml':
                    if tailwind != 'none':
                        click.echo(f'Updated tailwind.config.js')
                        filename = templates['filename']
                        content = templates['content']
                        create_file(filename, content)
                        update_tailwind_config(filename, plugins, fonts)

    click.echo(f"App '{app_name}' has been created successfully!")


def create_file(filename, content=''):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        f.write(content)


if __name__ == '__main__':
    create_app()
