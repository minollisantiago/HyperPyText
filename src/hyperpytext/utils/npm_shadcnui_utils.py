import os
import json
import click
import subprocess
from .npm_utils import check_system


def update_tsconfig_json(project_dir):
    tsconfig_path = os.path.join(project_dir, 'tsconfig.json')
    if os.path.exists(tsconfig_path):
        with open(tsconfig_path, 'r') as f:
            tsconfig = json.load(f)

        if 'compilerOptions' not in tsconfig:
            tsconfig['compilerOptions'] = {}

        tsconfig['compilerOptions']['baseUrl'] = '.'
        tsconfig['compilerOptions']['paths'] = {
            "@/*": ["./src/*"]
        }

        with open(tsconfig_path, 'w') as f:
            json.dump(tsconfig, f, indent=2)

        click.echo("Updated tsconfig.json with baseUrl and paths for Shadcn UI.")
    else:
        click.echo("tsconfig.json not found. Skipping update.")


def update_tsconfig_app_json(project_dir):
    tsconfig_app_path = os.path.join(project_dir, 'tsconfig.app.json')
    if os.path.exists(tsconfig_app_path):
        new_config = {
            "compilerOptions": {
                "target": "ES2020",
                "useDefineForClassFields": True,
                "lib": ["ES2020", "DOM", "DOM.Iterable"],
                "module": "ESNext",
                "skipLibCheck": True,
                "moduleResolution": "Bundler",
                "allowImportingTsExtensions": True,
                "isolatedModules": True,
                "moduleDetection": "force",
                "noEmit": True,
                "jsx": "react-jsx",
                "strict": True,
                "noUnusedLocals": True,
                "noUnusedParameters": True,
                "noFallthroughCasesInSwitch": True,
                "noUncheckedSideEffectImports": True,
                "baseUrl": ".",
                "paths": {
                    "@/*": ["./src/*"]
                }
            },
            "include": ["src"]
        }

        with open(tsconfig_app_path, 'w') as f:
            json.dump(new_config, f, indent=2)

        click.echo("Updated tsconfig.app.json with baseUrl and paths for Shadcn UI.")
    else:
        click.echo("tsconfig.app.json not found. Skipping update.")


def install_types_node(project_dir):
    os.chdir(project_dir)
    npm_ = "npm.cmd" if check_system() == "windows" else "npm"
    try:
        subprocess.run([npm_, "install", "-D", "@types/node"], check=True)
        click.echo("Installed @types/node successfully.")
    except subprocess.CalledProcessError:
        click.echo("Failed to install @types/node. Please check your npm installation.")


def update_vite_config(project_dir):
    vite_config_path = os.path.join(project_dir, 'vite.config.ts')
    if os.path.exists(vite_config_path):
        new_config = (
"""
import path from "path"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"

export default defineConfig({
plugins: [react()],
resolve: {
    alias: {
    "@": path.resolve(__dirname, "./src"),
    },
},
server: {
    proxy: {
        '/api': 'http://localhost:8000',
    },
},
})
"""
        )
        with open(vite_config_path, 'w') as f:
            f.write(new_config)
        click.echo("Updated vite.config.ts for Shadcn UI.")
    else:
        click.echo("vite.config.ts not found. Skipping update.")


def setup_shadcn_ui(project_dir):
    update_tsconfig_json(project_dir)
    update_tsconfig_app_json(project_dir)
    install_types_node(project_dir)
    update_vite_config(project_dir)

    os.chdir(project_dir)
    npx_ = "npx.cmd" if check_system() == "windows" else "npx"
    click.echo("Initializing Shadcn UI...")
    try:
        subprocess.run([npx_, "shadcn@latest", "init"], check=True)
    except subprocess.CalledProcessError:
        click.echo(
            "Failed to initialize Shadcn UI. Please check your npm installation and try again."
        )
