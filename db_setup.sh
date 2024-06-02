#!/bin/bash

pipenv shell
python3 -m manage migrate
python3 -m manage mock_db_population
python3 -m manage mock_users
