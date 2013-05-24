"""Production settings and globals."""


from base import *
from memcacheify import memcacheify


INSTALLED_APPS += ('gunicorn',)

########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER', '')
EMAIL_PORT = environ.get('EMAIL_PORT', 587)
EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME
EMAIL_USE_TLS = True
SERVER_EMAIL = EMAIL_HOST_USER
########## END EMAIL CONFIGURATION


########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = memcacheify()
########## END CACHE CONFIGURATION


########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = get_env_setting('DJANGO_SECRET_KEY')
########## END SECRET CONFIGURATION
