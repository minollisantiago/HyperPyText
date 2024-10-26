import os
import json
import click
import subprocess
from .npm_utils import check_system, check_npm_package


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
        os.chdir("..")
        click.echo("Vite setup complete.")


def update_package_json_for_vite(project_dir):
    client_dir = os.path.join(project_dir, 'client')
    client_package_path = os.path.join(client_dir, 'package.json')
    
    if os.path.exists(client_package_path):
        with open(client_package_path, 'r') as f:
            client_package = json.load(f)
        
        client_package['scripts']['start'] = 'vite'
        client_package['scripts']['build'] = 'vite build'
        
        with open(client_package_path, 'w') as f:
            json.dump(client_package, f, indent=2)
        
        click.echo("Updated client package.json with Vite scripts.")
    else:
        click.echo("Client package.json not found. Skipping package.json update.")


def configure_vite_proxy(project_dir):
    vite_config_path = os.path.join(project_dir, 'client', 'vite.config.js')
    if os.path.exists(vite_config_path):
        with open(vite_config_path, 'r') as f:
            config_content = f.read()
        
        updated_config = config_content.replace(
            "export default defineConfig({",
            """export default defineConfig({
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },"""
        )
        
        with open(vite_config_path, 'w') as f:
            f.write(updated_config)
        
        click.echo("Updated Vite config with proxy settings.")
    else:
        click.echo("Vite config not found. Skipping proxy configuration.")

