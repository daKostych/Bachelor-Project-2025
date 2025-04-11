#!/bin/bash

poetry install --no-root

cd src
PYTHONPATH=$(pwd)/.. poetry run python main.py
cd ..