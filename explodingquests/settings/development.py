from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'explodingquests_db',
        'USER': 'jay',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '', 
    }
}