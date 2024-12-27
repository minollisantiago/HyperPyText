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
from hyperpytext.utils.npm_shadcnui_utils import setup_shadcn_ui
from hyperpytext.utils.npm_utils import check_npm, npm_install_instructions, check_npm_package
from hyperpytext.utils.npm_electron_utils import setup_electron_npm
from hyperpytext.utils.poetry_utils import check_poetry, setup_poetry_environment, poetry_install_instructions
from hyperpytext.utils.uv_utils import check_uv, setup_uv_environment, uv_install_instructions
from hyperpytext.utils.npm_vite_utils import setup_vite_npm

#APP SETUP
# TODO: Cleanup the code on this script, server first, then client, too much repeated code
# TODO: Make the server template more precise: app / library
# TODO: I might remove poetry alltogether and focus on uv for package and project management
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
    "jinja2~=3.1.2",
    "ipython~=8.28.0",
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

    # Prompt for App backend project manager
    project_manager = click.prompt(
        'Select a python project manager',
        type=click.Choice(['poetry', 'uv']),
        default='uv',
        show_default=True,
    )

    # Prompt for App frontend
    app_client = click.prompt(
        'Select a framework for the client',
        type=click.Choice(['react', 'vanilla']),
        default='react',
        show_default=True,
    )

    ###### PYTHON + REACT APP SETUP ######
    if app_client == 'react':

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

        if project_manager == 'uv':
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

                    # Poetry config update
                    if template_file == 'pyproject.yaml' and project_manager == 'poetry':
                        filename = templates['filename']
                        content = templates['content']
                        db_example_dependencies = 'faker = "^30.1.0"' if piccolo_example else ''
                        content = content.format(
                            app_name=app_name,
                            db_example_dependencies=db_example_dependencies
                        )
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

                            # Tailwind globals.css
                            else:
                                filename = templates['filename']
                                click.echo(f'✔ Created {filename}')
                                content = templates['content']
                                create_file(filename, content)

                # Setup Shadcn UI if selected
                if shadcn_ui:
                    setup_shadcn_ui(client_dir)

                os.chdir(app_dir)

        # Prompt to install environment
        if project_manager == 'poetry':
            install_env = click.confirm(
                'Would you like to install python dependencies? (poetry required)',
                default=False
            )
            if install_env:
                if not check_poetry():
                    poetry_install_instructions()
                    return
                else:
                    server_dir = os.path.join(os.getcwd(), 'server')
                    os.chdir(server_dir)
                    setup_poetry_environment()
                    os.chdir(app_dir)

        # Show available npm scripts
        click.echo("\n📦 Available npm scripts:")
        click.echo(click.style("+", fg="#5cf19e") + "  npm run start    - Start Vite development server")
        click.echo(click.style("+", fg="#5cf19e") + "  npm run build    - Build Vite production bundle")
        if tailwind:
            click.echo(click.style("+", fg="#5cf19e") + "  npm run build-css - Build Tailwind CSS")
            click.echo(click.style("+", fg="#5cf19e") + "  npm run watch-css - Watch and build Tailwind CSS changes")

        # Task complete message
        click.echo(click.style("Success!", fg="#5cf19e") + f" App '{app_name}' has been created successfully!")

    ###### PYTHON + VANILLA JS APP SETUP ######
    elif app_client == 'vanilla':

        templates_dir = get_template_path('vanilla')

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
        click.echo(f"\n🚀 Creating a new HyperPy app in {os.path.join(os.getcwd(), app_name)}")
        click.echo("⌛ This process might take a few minutes. Please be patient.")

        # Project structure
        os.makedirs(app_name, exist_ok=True)
        app_dir = os.path.abspath(app_name)

        # Setup project
        os.chdir(app_dir)

        if piccolo_example:
            server_dependencies.append('faker~=30.1.0')

        if project_manager == 'uv':
            if not check_uv():
                uv_install_instructions()
                return
            else:
                setup_uv_environment(dependencies=server_dependencies)

        # Setup server folders
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
            if not check_npm_package('tailwindcss'):
                click.echo("Tailwind CSS is not installed. It will be installed during app setup.")
        elif tailwind == 'standalone':
            if not check_tailwind_standalone():
                click.echo("Tailwind CSS standalone CLI is not found. It will be downloaded during app setup.")

        # Setup Tailwind if selected
        if tailwind == 'npm':
            setup_tailwind_npm(app_dir, plugins, fonts)
        elif tailwind == 'standalone':
            setup_tailwind_standalone(app_dir)

        # Setup Electron if selected
        if use_electron:
            click.echo("⌛ Setting up Electron...")
            setup_electron_npm(app_dir, app_name)
            click.echo("✔ Electron setup complete.")

        # Setup Piccolo Database
        db_files = [f'db_{filename}.yaml' for filename in ['primary', 'cache', 'queues',]]

        # Database migrations timestamp
        current_time = datetime.now()
        migrations_timestamp = current_time.strftime("%Y-%m-%dT%H:%M:%S:%f")

        # Setup Root files & tailwind input.css
        root_files = [
            f'{filename}.yaml' for filename in ['env', 'envrc', 'init', 'readme', 'uvicorn', 'gitignore', 'input_css',]
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
                            content = template['content'].format(html_filename=html_filename)
                            create_file(filename, content)

                    # Index starter HTML5 template
                    if template_file == 'index.yaml':
                        click.echo(f'✔ Created {html_filename}.html file')
                        filename = templates['filename'].format(filename=html_filename)
                        content = templates['content'].format(title=html_filename)
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

                    # Root files & tailwind input.css
                    if template_file in root_files:
                        filename = templates['filename']
                        click.echo(f'✔ Created {filename}')
                        content = templates['content']
                        create_file(filename, content)

                    # Poetry config update
                    if template_file == 'pyproject.yaml' and project_manager == 'poetry':
                        filename = templates['filename']
                        content = templates['content']
                        db_example_dependencies = 'faker = "^30.1.0"' if piccolo_example else ''
                        content = content.format(
                            app_name=app_name,
                            db_example_dependencies=db_example_dependencies
                        )
                        create_file(filename, content)

                    # Tailwind config update
                    if template_file == 'tailwind_config.yaml':
                        if tailwind != 'none':
                            click.echo(f'✔ Updated tailwind.config.js')
                            filename = templates['filename']
                            content = templates['content']
                            create_file(filename, content)
                            update_tailwind_config(filename, plugins, fonts)

                    # Electron setup
                    if template_file == 'electron.yaml' and use_electron:
                        click.echo(f'✔ Created Electron main.js file')
                        filename = templates['filename']
                        content = templates['content']
                        content = content.replace('{', '{{').replace('}', '}}')
                        content = content.format(app_name=app_name)
                        create_file(filename, content)

        # Task complete message
        click.echo(click.style("Success!", fg="#5cf19e") + f" App '{app_name}' has been created successfully!")

        # Prompt to install environment
        if project_manager == 'poetry':
            install_env = click.confirm(
                'Would you like to install python dependencies? (poetry required)',
                default=False
            )
            if install_env:
                if not check_poetry():
                    poetry_install_instructions()
                    return
                else:
                    setup_poetry_environment()
