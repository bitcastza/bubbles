# Bubbles
Bubbles is a SCUBA equipment management system for dive clubs. It manages
equipment details and rentals by members.

# Features
- Rentals - members can rent out gear for a period of time
- Service tracking - staff can easily see equipment that needs servicing
- Equipment life-cycle - track equipment from purchase to condemnation
- User management

# Installation
Bubbles is built using Django and Python 3.

## Development
A development environment can be set up using:

```
$ virtualenv -p python3 pyenv
$ pyenv/bin/pip install -r requirements.txt
$ pyenv/bin/python manage.py createsuperuser
$ pyenv/bin/python manage.py migrate
$ pyenv/bin/python manage.py runserver
```
This will start a development web server on http://127.0.0.1:8000/

## Production
A more production ready setup can be created by following the
[Ansible role](https://gitlab.com/bubbles/ansible).

# Contribute
- Issue Tracker: https://gitlab.com/bubbles/bubbles/issues
- Source Code: https://gitlab.com/bubbles/bubbles

# Licence
This project is licensed under the GNU Public License version 3.

