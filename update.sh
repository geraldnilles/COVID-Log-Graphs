#!/usr/bin/env bash


cd covid-19-data

git pull

cd ..

. venv/bin/activate

./plot.py

git add -A
git commit -m "Automatic Update of Graphs"


