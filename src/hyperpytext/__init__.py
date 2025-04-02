import os
import yaml
import typer
from datetime import datetime
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Confirm
from rich.console import Console
#from rich.progress import Progress, SpinnerColumn, TextColumn
from hyperpytext.utils.npm_shadcnui_utils import setup_shadcn_ui
from hyperpytext.utils.npm_tailwind_utils import setup_tailwind_npm
from hyperpytext.utils.npm_vite_utils import setup_vite_npm, configure_vite
from hyperpytext.utils.npm_utils import check_npm, npm_install_instructions
from hyperpytext.utils.templates_utils import create_file, SERVER_TEMPLATES_PATH, create_client_files
from hyperpytext.utils.uv_utils import SERVER_DEPENDENCIES, check_uv, setup_uv_environment, uv_install_instructions

#APP SETUP
# TODO: Make the server template more precise: app / library
# TODO: Add some default shadcn components, at least examples
# TODO: Make a reference to the host and port on this file to reference on the vite server proxy and .env file
# TODO: Handle all authentication redirects, at least to specific endpoints, use piccolo docs for reference (all their auth endpoints have redirects)
# TODO: Move the root route to a new yaml file: routes_root.yaml

app = typer.Typer(help="Create a new HyperPy application")
console = Console()

HEADER = """[bold cyan]
██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗ ██████╗ ██╗   ██╗████████╗███████╗██╗  ██╗████████╗
██║  ██║╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔══██╗╚██╗ ██╔╝╚══██╔══╝██╔════╝╚██╗██╔╝╚══██╔══╝
███████║ ╚████╔╝ ██████╔╝█████╗  ██████╔╝██████╔╝ ╚████╔╝    ██║   █████╗   ╚███╔╝    ██║
██╔══██║  ╚██╔╝  ██╔═══╝ ██╔══╝  ██╔══██╗██╔═══╝   ╚██╔╝     ██║   ██╔══╝   ██╔██╗    ██║
██║  ██║   ██║   ██║     ███████╗██║  ██║██║        ██║      ██║   ███████╗██╔╝ ██╗   ██║
╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝        ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝   ╚═╝   [/bold cyan]

[bold blue]🚀 Create modern web applications with Python and React[/bold blue]
[bold green]🔗 Project repo: https://github.com/minollisantiago/hyperpytext[/bold green]
"""

@app.command()
def main(app_name: str):
    """Create a new HyperPy application with FastAPI backend and React frontend."""
    console.print(HEADER)
    console.print(Panel(f"Creating a new HyperPy app in {os.path.join(os.getcwd(), app_name)}"))

    #Create app directory
    os.makedirs(app_name, exist_ok=True)
    app_dir = os.path.abspath(app_name)

    # Piccolo (db) setup
    piccolo_auth = Confirm.ask("Would you like to include authentication with Piccolo?", default=False)
    piccolo_example = Confirm.ask("Would you like to include a Piccolo db app example for SQLite?", default=False)

    # Prompt for custom fonts: geist
    fonts = Confirm.ask("Would you like to install Geist fonts?", default=False)

    # Prompt for Shadcn UI
    shadcn_ui = Confirm.ask("Would you like to install Shadcn UI components?", default=False)

    console.print("⌛ This process might take a bit. Please be patient.")

    #Progress instance
    #progress = Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console)
    #with progress:

    ## STEP1: Server setup
    #server_task = progress.add_task("🐍 Setting up the Python web server...", total=None)

    # Create server directory
    server_dir = os.path.join(app_dir, 'server')
    os.makedirs(server_dir, exist_ok=True)

    # Uv package manager setup
    os.chdir(server_dir)
    if not check_uv():
        uv_install_instructions()
        return
    setup_uv_environment(dependencies=SERVER_DEPENDENCIES)
    os.chdir(app_dir)

    # Setup server folders
    folders = {'server/src/app': ['api/routes', 'db', 'utils']}
    for base, subdirs in folders.items():
        for subdir in subdirs:
            os.makedirs(os.path.join(base, subdir), exist_ok=True)

    # Setup root files
    root_files = [
        f'{filename}.yaml' for filename in [
            'env', 'envrc', 'init', 'readme', 'uvicorn', 'gitignore'
        ]
    ]

    # Setup database
    db_files = [f'db_{filename}.yaml' for filename in ['primary', 'cache', 'queues',]]

    if piccolo_example:
        SERVER_DEPENDENCIES.append('faker~=30.1.0')

    # Database migrations timestamp
    current_time = datetime.now()
    migrations_timestamp = current_time.strftime("%Y-%m-%dT%H:%M:%S:%f")

    # Create files from templates
    for template_file in os.listdir(SERVER_TEMPLATES_PATH):
        if template_file.endswith('.yaml'):
            with open(os.path.join(SERVER_TEMPLATES_PATH, template_file), 'r') as file:
                templates = yaml.safe_load(file)

                # App files
                if template_file == 'app.yaml':
                    for template in templates:
                        filename = template['filename']
                        content = template['content']
                        create_file(filename, content)
                    console.print("✔ Created app files")

                # Api
                if template_file == 'api.yaml':
                    for template in templates:
                        filename = template['filename']
                        content = template['content']
                        create_file(filename, content)
                    console.print("✔ Created fastApi routes example")

                # Db base
                if template_file in db_files:
                    for template in templates:
                        filename = template['filename']
                        content = template['content']
                        create_file(filename, content)
                    console.print("✔ Created piccolo database files")

                # Db example
                if template_file == 'db_primary_example.yaml' and piccolo_example:
                    migrations_file_name = f"primary_{current_time.strftime('%Y_%m_%dt%H_%M_%S_%f')}.py"
                    for template in templates:
                        filename = template['filename'].format(filename=migrations_file_name)
                        content = template['content'].replace('{migrations_timestamp}', migrations_timestamp)
                        create_file(filename, content)
                    console.print("✔ Created a piccolo database example")

                # Authentication
                if piccolo_auth:
                    # Db
                    if template_file == 'db_auth.yaml':
                        migrations_file_name = f"auth_{current_time.strftime('%Y_%m_%dt%H_%M_%S_%f')}.py"
                        for template in templates:
                            filename = template['filename'].format(filename=migrations_file_name)
                            content = template['content'].replace('{migrations_timestamp}', migrations_timestamp)
                            create_file(filename, content)
                        console.print("✔ Created piccolo_api database dependencies")

                    # Routes
                    if template_file == 'routes_auth.yaml':
                        for template in templates:
                            filename = template['filename']
                            content = template['content']
                            create_file(filename, content)
                        console.print("✔ Created authentication routes.")

                    # Route Models (types)
                    if template_file == 'routes_models.yaml':
                        for template in templates:
                            filename = template['filename']
                            content = template['content']
                            create_file(filename, content)
                        console.print("✔ Created route response models")

                # Utils files
                if template_file == 'utils.yaml':
                    for template in templates:
                        filename = template['filename']
                        content = template['content']
                        create_file(filename, content)
                    console.print("✔ Created utils files")

                # Root files
                if template_file in root_files:
                    filename = templates['filename']
                    content = templates['content']
                    create_file(filename, content)
                    console.print(f"✔ Created {filename}")

    #progress.update(server_task, completed=100)

    ## STEP2: Client setup
    #client_task = progress.add_task("⚛️ Setting up the React client app...", total=None)

    # Create client directory
    client_dir = os.path.join(app_dir, 'client')
    os.makedirs(client_dir, exist_ok=True)

    # Check for npm and setup client
    if not check_npm():
        npm_install_instructions()
        return

    # Setup Vite and the react client
    setup_vite_npm(app_dir, template='react', use_typescript=True)

    # Setup Tailwind if selected
    setup_tailwind_npm(client_dir, fonts)

    # Setup Shadcn UI if selected
    if shadcn_ui:
        setup_shadcn_ui(client_dir)

    # Configure Vite with all selected features
    configure_vite(client_dir, use_shadcn=shadcn_ui)

    # Create client files
    create_client_files(fonts=fonts)

    os.chdir(app_dir)
    #progress.update(client_task, completed=100)

    # Task complete message
    console.print(Panel(f"App '{app_name}' has been created successfully!", style="bold green"))

    # Create tables for scripts
    console.print("🐍 Python Server Scripts")
    server_table = Table(show_header=True, header_style="bold magenta")
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

    console.print("⚛️ React Client Scripts")
    client_table = Table(show_header=True, header_style="bold magenta")
    client_table.add_column("Command", style="cyan")
    client_table.add_column("Description", style="green")
    client_table.add_column("Directory", style="yellow")

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

if __name__ == "__main__":
    app()
