import os

from settings.base import *
from settings.base import BASE_DIR



DEBUG = True
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'postgres',
#         'USER': 'postgres',
#         'PASSWORD': 'password',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
INTERNAL_IPS = [
    "127.0.0.1",
]
ALLOWED_HOSTS = ['*']

# ASGI | WSGI configuration
ASGI_APPLICATION = "deploy.asgi.application"
WSGI_APPLICATION = 'deploy.wsgi.application'
