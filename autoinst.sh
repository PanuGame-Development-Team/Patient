#!/bin/bash
mkdir -p static/exports
mkdir -p static/uploads
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
touch Patient/properties.py
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py makemigrations core
python3 manage.py makemigrations user
python3 manage.py makemigrations records
python3 manage.py migrate
python3 manage.py createsuperuser