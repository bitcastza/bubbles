#!/usr/bin/env bash

echo "Waiting for postgres..."
while ! nc -z $SQL_HOST $SQL_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createdefaultuser

python3 manage.py runserver 0.0.0.0:8000
