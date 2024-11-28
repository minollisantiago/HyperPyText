# HyperPyText

#### Python and react/vanilla javascript apps boilerplate to get your project started fast:fire: :rocket: :fire:

> [!NOTE]
> This is a work in progress, more documentation will be added as it improves, also undergoing iterations, so expect changes and outdated documentation.

<br>
<br>

![hyperpytext](./images/hyperpytext.png)

<br>
<br>

HyperPyText is a Python-based tool for creating fullstack applications. It streamlines the process of setting up a new project by automating the creation of directory structures, configuration files, and initial backend and frontend templates.

The idea is to set up a dashboard/app project as fast as possible and get working quickly.

Built on top of:

- [FastApi](https://fastapi.tiangolo.com/)
- [Piccolo ORM](https://piccolo-orm.readthedocs.io/en/latest/)
- [Piccolo API](https://piccolo-api.readthedocs.io/en/latest/)
- [SQLite](https://www.sqlite.org/index.html)
- [UV](https://docs.astral.sh/uv/)
- [React](https://react.dev/)
- [Shadcn](https://ui.shadcn.com/)
- [Tailwindcss](https://tailwindcss.com/)
- [Jinja Templates](https://jinja.palletsprojects.com/en/3.1.x/)
- [HTMX](https://htmx.org/)

## Features

**Backend:**

- FastAPI application setup
- [Piccolo ORM](https://piccolo-orm.readthedocs.io/en/latest/) setup with [SQLite](https://www.sqlite.org/index.html): example main database, cache database and queues database
- Authentication with [Piccolo API](https://piccolo-api.readthedocs.io/en/latest/), [fastapi](https://fastapi.tiangolo.com/) routes and tables
- [Uv](https://docs.astral.sh/uv/) or [Poetry](https://python-poetry.org/) for python dependency management
- Automatic project env with uv (prefered)
- Environment default variable configuration

**Frontend (react):**

- React + typescript setup with [vite](https://vitejs.dev/)
- [Shadcn](https://ui.shadcn.com/) setup with (in the future) custom components

**Frontend (Vanilla with htmx):**
- [htmx](https://htmx.org/) setup
- [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/) templating
- Customizable HTML templates
- Asset management structure

**Frontend (general):**

- Tailwind CSS integration + [plugins](https://tailwindcss.com/docs/plugins)
- Optional [Electron](https://www.electronjs.org/) setup for desktop applications
- Vercel [Geist](https://vercel.com/font) font (sans and mono)


## Installation

> [!IMPORTANT]
> You need to have uv installed to use this tool.
> For more information on how to install uv check [here](https://docs.astral.sh/uv/getting-started/installation/).
> You do not need to have python installed to install uv itself, which is pretty handy.

1. Clone the repository:

```bash
git clone https://github.com/yourusername/hyperpytext.git
```

2. Navigate to the package folder:

```bash
cd hyperpytext
```

3. Activate the environment and update/install the dependencies:

```bash
uv sync
```

> [!NOTE]
> Uv does not need to have python installed previously, it will handle the installation itself.

## Usage

Navigate to the folder where you want to create your project:

```bash
cd /path/to/your/new/app/folder
```

Activate the hyperpytext environment, this will depend on your shell, for a bash example:

```bash
source path/to/hyperpytext/.venv/bin/activate
```

Run the `create-hyperpy-app {app name}` command to create a new application on the current working directory:

```bash
create-hyperpy-app your_app_name
```

Follow the instructions on the terminal to choose the options you want for your project.

## Project Structure

> [!NOTE]
> Im only including the structure of the python + react client/server version, as it is the most comprehensive and polished one for now:

**General Project Structure:**

```
your_app_name/
├── server/               # Python FastAPI backend
│   ├── src/              # Server source code
│   ├── .env              # Server environment variables
│   ├── .envrc            # Direnv configuration
│   ├── .gitignore        # Server-specific gitignore
│   ├── README.md         # Server documentation
│   ├── pyproject.toml    # Project configuration
│   └── run_server.py     # Server entry point
│
├── client/                 # React frontend
│   ├── src/                # Client source code
│   ├── public/             # Static assets
│   ├── .gitignore          # Client-specific gitignore
│   ├── index.html          # HTML entry point
│   ├── package.json        # NPM dependencies and scripts
│   ├── tailwind.config.js  # Tailwind configuration
│   ├── tsconfig.json       # TypeScript configuration
│   └── vite.config.ts      # Vite configuration
```
**Python Server Structure:**

```
your_app_name/
├── server/
│   ├── src/
│   │   ├── app/
│   │   │   ├── api/
│   │   │   │   ├── routes/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── root.py
│   │   │   │   │   └── auth/
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── login.py
│   │   │   │   │       ├── logout.py
│   │   │   │   │       ├── register.py
│   │   │   │   │       └── session.py
│   │   │   │   ├── models/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── auth.py
│   │   │   │   └── __init__.py
│   │   │   ├── db/
│   │   │   │   ├── primary/
│   │   │   │   │   ├── migrations/
│   │   │   │   │   │   └── __init__.py
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── piccolo_app.py
│   │   │   │   │   ├── piccolo_conf.py
│   │   │   │   │   ├── tables.py
│   │   │   │   │   └── db_populate.py
│   │   │   │   ├── cache/
│   │   │   │   │   ├── migrations/
│   │   │   │   │   │   └── __init__.py
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── piccolo_app.py
│   │   │   │   │   └── piccolo_conf.py
│   │   │   │   ├── queues/
│   │   │   │   │   ├── migrations/
│   │   │   │   │   │   └── __init__.py
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── piccolo_app.py
│   │   │   │   │   └── piccolo_conf.py
│   │   │   │   ├── auth/
│   │   │   │   │   ├── migrations/
│   │   │   │   │   │   └── auth_{timestamp}.py
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── piccolo_app.py
│   │   │   │   │   ├── piccolo_conf.py
│   │   │   │   │   └── tables.py
│   │   │   │   └── __init__.py
│   │   │   └── utils/
│   │   │       └── __init__.py
│   ├── .env
│   ├── .envrc
│   ├── .gitignore
│   ├── README.md
│   ├── pyproject.toml
│   └── run_server.py
```

> [!NOTE]
> The client structure is the basic react + typescript vite setup, with shadcn and tailwind already installed if selected on the project creation.

## Server Templates

### SQLite with Piccolo ORM

#### Default Database Structure

HyperPyText uses [Piccolo ORM](https://piccolo-orm.com/) for database management with SQLite.

>[!NOTE]
> Postgress support will be added in the future, but for now SQLite is the only db with templates out of the box, as this is intended for small lightweight apps.

The project comes pre-configured with three separate database piccolo apps, each with its own SQLite database file:

1. Primary Database
2. Cache Database
3. Queues Database

This is the general structure of any of the apps from above:

```
src/app/db/
├── primary/
│   ├── migrations/
│   │   └── __init__.py
│   ├── __init__.py
│   ├── piccolo_app.py
│   ├── piccolo_conf.py
│   ├── tables.py
│   └── ...
```

Each of them is pre-built with the proper configuration, including `piccolo_app.py` files and all the necessary setup to start working with the piccolo CLI.

#### Primary Database example

If you choose to add the example piccolo app when prompted while creating the project, it will include a `tables.py` file with a pre-defined `Clients` table example. You can find it at `src/app/db/primary/tables.py`. 

The file will include a Clients piccolo table, with the following model: 

```python
from piccolo.table import Table
from piccolo.columns import Varchar, Timestamp

class Clients(Table, tablename="clients"):
    name = Varchar(length=100, unique=True, index=True)
    email = Varchar(length=100, unique=True, index=True)
    company = Varchar(length=100)
    role = Varchar(length=100)
    created_at = Timestamp(auto_now=True)
    updated_at = Timestamp(auto_now_add=True)
```

**Creating and running migrations**
Once you've created the project, you can create and run migrations for the primary database. First you need to navigate to the primary database folder:

```bash
cd src/app/db/primary
```

Then you can create and run migrations with the following commands:

```bash
piccolo migrations new primary
piccolo migrations forwards primary
```

If the app is registered in the `piccolo_conf.py` file, you only need to specify the app name on the migrations command(s), like on the example above.

You can check all the apps registered on the file as well by running this command:

```bash
piccolo show_all
```

You can also check all migrations that havent been run yet by running:

```bash
piccolo migrations check
```
>[!IMPORTANT]
>In order to run the migrations you will need to write the files yourself, as auto migrations are not supported for SQLite, see the Piccolo [migration docs](https://piccolo-orm.readthedocs.io/en/latest/piccolo/migrations/index.html) for more information.

Once you successfully run the initial migration you can run the following command from the terminal *(need to have the python environment activated with all the dependencies installed)*:

```bash
cd src/app/db/primary
python db_populate.py
```
With uv:

```bash
cd src/app/db/primary
uv run db_populate.py
```

This will populate the database with some random data so you can begin querying the database using the Piccolo CLI and its ipython shell. To activate the ipython shell run:

```bash
cd src/app/db/primary
piccolo shell run
```
Then you can query the database using the piccolo syntax, for example for a `SELECT * FROM clients` query the syntax would be:

```bash
await Clients.select()
```
> [!NOTE]
> For more Query types, go [here](https://piccolo-orm.readthedocs.io/en/latest/piccolo/query_types/index.html).

#### Piccolo CLI

Here is a general overview of the Piccolo CLI, for more information check the [Piccolo docs](https://piccolo-orm.readthedocs.io/en/latest/piccolo/getting_started/index.html):

1. Explore Piccolo CLI:
   To see all available Piccolo CLI commands with descriptions, run:
   ```bash
   piccolo --help
   ```
2. Start a Piccolo project:
   After creating your app, navigate to the project directory and run:
   ```bash
   piccolo project new --engine=sqlite
   ```
   This creates a `piccolo_conf.py` file in your project root.

4. Create a new Piccolo app:
   To create a new Piccolo app within your project, use the following command:
   ```bash
   piccolo app new [app_name] --root=./src/app/db
   ```
   This will create a new directory for your app with the necessary structure, including a `tables.py` file where you can define your database tables, and a `piccolo_migrations` folder where the migrations will be stored.

   After creating the app, make sure to register it in your `piccolo_conf.py` file by adding it to the `APP_REGISTRY`:
   ```python
   APP_REGISTRY = [
       "src.app.db.[app_name].piccolo_app",
       # ... other registered apps
   ]
   ```
4. Run migrations:
   After defining your tables, create and run migrations:
   ```bash
   piccolo migrations new [app_name]
   piccolo migrations forwards [app_name]
   ```
   If the app is registered in the piccolo_conf.py file, you only need to specify the app name on the migrations command(s), you can check all the apps registered on the file as well by running this command:

   ```bash
   piccolo show_all
   ```

   You can also check all migrations that havent been run yet by running:

   ```bash
   piccolo migrations check
   ```

#### Piccolo + FastAPI

To use Piccolo in your FastAPI endpoints, first import your tables and then use Piccolo's query API in your route handlers:

```python
from src.app.db.primary.tables import Clients

@app.get("/clients")
async def get_clients():
      return await Clients.select().run()
```

### Authentication (Piccolo)

**Structure**

If you choose to go with Piccoolo authentication, the project will have a folder inside the db folder with the following structure:

```
src/app/db/
├── auth/
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── auth_{timestamp}.py
│   ├── __init__.py
│   ├── piccolo_app.py
│   ├── piccolo_conf.py
│   └── tables.py
│...

```

**Session Auth**

Piccolo has a side project called piccolo-api that provides with some useful tools for ASGI applications, including built in authentication, admin interface and endpoints for authentication, **we will be using our own endpoints templates**.

Piccolo [recommends using session auth](https://piccolo-api.readthedocs.io/en/latest/which_authentication/index.html) for most apps, so we are going with that.

>[!NOTE]
>For a complete guide on how to set up session auth with piccolo api, read their [docs](https://piccolo-api.readthedocs.io/en/latest/session_auth/index.html).

Piccolo's session auth comes with a built in `SessionsBase` table to store the session tokens, and a `BaseUser` table to store user credentials. 

**Piccolo auth apps and tables**

Both apps are included by default in `src/app/db/auth/piccolo_conf.py`, so you can immediately start using them:

```python
from piccolo.conf.apps import AppRegistry
from piccolo.engine.sqlite import SQLiteEngine

DB = SQLiteEngine(path="auth_db.sqlite")

# A list of paths to piccolo apps
APP_REGISTRY = AppRegistry(
    apps=[
        "piccolo_app",
        "piccolo_api.session_auth.piccolo_app",
        "piccolo.apps.user.piccolo_app",
    ]
)
```

To create both tables using migrations, after the hyperpytext app is created, run the following command to setup the auth app:

```bash
piccolo migrations forwards user
piccolo migrations forwards session_auth
```

**Custom Tables**

I've included a new table called `PasswordResetToken` located at `src/app/db/auth/tables.py` to store the password reset tokens. 

It has the same structure as the `SessionsBase` table, but comes with a few methods of its own, and is intended to be used only for password reset. It is structured in a way that allows us to take advantage of the piccolo api session auth features without interfering with the `SessionsBase` table.

The template includes the migrations file for this table, so you can run the migrations like for any other piccolo table.

**Endpoints**

The app, if prompted to include auth, will come with custom fastapi template routes for authentication, including:

- login
- logout
- register
- change password
- password reset
- a `models.py` file with searializers for the request and response models

All of them are located at `src/app/api/routes/`.

## Client Templates

>[!IMPORTANT]
> The client templates are still under development, expect changes and outdated documentation.

### Tailwind CSS

HyperPyText supports two methods of Tailwind CSS integration:

- NPM: Installs Tailwind CSS via npm and sets up the build process.

- Standalone: Downloads the Tailwind CSS standalone CLI for direct usage.

The setup process creates an `globals.css` file and configures the build command to generate the final `style.css` file.

To build the css run:

```bash
npm run build-css
```
Alternatively you can use the npm run watch-css command to rebuild the css file when you make changes:

```bash
npm run watch-css
```

The official plugins that come out of the box with the boilerplate are the [forms](https://github.com/tailwindlabs/tailwindcss-typography), [typography](https://github.com/tailwindlabs/tailwindcss-typography) and [container-queries](https://github.com/tailwindlabs/tailwindcss-container-queries) plugins.

The geist fonts are set as default both for sans and mono families.

### Custom CSS (react or vanilla clients)

The `globals.css` file includes a content-grid class that allows you to establish a content hiearchy in a straightforward way, mobile friendly as well:

![content-grid](./images/content-grid.PNG)

You can determine where an element is placed within the horizonta hierarchy by giving it the utility class that corresponds to each hierarchy breakpoint:

- `full`
- `feature`
- `popout`
- `content`

The index.html template includes these classes for the `main-content` section, you can also combine them with tailwind's [responsive breakpoints](https://tailwindcss.com/docs/theme):

```html
<!-- Main content -->
<div
  id="main-content"
  class="full xl2:feature xl3:popout content-grid h-full xl2:rounded-md xl3:rounded-md"
></div>
```

Inspired by [this blogpost](https://ryanmulligan.dev/blog/layout-breakouts/).

### Customization

You can customize the generated templates by modifying the YAML files in the `templates/` directory of the HyperPyText project.

### License

This project is licensed under the MIT License.
