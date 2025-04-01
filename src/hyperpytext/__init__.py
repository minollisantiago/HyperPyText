import os
import yaml
import typer
from datetime import datetime
from importlib import resources
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm
from rich.table import Table
from rich import print as rprint
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
from hyperpytext.utils.bun_utils import (
    check_bun,
    bun_install_instructions,
    setup_vite_bun,
    setup_tailwind_bun,
    setup_shadcn_bun,
)

#APP SETUP
# TODO: Cleanup the code on this script, server first, then client, too much repeated code
# TODO: Make the server template more precise: app / library
# TODO: Add some default shadcn components, at least examples
# TODO: Make a reference to the host and port on this file to reference on the vite server proxy and .env file
# TODO: Handle all authentication redirects, at least to specific endpoints, use piccolo docs for reference (all their auth endpoints have redirects)
# TODO: Move the root route to a new yaml file: routes_root.yaml

#DOCS
# TODO: Update docs with auth setup (backend) including migrations

app = typer.Typer(help="Create a new HyperPy application")
console = Console()

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

@app.command()
def main(app_name: str):
    """Create a new HyperPy application with FastAPI backend and React frontend."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        # Server setup
        server_task = progress.add_task("🐍 Setting up the Python web server...", total=None)
        
        templates_dir = get_template_path('react/server')

        # Prompt for Piccolo auth
        piccolo_auth = Confirm.ask("Would you like to include authentication with Piccolo?", default=False)
        
        # Prompt for Piccolo app example
        piccolo_example = Confirm.ask("Would you like to include a Piccolo db app example for SQLite?", default=False)

        # Start populating the project folder
        console.print(Panel(f"Creating a new HyperPy app in {os.path.join(os.getcwd(), app_name)}"))
        console.print("⌛ This process might take a few minutes. Please be patient.")

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
                        console.print("✔ Created app files")
                        for template in templates:
                            filename = template['filename']
                            content = template['content']
                            create_file(filename, content)

                    # Api
                    if template_file == 'api.yaml':
                        console.print("✔ Created fastApi routes example")
                        for template in templates:
                            filename = template['filename']
                            content = template['content']
                            create_file(filename, content)

                    # Db base
                    if template_file in db_files:
                        console.print("✔ Created piccolo database files")
                        for template in templates:
                            filename = template['filename']
                            content = template['content']
                            create_file(filename, content)

                    # Db example
                    if template_file == 'db_primary_example.yaml' and piccolo_example:
                        console.print("✔ Created a piccolo database example")
                        migrations_file_name = f"primary_{current_time.strftime('%Y_%m_%dt%H_%M_%S_%f')}.py"
                        for template in templates:
                            filename = template['filename'].format(filename=migrations_file_name)
                            content = template['content'].replace('{migrations_timestamp}', migrations_timestamp)
                            create_file(filename, content)

                    # Authentication
                    if piccolo_auth:
                        # Db
                        if template_file == 'db_auth.yaml':
                            console.print("✔ Created piccolo_api database dependencies")
                            migrations_file_name = f"auth_{current_time.strftime('%Y_%m_%dt%H_%M_%S_%f')}.py"
                            for template in templates:
                                filename = template['filename'].format(filename=migrations_file_name)
                                content = template['content'].replace('{migrations_timestamp}', migrations_timestamp)
                                create_file(filename, content)

                        # Routes
                        if template_file == 'routes_auth.yaml':
                            console.print("✔ Created authentication routes.")
                            for template in templates:
                                filename = template['filename']
                                content = template['content']
                                create_file(filename, content)

                        # Route Models (types)
                        if template_file == 'routes_models.yaml':
                            console.print("✔ Created route response models")
                            for template in templates:
                                filename = template['filename']
                                content = template['content']
                                create_file(filename, content)

                    # Utils files
                    if template_file == 'utils.yaml':
                        console.print("✔ Created app files")
                        for template in templates:
                            filename = template['filename']
                            content = template['content']
                            create_file(filename, content)

                    # Root files
                    if template_file in root_files:
                        filename = templates['filename']
                        console.print(f"✔ Created {filename}")
                        content = templates['content']
                        create_file(filename, content)

        progress.update(server_task, completed=True)

        # Client setup
        client_task = progress.add_task("⚛️ Setting up the React client app...", total=None)
        
        templates_dir = get_template_path('react/client')
        client_dir = os.path.join(app_dir, 'client')

        # Prompt for Tailwind CSS and plugins
        plugins = []
        tailwind = Confirm.ask("Would you like to use Tailwind CSS?", default=False)
        if tailwind:
            for plugin in ['forms', 'typography', 'container-queries']:
                if Confirm.ask(f"Would you like to install the Tailwind {plugin} plugin?", default=False):
                    plugins.append(plugin)

        # Prompt for custom fonts
        fonts = False
        if tailwind != 'none':
            fonts = Confirm.ask("Would you like to install Geist fonts?", default=False)

        # Prompt for Shadcn UI
        shadcn_ui = False
        if tailwind != 'none':
            shadcn_ui = Confirm.ask("Would you like to install Shadcn UI components?", default=False)

        # Try to use bun first, fall back to npm if not available
        if not check_bun():
            if not check_npm():
                npm_install_instructions()
                return
            else:
                # Setup Vite and the react client with npm
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
                                    console.print("✔ Updated tailwind.config.js")
                                    filename = templates['filename']
                                    content = templates['content']
                                    create_file(filename, content)
                                    update_tailwind_config(filename, plugins, fonts)

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

                    # Setup Shadcn UI if selected
                    if shadcn_ui:
                        setup_shadcn_ui(client_dir)

                    os.chdir(app_dir)
        else:
            # Setup Vite and the react client with bun
            setup_vite_bun(app_dir, template='react', use_typescript=True)

            # Setup Tailwind if selected
            if tailwind:
                setup_tailwind_bun(client_dir, plugins, fonts)

                for template_file in os.listdir(templates_dir):
                    if template_file.endswith('.yaml'):
                        with open(os.path.join(templates_dir, template_file), 'r') as file:
                            templates = yaml.safe_load(file)

                            # Tailwind config update
                            if template_file == 'tailwind.config.js.yaml':
                                console.print("✔ Updated tailwind.config.js")
                                filename = templates['filename']
                                content = templates['content']
                                create_file(filename, content)
                                update_tailwind_config(filename, plugins, fonts)

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

                # Setup Shadcn UI if selected
                if shadcn_ui:
                    setup_shadcn_bun(client_dir)

                os.chdir(app_dir)

        progress.update(client_task, completed=True)

    # Task complete message
    console.print(Panel(f"App '{app_name}' has been created successfully!", style="bold green"))

    # Create tables for scripts
    server_table = Table(title="🐍 Python Server Scripts", show_header=True, header_style="bold magenta")
    server_table.add_column("Command", style="cyan")
    server_table.add_column("Description", style="green")
    server_table.add_column("Directory", style="yellow")

    server_table.add_row(
        "uv run run_server.py",
        "Start Python server",
        "./server"
    )
    server_table.add_row(
        "uv run run_server.py --reload",
        "Start Python development server",
        "./server"
    )
    server_table.add_row(
        "uvicorn src.app:app",
        "Start Python server with Uvicorn",
        "./server"
    )
    server_table.add_row(
        "uvicorn src.app:app --reload",
        "Start Python development server with Uvicorn",
        "./server"
    )

    client_table = Table(title="⚛️ React Client Scripts", show_header=True, header_style="bold magenta")
    client_table.add_column("Command", style="cyan")
    client_table.add_column("Description", style="green")
    client_table.add_column("Directory", style="yellow")

    if check_bun():
        client_table.add_row(
            "bun run start",
            "Start Vite development server",
            "./client"
        )
        client_table.add_row(
            "bun run build",
            "Build Vite production bundle",
            "./client"
        )
        if tailwind:
            client_table.add_row(
                "bun run build-css",
                "Build Tailwind CSS",
                "./client"
            )
            client_table.add_row(
                "bun run watch-css",
                "Watch and build Tailwind CSS changes",
                "./client"
            )
    else:
        client_table.add_row(
            "npm run start",
            "Start Vite development server",
            "./client"
        )
        client_table.add_row(
            "npm run build",
            "Build Vite production bundle",
            "./client"
        )
        if tailwind:
            client_table.add_row(
                "npm run build-css",
                "Build Tailwind CSS",
                "./client"
            )
            client_table.add_row(
                "npm run watch-css",
                "Watch and build Tailwind CSS changes",
                "./client"
            )

    console.print("\n")
    console.print(server_table)
    console.print("\n")
    console.print(client_table)
    console.print("\n")
    console.print(Panel(f"App '{app_name}' created successfully!", style="bold green"))

if __name__ == "__main__":
    app()
