#!/usr/bin/env bash

python3 manage.py collectstatic --noinput
python3 manage.py migrate --noinput

if [[ -n $USER_USERNAME ]]; then
    echo "Creating user..."
    python3 manage.py createdefaultuser --username $USER_USERNAME --email $USER_EMAIL --password $USER_PASSWORD
fi

uwsgi /etc/uwsgi/bubbles.ini
