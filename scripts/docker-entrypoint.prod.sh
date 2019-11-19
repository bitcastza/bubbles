#!/usr/bin/env bash

rm -fr staticfiles

python3 manage.py collectstatic --noinput
python3 manage.py migrate --noinput

uwsgi /etc/uwsgi/bubbles.ini
