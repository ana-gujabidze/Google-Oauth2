from dotenv import dotenv_values

from .base import *

# Connet to env file
config = dotenv_values('.env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Append application definition
INSTALLED_APPS.insert(INSTALLED_APPS.index('rest_framework'), 'drf_yasg')

# Connection configuration to Google OAuth client
GOOGLE_OAUTH2_CLIENT_ID = config['GOOGLE_OAUTH2_CLIENT_ID']
GOOGLE_OAUTH2_CLIENT_SECRET = config['GOOGLE_OAUTH2_CLIENT_SECRET']

# JWT configuration
SIMPLE_JWT['SIGNING_KEY'] = SECRET_KEY

CORS_ALLOW_ALL_ORIGINS = True
