import os
import json
import subprocess
from rich.console import Console
from .npm_utils import check_system

console = Console()

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

        console.print("✔ Updated tsconfig.json with baseUrl and paths for Shadcn UI.")
    else:
        console.print("🚩 tsconfig.json not found. Skipping update.")


def update_tsconfig_app_json(project_dir):
    tsconfig_app_path = os.path.join(project_dir, 'tsconfig.app.json')
    if os.path.exists(tsconfig_app_path):
        new_config = {
            "compilerOptions": {
                "tsBuildInfoFile": "./node_modules/.tmp/tsconfig.app.tsbuildinfo",
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

        console.print("✔ Updated tsconfig.app.json with baseUrl and paths for Shadcn UI.")
    else:
        console.print("🚩 tsconfig.app.json not found. Skipping update.")


def install_types_node(project_dir):
    os.chdir(project_dir)
    npm_ = "npm.cmd" if check_system() == "windows" else "npm"
    try:
        subprocess.run([npm_, "install", "-D", "@types/node"], check=True)
        console.print("✔ Installed @types/node successfully.")
    except subprocess.CalledProcessError:
        console.print("🚩 Failed to install @types/node. Please check your npm installation.")


def setup_shadcn_npm(project_dir):
    update_tsconfig_json(project_dir)
    update_tsconfig_app_json(project_dir)
    install_types_node(project_dir)
    os.chdir(project_dir)
    npx_ = "npx.cmd" if check_system() == "windows" else "npx"
    console.print("Initializing Shadcn UI...")
    try:
        subprocess.run([npx_, "shadcn@latest", "init"], check=True)
    except subprocess.CalledProcessError:
        console.print(
            "🚩 Failed to initialize Shadcn UI. Please check your npm installation and try again."
        )
