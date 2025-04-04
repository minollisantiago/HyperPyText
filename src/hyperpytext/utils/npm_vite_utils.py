import os
import subprocess
from rich.console import Console
from .npm_utils import check_system, check_npm_package, update_package_json

console = Console()

def update_package_json_for_vite(project_dir):
    updates = {
        'scripts': {
            'dev': 'vite',
            'build': 'vite build',
            'preview': 'vite preview'
        }
    }
    update_package_json(project_dir, updates)

def configure_vite(project_dir: str, *, use_shadcn: bool = False):
    """
    Configure Vite with all necessary plugins and settings.

    Args:
        project_dir: The project directory where vite.config.ts should be created/updated
        use_shadcn: Whether to include Shadcn UI configuration (includes path aliases)

    Notes on the last step:
    We configure Vite's development server proxy settings to forward API requests to the FastAPI backend.

    This function updates the Vite config to proxy all /api/* requests to the FastAPI server running on
    localhost:8000. This allows the React frontend to make API calls to relative URLs like '/api/...'
    which will be automatically forwarded to the backend server.

    The FastAPI backend has routes defined under /api prefix, including the root route at /api/ which
    returns a "Hello World" message.
    """
    vite_config_path = os.path.join(project_dir, 'vite.config.ts')

    # Build imports section
    imports = [
        'import react from "@vitejs/plugin-react"',
        'import { defineConfig } from "vite"',
        'import tailwindcss from "@tailwindcss/vite"'
    ]

    if use_shadcn:
        imports.append('import path from "path"')

    # Build plugins section - Tailwind is always included
    plugins = ['react()', 'tailwindcss()']

    # Build config object
    config_parts = []

    # Add plugins
    config_parts.append(f"  plugins: [{', '.join(plugins)}],")

    # Add path aliases if using Shadcn
    if use_shadcn:
        config_parts.append("""  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },""")

    # Add API proxy configuration
    config_parts.append("""  server: {
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },""")

    # Combine everything into the final config
    vite_config = f"""
{chr(10).join(imports)}

export default defineConfig({{
{chr(10).join(config_parts)}
}})
"""

    with open(vite_config_path, 'w') as f:
        f.write(vite_config)

    console.print("✔ Updated Vite configuration.")

def remove_default_styles(project_dir):
    """Remove default style files created by Vite."""
    app_css_path = os.path.join(project_dir, 'src', 'App.css')

    if os.path.exists(app_css_path):
        os.remove(app_css_path)
        console.print("✔ Removed default App.css file.")

def setup_vite_npm(project_dir, app_name = 'client', template='react', use_typescript=True, shadcn=False):
    """Setup a new Vite project using npm."""
    os.chdir(project_dir)
    npm_ = "npm.cmd" if check_system() == "windows" else "npm"
    if not check_npm_package('vite'):
        console.print("Setting up Vite...")
        template_with_ts = f"{template}-ts" if use_typescript else template
        subprocess.run(
            [npm_, "create", "vite@latest", app_name, "--", "--template", template_with_ts],
            check=True
        )

        # Install dependencies
        os.chdir(app_name)
        console.print("Running npm install...")
        subprocess.run([npm_, "install"], check=True)

        # Update package.json with npm-specific scripts
        updates = {
            'scripts': {
                'dev': 'vite',
                'build': 'vite build',
                'preview': 'vite preview'
            }
        }
        update_package_json(project_dir, updates, subdir=app_name)
        configure_vite(project_dir, use_shadcn=shadcn)
        remove_default_styles(project_dir)

        os.chdir("..")
        console.print("✔ Vite setup complete.")

