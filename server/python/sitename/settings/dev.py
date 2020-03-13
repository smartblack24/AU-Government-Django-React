from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'admin',
        'USER': 'admin',
        'PASSWORD': 'admin',
        'HOST': 'db',
        'PORT': '5432',
    },
    'emails': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'admin',
        'USER': 'admin',
        'PASSWORD': 'admin',
        'HOST': 'db',
        'PORT': '5432',
    }
}

SITE_URL = os.environ.get('SITE_URL')
API_URL = os.environ.get('API_URL')

INSTALLED_APPS.append('django_extensions')
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = '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'
EMAIL_USE_TLS = True


CORS_ORIGIN_WHITELIST = (
    'localhost:8000',
    'localhost:3000',
)

X_FRAME_OPTIONS = 'ALLOWALL'
