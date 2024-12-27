import os
import click
import subprocess
from .npm_utils import check_system, check_npm_package, update_package_json


def update_package_json_for_vite(project_dir):
    updates = {
        'scripts': {
            'start': 'vite',
            'build': 'vite build'
        }
    }
    update_package_json(project_dir, updates, subdir='client')


def configure_vite_proxy(project_dir):
    """
    Configure Vite's development server proxy settings to forward API requests to the FastAPI backend.

    This function updates the Vite config to proxy all /api/* requests to the FastAPI server running on 
    localhost:8000. This allows the React frontend to make API calls to relative URLs like '/api/...' 
    which will be automatically forwarded to the backend server.

    The FastAPI backend has routes defined under /api prefix, including the root route at /api/ which 
    returns a "Hello World" message.
    """
    vite_config_path = os.path.join(project_dir, 'client', 'vite.config.ts')
    if os.path.exists(vite_config_path):
        with open(vite_config_path, 'r') as f:
            config_content = f.read()

        updated_config = config_content.replace(
            "export default defineConfig({",
            (
            """
            export default defineConfig({
                server: {
                    proxy: {
                        '/api': 'http://localhost:8000',
                    },
                },
            """
            )
        )

        with open(vite_config_path, 'w') as f:
            f.write(updated_config)

        click.echo("✔ Updated Vite config with proxy settings.")
    else:
        click.echo("🚩 Vite config not found. Skipping proxy configuration.")


def remove_default_styles(project_dir):
    """Remove default style files created by Vite."""
    app_css_path = os.path.join(project_dir, 'client', 'src', 'App.css')
    index_css_path = os.path.join(project_dir, 'client', 'src', 'index.css')

    if os.path.exists(app_css_path):
        os.remove(app_css_path)
        click.echo("✔ Removed default App.css file.")

    if os.path.exists(index_css_path):
        os.remove(index_css_path)
        click.echo("✔ Removed default index.css file.")


def setup_vite_npm(project_dir, template='react', use_typescript=True):
    os.chdir(project_dir)
    npm_ = "npm.cmd" if check_system() == "windows" else "npm"
    if not check_npm_package('vite'):
        click.echo("Setting up Vite...")
        template_with_ts = f"{template}-ts" if use_typescript else template
        subprocess.run(
            [npm_, "create", "vite@latest", "client", "--", "--template", template_with_ts], 
            check=True
        )

        os.chdir("client")
        click.echo("Running npm install...")
        subprocess.run([npm_, "install"], check=True)

        update_package_json_for_vite(project_dir)
        configure_vite_proxy(project_dir)
        remove_default_styles(project_dir)

        os.chdir("..")
        click.echo("✔ Vite setup complete.")

