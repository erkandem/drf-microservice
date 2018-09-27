"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/

List of settings that the project as to have to be ready for production:

- General settings:
    - SECRET_KEY: the Django secret key
    - ENABLE_DEBUG: False by default, set to 1 to enable it.
    - ALLOWED_HOSTS: empty by default, use comma-separated list.
    - LOGGING_CONFIG: default None. TODO
    - TIME_ZONE: default 'UTC', list: http://pytz.sourceforge.net/#what-is-utc
    - PATH_TO_STORE_FILE: default BASE_DIR + '/files/'
- DB-related settings:
    - DB_HOST: default 'localhost'
    - DB_USER: default 'user'
    - DB_NAME: default 'project_db'
    - DB_PASS: default 'passwd' in debug mode ssm 'db_password' in production.
    - DB_PORT: default '5432'
- Email settings:
    - TODO
- Sentry settings:
    - SENTRY_DSN: default is None, set to a valid DSN to enable sentry.
    - SENTRY_RELEASE: default 'local', set to 'stage', 'live', etc.
- AWS settings:
    - TODO
- Silk profiler:
    - ENABLE_SILK: False by default, set to 1 to enable it.

"""

import os
import sys

# import boto3 as boto3
#
# # for the secrets
# aws_client = boto3.client('ssm', region_name='eu-west-1')
# response = aws_client.get_parameters(
#     Names=[
#         'db_password',
#         'email_password',
#         'django_secret_key',
#         'stats_api_key',
#     ],
#     WithDecryption=True
# )
# secrets = {p.get('Name'): p.get('Value') for p in response.get('Parameters')}
secrets = {}

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PATH_TO_STORE_FILE = os.environ.get(
    'PATH_TO_STORE_FILE', default=BASE_DIR + '/files/')
os.makedirs(PATH_TO_STORE_FILE, exist_ok=True)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# Are in test mode?
TESTING = 'test' or '-k e2e' in sys.argv

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.getenv('ENABLE_DEBUG', 0)))

# Allowed hosts
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
if DEBUG:
    ALLOWED_HOSTS.extend(['127.0.0.1', 'localhost'])


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    )
}

# Application definition
INSTALLED_APPS = [
    # Core authentication framework and its default models.
    'django.contrib.admin',
    # Django content type system (allows perms to be associated with models).
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',

    'project',
    'rest',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Manages sessions across requests
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # Associates users with requests using sessions.
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

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

WSGI_APPLICATION = 'project.wsgi.application'


if TESTING:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'tests.sqlite3'),
        }
    }
else:
    if DEBUG:
        DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
        DB_USER = os.getenv('DB_USER', 'user')
        DB_PASS = os.getenv('DB_PASS', 'passwd')
        DB_NAME = os.getenv('DB_NAME', 'project_db')
        DB_PORT = os.getenv('DB_PORT', '5432')
        # todo: change to postgres later, and refactor this part
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            },
        }
    else:
        DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
        DB_USER = os.getenv('DB_USER', 'user')
        DB_PASS = secrets.get('db_password', 'passwd')
        DB_NAME = os.getenv('DB_NAME', 'project_db')
        DB_PORT = os.getenv('DB_PORT', '5432')
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'HOST': DB_HOST,
                'PORT': DB_PORT,
                'NAME': DB_NAME,
                'USER': DB_USER,
                'PASSWORD': DB_PASS,
            }
        }

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {   # todo; here for the fanatic pep8 line len max 79, tell me how to solve it???
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


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = 'en-us'

# list: http://pytz.sourceforge.net/#what-is-utc
TIME_ZONE = os.environ.get('TIME_ZONE', default='UTC')
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'

# # Sentry
# SENTRY_DSN = os.getenv('SENTRY_DSN', None)
# if SENTRY_DSN is not None:
#     import raven
#     SENTRY_RELEASE = os.getenv('SENTRY_RELEASE', 'local')
#
#     INSTALLED_APPS.append('raven.contrib.django.raven_compat')
#     RAVEN_CONFIG = {
#         'dsn': SENTRY_DSN,
#         'release': SENTRY_RELEASE,
#     }