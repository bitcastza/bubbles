###########################################################################
# Bubbles is Copyright (C) 2018 Kyle Robbertze <krobbertze@gmail.com>
#
# Bubbles is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# Bubbles is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Bubbles. If not, see <http://www.gnu.org/licenses/>.
###########################################################################
"""
Django settings for development bubbles project.
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'bubbles',
    'bubbles.inventory.apps.InventoryConfig',
    'bubbles.rentals.apps.RentalsConfig',
    'bubbles.registration',
    'bubbles.reporting',
    'bubbles.pages',
    'sakaiauthenticator',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'django_prometheus',
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

ROOT_URLCONF = 'bubbles.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bubbles.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases


if (os.environ.get('SQL_ENGINE', 'django_prometheus.db.backends.sqlite3').endswith('sqlite3')):
    DATABASES = {
        'default': {
            'ENGINE': os.environ.get('SQL_ENGINE', 'django_prometheus.db.backends.sqlite3'),
            'NAME': os.environ.get('SQL_DATABASE', os.path.join(BASE_DIR, 'db.sqlite3')),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': os.environ.get('SQL_ENGINE'),
            'NAME': os.environ.get('SQL_DATABASE'),
            'USER': os.environ.get('SQL_USER'),
            'PASSWORD': os.environ.get('SQL_PASSWORD'),
            'HOST': os.environ.get('SQL_HOST'),
            'PORT': os.environ.get('SQL_PORT'),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = [
    'sakaiauthenticator.sakaiauthenticator.SakaiAuthenticatorBackend',
    'django.contrib.auth.backends.ModelBackend',
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-za'

TIME_ZONE = 'Africa/Johannesburg'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SAKAI_URL = 'https://vula.uct.ac.za'
USE_SAKAI_SITE = True
SAKAI_SITE_ID = '9def63ae-af28-42c3-8f56-0055fbf8ad74'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_URL = '/static/'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MEDIA_ROOT = os.path.join(project_root, 'bubbles/media')

# Redirect to home URL after login
LOGIN_REDIRECT_URL = '/'
