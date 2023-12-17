#! /bin/sh
sleep 3
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn -c gunicorn_conf.py wallet.wsgi
