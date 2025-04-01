I want to improve this package ive created. 

This is a tool that creates boilerplate web applications with a python fast api server, and a react with vite client using some dependencies for components like shadcn. Take a look at the @README.md for more details.

Im looking to make several improvements, we will be working on them sequentially, i want  mark them as done as we finish with each one:

#### Main and most important improvements
1. [ ] Make uv the sole package manager, and remove poetry support.
2. [ ] Make react with vite the sole frontend framework, and remove vanilla js with htmx support.
3. [ ] Move from click to typer/rich for the CLI. I want rich text output for the CLI.
4. [ ] Simplify the @__init__.py file, and move as much logic outside of it and into separate files if possible (server and client setup, for example, also util functions).
5. [ ] All template files for the client on the react folder (src/hyperpytext/templates/react/client) include their file extensions. I want to do the same for the server files (py files).

#### Longer term improvements
1. [ ] Add support for postgres (within the context of piccolo orm).
2. [ ] Make functions more granular, add type hinting and input models using pydantic, the goal is to have a toolset of functions for agentic use later when we create single file agents that handle the creation of the boilerplate project.
3. [ ] Add support for CLI tools using uv, without frontend.
4. [ ] Add support for docker.
5. [ ] Add tooling to automate the creation of PRD files based on the project instance created by the tool, example: if the user creates a CLI without frontend, have a function that can be used to create a PRD template file for a CLI project, etc. We are going to use this project as an inspiration: [claude-task-master](https://github.com/eyaltoledano/claude-task-master).
6. [ ] Add a custom agent that can be used to setup the project based on a PRD (project requirements document).

#### Nice to have
1. [ ] Add support for LLM to write the frontend code, and the backend code.
2. [ ] Add support for LLM to write the tests.
3. [ ] Add support for LLM to write the docker file.
4. [ ] Add support for LLM to write the PRD file.

#### App structure

├── images
│   ├── content-grid.PNG
│   └── hyperpytext.png
├── pyproject.toml
├── README.md
├── rules.md
├── src
│   └── hyperpytext
│       ├── __init__.py
│       ├── templates
│       │   ├── react
│       │   │   ├── client
│       │   │   │   ├── app.tsx.yaml
│       │   │   │   ├── carousel.tsx.yaml
│       │   │   │   ├── fastapi.svg.yaml
│       │   │   │   ├── favicon.svg.yaml
│       │   │   │   ├── fonts.css.yaml
│       │   │   │   ├── globals.css.yaml
│       │   │   │   ├── headline.tsx.yaml
│       │   │   │   ├── hero.tsx.yaml
│       │   │   │   ├── hyperpylogo.tsx.yaml
│       │   │   │   ├── index.html.yaml
│       │   │   │   ├── links.tsx.yaml
│       │   │   │   ├── main.tsx.yaml
│       │   │   │   ├── mask.svg.yaml
│       │   │   │   ├── mask.tsx.yaml
│       │   │   │   ├── python.svg.yaml
│       │   │   │   ├── react.svg.yaml
│       │   │   │   ├── serverstatus.tsx.yaml
│       │   │   │   ├── shadcn.svg.yaml
│       │   │   │   ├── tailwind.config.js.yaml
│       │   │   │   └── tailwindcss.svg.yaml
│       │   │   └── server
│       │   │       ├── api.yaml
│       │   │       ├── app.yaml
│       │   │       ├── db_auth.yaml
│       │   │       ├── db_cache.yaml
│       │   │       ├── db_primary.yaml
│       │   │       ├── db_primary_example.yaml
│       │   │       ├── db_queues.yaml
│       │   │       ├── env.yaml
│       │   │       ├── envrc.yaml
│       │   │       ├── gitignore.yaml
│       │   │       ├── init.yaml
│       │   │       ├── pyproject.yaml
│       │   │       ├── readme.yaml
│       │   │       ├── routes_auth.yaml
│       │   │       ├── routes_models.yaml
│       │   │       ├── utils.yaml
│       │   │       └── uvicorn.yaml
│       │   └── vanilla
│       │       ├── api.yaml
│       │       ├── app.yaml
│       │       ├── db_auth.yaml
│       │       ├── db_cache.yaml
│       │       ├── db_primary.yaml
│       │       ├── db_primary_example.yaml
│       │       ├── db_queues.yaml
│       │       ├── electron.yaml
│       │       ├── env.yaml
│       │       ├── envrc.yaml
│       │       ├── gitignore.yaml
│       │       ├── index.yaml
│       │       ├── init.yaml
│       │       ├── input_css.yaml
│       │       ├── pyproject.yaml
│       │       ├── readme.yaml
│       │       ├── routes_auth.yaml
│       │       ├── routes_models.yaml
│       │       ├── tailwind_config.yaml
│       │       ├── utils.yaml
│       │       └── uvicorn.yaml
│       └── utils
│           ├── __init__.py
│           ├── npm_electron_utils.py
│           ├── npm_shadcnui_utils.py
│           ├── npm_tailwind_utils.py
│           ├── npm_utils.py
│           ├── npm_vite_utils.py
│           ├── poetry_utils.py
│           └── uv_utils.py
└── uv.lock

- All utility functions are on the utils/ folder.
- All template files are yaml files, and they are split by type of file (frontend, backend, etc).
- All yaml files on the client folder for react include their file extension for reference.