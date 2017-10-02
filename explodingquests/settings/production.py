from .base import *
from django.contrib.messages import constants as messages

ALLOWED_HOSTS = ["https://explodingquests.herokuapp.com", "www.explodingquests.com"]

DEBUG = False

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

import dj_database_url
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)

# GOOGLE_MAP_API_KEY = ''

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

TIME_ZONE = "America/New_York"