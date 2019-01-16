# Bubbles

Bubbles is an equipment management system for the UCT Underwater Club.

# Building

## Django

Bubbles is built using Django. A development environment can be set up using:

```
$ virtualenv -p python3 pyenv
$ pyenv/bin/pip install -r requirements.txt
$ pyenv/bin/python manage.py migrate
$ pyenv/bin/python manage.py runserver
```
This will start a development web server on http://127.0.0.1:8000/

A more production ready setup can be created by following the
[ansible role](https://gitlab.com/bubbles/ansible).

## Analysis

The analysis documentation can be built using

````
$ cd analysis
$ make
````

This requires `pdflatex` and `plantuml` to build.
