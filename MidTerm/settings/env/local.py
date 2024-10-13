from settings.base import *
from decouple import config


DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config("POSTGRES_DB", cast=str),
        'USER': config("POSTGRES_USER", cast=str),
        'PASSWORD': config("POSTGRES_PASSWORD", cast=str),
        'HOST': 'db',
        'PORT': '5432',
    }
}

INTERNAL_IPS = [
    "127.0.0.1",
]
ALLOWED_HOSTS = ['*']

# ASGI | WSGI configuration
ASGI_APPLICATION = "deploy.asgi.application"
WSGI_APPLICATION = 'deploy.wsgi.application'
