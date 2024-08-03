# HyperPyText

HyperPyText is a Python-based tool for creating FastAPI application boilerplates with Tailwind CSS integration. It streamlines the process of setting up a new project by automating the creation of directory structures, configuration files, and initial code templates.

The idea is to set up a dashboard/app project as fast as possible and get working quickly. This boilerplate is a simpler version of [FastHTML](https://fastht.ml/). I just prefer to write the html/css myself.

Its important to note that fastHTML is more robust and complete, this is just a simplified version (no auth, database, ease of deployment tools), so its minimal as of now.

literally built it in a couple of hours with Claude 3.5 Sonnet from [Anthropic](https://www.anthropic.com/).

Ill add more documentation as it improves, this is the first iteration, built in a couple of hours.

Built on top of:
- [FastApi](https://fastapi.tiangolo.com/)
- [Jinja Templates](https://jinja.palletsprojects.com/en/3.1.x/templates/v)
- [HTMX](https://htmx.org/)
- [Tailwindcss](https://tailwindcss.com/)

## Features

- FastAPI application setup
- Tailwind CSS integration (npm or standalone)
- Jinja2 templating
- Customizable HTML templates
- Automatic router setup
- Asset management structure

## Installation

1. Clone the repository:

```
git clone https://github.com/yourusername/hyperpytext.git cd hyperpytext
```
2. Install the required packages:

```
pip install -r requirements.txt
```
## Usage

Run the `create-HyperPy-app.py {app name}` script to create a new application:

```
python create-HyperPy-app.py {app name}
```

You'll be prompted to enter:
- The app name
- The HTML file name
- The Tailwind CSS setup option (npm, standalone, or none)

## Project Structure

The generated project will have the following structure:

your_app_name/
├── api/
│   ├── routers/
│   │   ├── __init__.py
│   │   └── your_app_name_router.py
│   └── __init__.py
├── assets/
│   ├── css/
│   ├── docs/
│   ├── fonts/
│   ├── icons/
│   ├── images/
│   ├── js/
│   └── svg-loaders/
├── config/
├── db/
├── logs/
├── notebooks/
├── templates/
│   └── your_html_file.html
├── utils/
├── app.py
└── requirements.txt

### Tailwind CSS Integration
HyperPyText supports two methods of Tailwind CSS integration:

- NPM: Installs Tailwind CSS via npm and sets up the build process.

- Standalone: Downloads the Tailwind CSS standalone CLI for direct usage.

The setup process creates an ```input.css``` file and configures the build command to generate the final ```style.css``` file.

### Customization
You can customize the generated templates by modifying the YAML files in the ```templates/``` directory of the HyperPyText project.

### Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

### License
This project is licensed under the MIT License.