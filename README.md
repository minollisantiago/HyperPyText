# HyperPyText

#### Build python and vanilla javascript apps :fire: :rocket: :fire:

<br>
<br>

![hyperpytext](./images/hyperpytext.png)

<br>
<br>

HyperPyText is a Python-based tool for creating FastAPI application boilerplates with Tailwind CSS integration. It streamlines the process of setting up a new project by automating the creation of directory structures, configuration files, and initial code templates.

The idea is to set up a dashboard/app project as fast as possible and get working quickly. This boilerplate is a simpler version of [FastHTML](https://fastht.ml/). I just prefer to write the html/css myself.

Its important to note that fastHTML is more robust and complete, this is just a simplified version (no auth, database, ease of deployment tools), so its minimal as of now.

literally built it in a couple of hours with Claude 3.5 Sonnet from [Anthropic](https://www.anthropic.com/).

Ill add more documentation as it improves, this is the first iteration, built in a couple of hours.

Built on top of:

- [FastApi](https://fastapi.tiangolo.com/)
- [Jinja Templates](https://jinja.palletsprojects.com/en/3.1.x/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [SQLite](https://www.sqlite.org/index.html)
- [HTMX](https://htmx.org/)
- [Tailwindcss](https://tailwindcss.com/)

## Features

- FastAPI application setup
- Tailwind CSS integration (npm or standalone)
- Jinja2 templating
- Customizable HTML templates
- Asset management structure
- Environment variable configuration
- Git integration with .gitignore
- SQLite database integration with piccolo (prefered/default) or sqlalchemy
- Optional Electron setup for desktop applications
- Poetry for python dependency management

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/hyperpytext.git
```

2. Navigate to the package folder:

```bash
cd hyperpytext
```

3. Install the package using pip:

```bash
pip install .
```

## Usage

After installing the package, run the `create-hyperpy-app {app name}` command to create a new application on the current working directory:

```bash
create-hyperpy-app your_app_name
```

You'll be prompted to enter:

- The HTML file name _(defaults to index.html)_.
- If you want Tailwind css and all its setup options: (npm or standalone installation and [plugins](https://tailwindcss.com/docs/plugins)).
- If you want to install [Vercel's Geist font](https://vercel.com/font) _(sans and mono versions, using npm)_.

## Project Structure

The generated project will have the following structure:

```
your_app_name/
├── src/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   └── root.py
│   │   │   └── __init__.py
│   │   ├── db/
│   │   │   ├── schemas/
│   │   │   │   ├── __init__.py
│   │   │   │   └── user.py
│   │   │   ├── __init__.py
│   │   │   └── db_manager.py
│   │   ├── templates/
│   │   │   └── {filename}.html
│   │   └── app.py
│   └── assets/
│       ├── css/
│       │   └── globals.css
│       ├── js/
│       │   ├── theme-control.js
│       │   └── scripts.js
│       └── icons/
│           └── favicon.ico
├── .env
├── .gitignore
├── main.js
├── package.json
├── pyproject.toml
├── README.md
└── tailwind.config.js
```
### SQLite with Piccolo ORM

#### Default Database Structure

HyperPyText uses [Piccolo ORM](https://piccolo-orm.com/) for database management with SQLite. 

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

If you choose to add the example piccolo app when prompted while creating the project, it will include a `tables.py` file with a pre-defined Users table example. You can find it at `src/app/db/primary/tables.py`. 

The file will include a Users_ piccolo table, with the following model: 

```python
from piccolo.table import Table
from piccolo.columns import Varchar, Timestamp

class Users_(Table, tablename="users_"):
    name = Varchar(length=100, unique=True, index=True)
    email = Varchar(length=100, unique=True, index=True)
    hashed_password = Varchar(length=100, null=True)
    created_at = Timestamp(auto_now=True)
    updated_at = Timestamp(auto_now_add=True)
```

#### Creating and running migrations

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
In order to run the migrations you will need to write the files yourself, as auto migrations are not supported for SQLite, see the Piccolo [migration docs](https://piccolo-orm.readthedocs.io/en/latest/piccolo/migrations/index.html) for more information.

One you successfully run the initial migration you can run the following command from the terminal *(need to have the python environment activated with all the dependencies installed)*:

```bash
cd src/app/db/primary
python db_populate.py
```
This will populate the database with some random data so you can begin querying the database using the Piccolo CLI and its ipython shell. To activate the ipython shell run:

```bash
cd src/app/db/primary
piccolo shell run
```
Then you can query the database using the piccolo syntax, for example for a `SELECT * FROM users_` query the syntax would be:

```bash
await Users_.select()
```
For more Query types, go [here](https://piccolo-orm.readthedocs.io/en/latest/piccolo/query_types/index.html).

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
from src.app.db.primary.tables import Users_

@app.get("/users")
async def get_users():
      return await Users_.select().run()
```
#### Piccolo Auth

**Structure**

If you choose to go with Picoolo authentication, the project will have a folder inside the db folder with the following structure:

```
src/app/db/
├── auth/
│   ├── __init__.py
│   ├── piccolo_conf.py
│   └── ...
```

**Session Auth**
Piccolo has a side project called piccolo-api that provides with some useful tools for ASGI applications, including built in authentication, admin interface, etc.

Piccolo [recommends using session auth](https://piccolo-api.readthedocs.io/en/latest/which_authentication/index.html) for most apps, so we are going with that.

For a complete guide on how to set up session auth with piccolo api, read their [docs](https://piccolo-api.readthedocs.io/en/latest/session_auth/index.html).

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

**Endpoints**




### Tailwind CSS Integration

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

### Custom CSS

The `input.css` file includes a content-grid class that allows you to establish a content hiearchy in a straightforward way, mobile friendly as well:

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

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### License

This project is licensed under the MIT License.
