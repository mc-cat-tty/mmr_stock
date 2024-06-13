# MMR Stock Manager

Final project for web technologies course @ UniMoRe.

## Abstract
This webapp tries to address the challenges of in-house stock management for medium-sized teams such as @mmr-driverless.

In particular, the focus of the project is on electronic components, but most of the code would be valid for any kind of discrete item.

## Features
Noteworthy features are:
 - Protection mechanism: most valuable/scarce components can be protected. Users must require a DL approval before use.
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

If `pipenv` complains about an already active venv, solve manually or force it with `--anyway` option.

Make sure there is no SQLite DB in root folder (where this README is located).

Create migrations (`python3 -m manage makemigrations`) if model has been changed.

Run the following to setup a mock environment with some users and some components:
```bash
bash db_setup.sh
```

Feel free to explore its internals to understand what's going on. The expected output is the creation of `dev_db.sqlite3` in root folder; the DB is filled in with stock data as mentioned above.

Now you are ready to start the development server:
```bash
python3 -m manage runserver 8080
```

Login as _admin_ with password _123_ and start to explore.

## Recommendation System
The recommendation is a user-based collaborative filtering.
Each user is characterized by a (presumably sparse) vector of stars.

For each user U, its k-neighbors (K parametrized in `analytics.recommendation`) are extracted from the high dimensional space. This is the set of users that has an influence on the prediction for U.

The assumption under which this recommender works, is that if users similar to U liked an item i, also U will like it.

Given this assumption, the prediction is easy: stars for each element are averaged. Items that survive a certain filter (thresholding + slicing N-top) will be proposted to the user in the _You may want to start from_ section.

More subtle strategies can be used, like weighting each star with the correlation between U and the user that gave the star; but for small instances, the current method showed to perform well.

## Testing
Some illustrative test-cases have been written in `core` (logic-only tests) and `analytics` (api-oriented tests) applications.

## License
This software is distributed under MIT License.
