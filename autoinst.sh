#!/bin/bash
mkdir -p static/exports
mkdir -p static/uploads
pip install -r requirements.txt
touch Patient/properties.py
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser