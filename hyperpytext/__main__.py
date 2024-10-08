
import os
import yaml
import click
from pkg_resources import resource_filename
from utils.npm_utils import check_npm, npm_install_instructions
from utils.npm_tailwind_utils import (
    check_tailwind_npm,
    check_tailwind_standalone,
    setup_tailwind_npm,
    setup_tailwind_standalone,
    update_tailwind_config,
    update_package_json
)
from utils.npm_electron_utils import (
    setup_electron_npm,
    update_package_json_for_electron
)
from utils.poetry_utils import (
    check_poetry,
    setup_environment,
    poetry_install_instructions
)

# TODO: Piccolo built-in auth, implement it
# TODO: Add a local port by default on .env maybe and a serve() or run() function to start the uvicorn server

@click.command()
@click.argument('app_name')
def create_app(app_name):

    templates_dir = resource_filename('hyperpytext', 'templates')

    # Prompt for HTML filename
    if click.confirm('Would you like to change the name of index.html?', default=False):
        html_filename = click.prompt('Enter the name for your HTML file (without .html extension)', default='index')
    else:
        html_filename = 'index'

    # Prompt for Tailwind CSS and plugins
    tailwind = 'none'
    plugins = []
    if click.confirm('Would you like to use Tailwind CSS?', default=False):
        tailwind = click.prompt('Choose Tailwind CSS setup option', type=click.Choice(['npm', 'standalone']), default='npm')
        for plugin in ['forms', 'typography', 'container-queries']:
            if click.confirm(f'Would you like to install the Tailwind {plugin} plugin?', default=False):
                plugins.append(plugin)

    # Pompt for custom fonts
    fonts = False
    if check_npm() and tailwind != 'none':
        if click.confirm(f'Would you like to install Geist fonts?', default=False):
           fonts = True

    # Prompt for Electron
    use_electron = click.confirm('Would you like to use Electron?', default=False)

    # Prompt for Piccolo app example
    piccolo_example = click.confirm('Would you like to include a Piccolo db app example for SQLite?', default=False)
    
    # Prompt for Piccolo auth
    piccolo_auth = click.confirm('Would you like to include Piccolo authentication?', default=False)

    # Start populating the project folder
    click.echo(f"\nCreating a new HyperPy app in {os.path.join(os.getcwd(), app_name)}")
    click.echo("This process might take a few minutes. Please be patient.")

    # Project structure
    os.makedirs(app_name, exist_ok=True)
    app_dir = os.path.abspath(app_name)
    os.chdir(app_dir)

    folders = {
        'src/app': ['api/routes', 'components', 'db', 'utils', 'templates'],
        'src/assets': ['fonts', 'icons', 'images', 'svg-loaders', 'css', 'js']
    }
    for base, subdirs in folders.items():
        for subdir in subdirs:
            os.makedirs(os.path.join(base, subdir), exist_ok=True)

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
        update_package_json(app_dir, '"build-css": "tailwindcss -i ./src/assets/css/globals.css -o ./src/assets/css/style.css"')
        update_package_json(app_dir, '"watch-css": "tailwindcss -i ./src/assets/css/globals.css -o ./src/assets/css/style.css --watch"')
    elif tailwind == 'standalone':
        setup_tailwind_standalone(app_dir)

    # Setup Electron if selected
    if use_electron:
        click.echo("Setting up Electron...")
        setup_electron_npm(app_dir)
        update_package_json_for_electron(app_dir, app_name)
        click.echo("Electron setup complete.")

    # Create files from templates
    for template_file in os.listdir(templates_dir):

        if template_file.endswith('.yaml'):

            with open(os.path.join(templates_dir, template_file), 'r') as file:

                templates = yaml.safe_load(file)

                # App files
                if template_file == 'app.yaml':
                    click.echo('creating app files')
                    for template in templates:
                        filename = template['filename']
                        content = template['content']
                        create_file(filename, content)

                # Api
                if template_file == 'api.yaml':
                    click.echo(f'Creating fastApi routes example')
                    for template in templates:
                        filename = template['filename']
                        content = template['content'].format(html_filename=html_filename)
                        create_file(filename, content)

                # Database piccolo setup
                db_files = [
                    f'db_{filename}.yaml' for filename in [
                        'primary',
                        'cache',
                        'queues',
                    ]
                ]
                if piccolo_auth:
                    db_files.append('db_auth.yaml')

                if template_file in db_files:
                    click.echo('Creating piccolo database files')
                    for template in templates:
                        filename = template['filename']
                        if not piccolo_example and (filename.endswith('tables.py') or filename.endswith('db_populate.py')):
                            continue
                        content = template['content']
                        create_file(filename, content)

                # Index starter HTML5 template
                if template_file == 'index.yaml':
                    click.echo(f'Creating {html_filename}.html file')
                    filename = templates['filename'].format(filename=html_filename)
                    content = templates['content'].format(title=html_filename)
                    create_file(filename, content)

                # Root files & tailwind input.css
                root_files = [
                    f'{filename}.yaml' for filename in [
                        'env',
                        'init',
                        'readme',
                        'uvicorn',
                        'gitignore',
                        'input_css',
                    ]
                ]
                if template_file in root_files:
                    filename = templates['filename']
                    click.echo(f'Creating {filename}')
                    content = templates['content']
                    create_file(filename, content)

                # Poetry config update
                if template_file == 'pyproject.yaml':
                    filename = templates['filename']
                    content = templates['content']
                    db_example_dependencies = 'bcrypt = "^4.2.0"\nfaker = "^30.1.0"' if piccolo_example else ''
                    content = content.format(
                        app_name=app_name,
                        db_example_dependencies=db_example_dependencies
                    )
                    create_file(filename, content)

                # Tailwind config update
                if template_file == 'tailwind_config.yaml':
                    if tailwind != 'none':
                        click.echo(f'Updated tailwind.config.js')
                        filename = templates['filename']
                        content = templates['content']
                        create_file(filename, content)
                        update_tailwind_config(filename, plugins, fonts)

                # Electron setup
                if template_file == 'electron.yaml' and use_electron:
                    click.echo(f'Creating Electron main.js file')
                    filename = templates['filename']
                    content = templates['content']
                    content = content.replace('{', '{{').replace('}', '}}')
                    content = content.format(app_name=app_name)
                    create_file(filename, content)

    click.echo(f"App '{app_name}' has been created successfully!")

    # Prompt to install environment
    install_env = click.confirm('Would you like to install python dependencies? (poetry required)', default=False)
    if install_env:
        if not check_poetry():
            poetry_install_instructions()
            return
        else:
            setup_environment()


def create_file(filename, content=''):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        f.write(content)


if __name__ == '__main__':
    create_app()
