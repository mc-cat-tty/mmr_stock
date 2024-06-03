# MMR Stock Manager

Final project for web technologies course @ UniMoRe.

## Abstract
This webapp tries to address the challenges of in-house stock management for medium-sized teams such as @mmr-driverless.

In particular, the focus of the project is on electronic components, but most of the code would be valid for any kind of discrete item.

## Features
Noteworthy features are:
 - Protection mechanism: most valuable/scarse components can be protected. Users must require a DL approval before use.
 - Naive recommendation system: user-based collaborative filtering
 - Real-time dashboard for easy management
 - Front-end independent APIs
 - DB access synchronization (guaranteed by Django)
 - Location uniqueness guaranteed by SQL constraints

## Startup
Make sure `pipenv` is installed.

Locally install dependencies, then open virtual-environment shell, with:
```bash
pipenv install
pipenv shell
```

If `pipenv` complains about the an already activate venv, solve manually or force it with `--anyway` option.

Make sure there is no SQLite DB in root folder (where this README is located).

Create migrations (`python3 -m manage makemigrations`) if model has been changed.

Run the following to setup a mock environment with some user and some components:
```bash
bash db_setup.sh
```

Feel free to explore its internals to understand what's going on. The expected output is the creation of `dev_db.sqlite3` in root folder; the DB is filled in with stock data as mentioned above.

Now you are ready to start the development server:
```bash
python3 -m manage runserver 8080
```

## License
This software is distributed under MIT License.