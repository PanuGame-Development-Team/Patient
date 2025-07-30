#!/bin/bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
echo "SECRET_KEY='${uuidgen}'" > Patient/properties.py
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py makemigrations core
python3 manage.py makemigrations user
python3 manage.py makemigrations record
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py collectstatic
mkdir -p static_root/exports
mkdir -p static_root/uploads
sudo cp Patient.conf /etc/nginx/conf.d
sudo cp Patient.service /usr/lib/systemd/system
sudo perl -i -pe 's|\Q{{place}}\Q|'"$(pwd)"'|g' /etc/nginx/conf.d/Patient.conf
sudo perl -i -pe 's|\Q{{place}}\Q|'"$(pwd)"'|g' /usr/lib/systemd/system/Patient.service
sudo systemctl daemon-reload
sudo systemctl enable Patient
sudo systemctl start Patient
sudo nginx -s reload