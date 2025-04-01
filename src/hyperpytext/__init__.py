import os
import yaml
import click
from datetime import datetime
from importlib import resources
from hyperpytext.utils.npm_tailwind_utils import (
    check_tailwind_standalone,
    setup_tailwind_npm,
    setup_tailwind_standalone,
    update_tailwind_config,
)
from hyperpytext.utils.npm_vite_utils import setup_vite_npm
from hyperpytext.utils.npm_shadcnui_utils import setup_shadcn_ui
from hyperpytext.utils.npm_electron_utils import setup_electron_npm
from hyperpytext.utils.uv_utils import check_uv, setup_uv_environment, uv_install_instructions
from hyperpytext.utils.npm_utils import check_npm, npm_install_instructions, check_npm_package

#APP SETUP
# TODO: Cleanup the code on this script, server first, then client, too much repeated code
# TODO: Make the server template more precise: app / library
# TODO: Add some default shadcn components, at least examples
# TODO: Make a reference to the host and port on this file to reference on the vite server proxy and .env file
# TODO: Handle all authentication redirects, at least to specific endpoints, use piccolo docs for reference (all their auth endpoints have redirects)
# TODO: Move the root route to a new yaml file: routes_root.yaml

#DOCS
# TODO: Update docs with the new project structure (react app)
# TODO: Update docs with auth setup (backend) including migrations
# TODO: Update docs with all shortcut scripts created on package.json


def get_template_path(template_path: str) -> str:
    """Get the absolute path to a template directory."""
    with resources.path('hyperpytext.templates', template_path) as path:
        return str(path)


def create_file(filename, content=''):
    """Writes the template file"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        f.write(content)


server_dependencies = [
    "uvicorn~=0.32.0",
    "fastapi~=0.115.0",
    "python-dotenv~=1.0.0",
    "piccolo[all]~=1.22.0",
    "piccolo-api~=1.5.2",
    "yagmail~=0.15.293"
]

@click.command()
@click.argument('app_name')
def main(app_name:str) -> None:

    ###### PYTHON + REACT APP SETUP ######

    ### Server setup ###

    click.echo(f"\n🐍 Setting up the python web server:")

    templates_dir = get_template_path('react/server')

    # Prompt for Piccolo auth
    piccolo_auth = click.confirm('Would you like to include authentication with Piccolo?', default=False)

    # Prompt for Piccolo app example
    piccolo_example = click.confirm('Would you like to include a Piccolo db app example for SQLite?', default=False)

    # Start populating the project folder
    click.echo(f"\nCreating a new HyperPy app in {os.path.join(os.getcwd(), app_name)}")
    click.echo("⌛ This process might take a few minutes. Please be patient.")

    # Project structure
    os.makedirs(app_name, exist_ok=True)
    app_dir = os.path.abspath(app_name)
    server_dir = os.path.join(app_dir, 'server')
    os.makedirs(server_dir, exist_ok=True)

    # Setup project
    os.chdir(server_dir)

    if piccolo_example:
        server_dependencies.append('faker~=30.1.0')

    if not check_uv():
        uv_install_instructions()
        return
    else:
        setup_uv_environment(dependencies=server_dependencies)

    os.chdir(app_dir)

    # Setup server folders
    folders = {'server/src/app': ['api/routes', 'db', 'utils']}
    for base, subdirs in folders.items():
        for subdir in subdirs:
            os.makedirs(os.path.join(base, subdir), exist_ok=True)

    # Setup database
    db_files = [f'db_{filename}.yaml' for filename in ['primary', 'cache', 'queues',]]

    # Database migrations timestamp
    current_time = datetime.now()
    migrations_timestamp = current_time.strftime("%Y-%m-%dT%H:%M:%S:%f")

    # Setup root files
    root_files = [
        f'{filename}.yaml' for filename in ['env', 'envrc', 'init', 'readme', 'uvicorn', 'gitignore']
    ]

    # Create files from templates
    for template_file in os.listdir(templates_dir):
        if template_file.endswith('.yaml'):
            with open(os.path.join(templates_dir, template_file), 'r') as file:
                templates = yaml.safe_load(file)

                # App files
                if template_file == 'app.yaml':
                    click.echo('✔ Created app files')
                    for template in templates:
                        filename = template['filename']
                        content = template['content']
                        create_file(filename, content)

                # Api
                if template_file == 'api.yaml':
                    click.echo(f'✔ Created fastApi routes example')
                    for template in templates:
                        filename = template['filename']
                        content = template['content']
                        create_file(filename, content)

                # Db base
                if template_file in db_files:
                    click.echo('✔ Created piccolo database files')
                    for template in templates:
                        filename = template['filename']
                        content = template['content']
                        create_file(filename, content)

                # Db example
                if template_file == 'db_primary_example.yaml' and piccolo_example:
                    click.echo('✔ Created a piccolo database example')
                    migrations_file_name = f"primary_{current_time.strftime('%Y_%m_%dt%H_%M_%S_%f')}.py"
                    for template in templates:
                        filename = template['filename'].format(filename=migrations_file_name)
                        content = template['content'].replace('{migrations_timestamp}', migrations_timestamp)
                        create_file(filename, content)

                # Authentication
                if piccolo_auth:

                    # Db
                    if template_file == 'db_auth.yaml':
                        click.echo('✔ Created piccolo_api database dependencies')
                        migrations_file_name = f"auth_{current_time.strftime('%Y_%m_%dt%H_%M_%S_%f')}.py"
                        for template in templates:
                            filename = template['filename'].format(filename=migrations_file_name)
                            content = template['content'].replace('{migrations_timestamp}', migrations_timestamp)
                            create_file(filename, content)

                    # Routes
                    if template_file == 'routes_auth.yaml':
                        click.echo('✔ Created authentication routes.')
                        for template in templates:
                            filename = template['filename']
                            content = template['content']
                            create_file(filename, content)

                    # Route Models (types)
                    if template_file == 'routes_models.yaml':
                        click.echo('✔ Created route response models')
                        for template in templates:
                            filename = template['filename']
                            content = template['content']
                            create_file(filename, content)

                # Utils files
                if template_file == 'utils.yaml':
                    click.echo('✔ Created app files')
                    for template in templates:
                        filename = template['filename']
                        content = template['content']
                        create_file(filename, content)

                # Root files
                if template_file in root_files:
                    filename = templates['filename']
                    click.echo(f'✔ Created {filename}')
                    content = templates['content']
                    create_file(filename, content)

    ### Client setup ###

    click.echo(f"⚛️ Setting up the react client app...")

    templates_dir = get_template_path('react/client')
    client_dir = os.path.join(app_dir, 'client')

    # Prompt for Tailwind CSS and plugins
    plugins = []
    tailwind = click.confirm('Would you like to use Tailwind CSS?', default=False)
    if tailwind:
        for plugin in ['forms', 'typography', 'container-queries']:
            if click.confirm(f'Would you like to install the Tailwind {plugin} plugin?', default=False):
                plugins.append(plugin)

    # Prompt for custom fonts
    fonts = False
    if check_npm() and tailwind != 'none':
        fonts = click.confirm(f'Would you like to install Geist fonts?', default=False)

    # Prompt for Shadcn UI
    shadcn_ui = False
    if check_npm() and tailwind != 'none':
        shadcn_ui = click.confirm('Would you like to install Shadcn UI components?', default=False)

    # Setup NPM dependencies
    if not check_npm():
        npm_install_instructions()
        return
    else:
        # Setup Vite and the react client
        setup_vite_npm(app_dir, template='react', use_typescript=True)

        # Setup Tailwind if selected
        if tailwind:
            setup_tailwind_npm(client_dir, plugins, fonts)

            for template_file in os.listdir(templates_dir):
                if template_file.endswith('.yaml'):
                    with open(os.path.join(templates_dir, template_file), 'r') as file:
                        templates = yaml.safe_load(file)

                        # Tailwind config update
                        if template_file == 'tailwind.config.js.yaml':
                            click.echo(f'✔ Updated tailwind.config.js')
                            filename = templates['filename']
                            content = templates['content']
                            create_file(filename, content)
                            update_tailwind_config(filename, plugins, fonts)

                        # Geist fonts
                        if template_file == 'fonts.css.yaml':
                            if fonts:
                                filename = templates['filename']
                                click.echo(f'✔ Created {filename}')
                                content = templates['content']
                                create_file(filename, content)
                            else:
                                continue

                        # All files
                        else:
                            filename = templates['filename']
                            click.echo(f'✔ Created {filename}')
                            content = templates['content']
                            create_file(filename, content)

            # Setup Shadcn UI if selected
            if shadcn_ui:
                setup_shadcn_ui(client_dir)

            os.chdir(app_dir)

    # Task complete message
    click.echo(click.style(f" App '{app_name}' has been created successfully!", fg=(89,255,209)))

    click.echo("\n📦 Here is a list of available scripts:")

    #Server scripts
    click.echo(f"\n🐍 For the Python web server (run these from the backend folder, ./server):")
    click.echo(click.style("+", fg=(89,255,209)) + " uv run run_server.py - Start Python server")
    click.echo(click.style("+", fg=(89,255,209)) + " uv run run_server.py --reload - Start Python development server")
    click.echo(click.style("+", fg=(89,255,209)) + " uvicorn src.app:app - Start Python server with Uvicorn")
    click.echo(click.style("+", fg=(89,255,209)) + " uvicorn src.app:app --reload - Start Python development server with Uvicorn")

    #Client scripts
    click.echo(f"\n⚛️ For the Vite web server (run these from the client folder, ./client):")
    click.echo(click.style("+", fg=(89,255,209)) + " npm run start - Start Vite development server")
    click.echo(click.style("+", fg=(89,255,209)) + " npm run build - Build Vite production bundle")
    if tailwind:
        click.echo(click.style("+", fg=(89,255,209)) + " npm run build-css - Build Tailwind CSS")
        click.echo(click.style("+", fg=(89,255,209)) + " npm run watch-css - Watch and build Tailwind CSS changes")

    click.echo(f"App '{app_name}' created successfully!")