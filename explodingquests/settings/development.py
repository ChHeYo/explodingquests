from .base import *

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

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

DATE_INPUT_FORMATS = ['%m/%d/%Y', ]

TIME_ZONE = 'America/New_York'