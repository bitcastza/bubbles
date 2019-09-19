#!/bin/bash

echo Starting Nginx
nginx
echo Starting uWSGI
mkdir /var/run/uwsgi/
chown www-data:www-data /var/run/uwsgi
uwsgi --uid www-data --gid www-data /etc/uwsgi/bubbles.ini
