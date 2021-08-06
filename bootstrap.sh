#!/usr/bin/env bash

git clone https://github.com/nytimes/covid-19-data

python3 -m venv venv

. venv/bin/activate

pip install matplotlib
pip install pandas
pip install scipy

