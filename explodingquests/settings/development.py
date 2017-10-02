from .base import *
from django.contrib.messages import constants as messages

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

# GOOGLE_MAP_API_KEY = ''

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

TIME_ZONE = "America/New_York"