"""
Django settings for unit tests the project 'project'.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

from project.settings import *

SECRET_KEY = 'key for unit tests, very secret as you can see, but we dont care'

# Are in test mode?
TESTING = 'test' or '-k e2e' in sys.argv

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allowed hosts
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
ALLOWED_HOSTS.extend(['127.0.0.1', 'localhost'])

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
# Of course DON'T use sqlite3 in Prod! use Postgres instead
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'tests.sqlite3'),
    }
}