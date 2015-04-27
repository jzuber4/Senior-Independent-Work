"""
Django settings for IW project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '74j2znpj2(#an@8ay242qxo*op2pncq=mguph9a=e0&_*x2x%)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # extra dependencies
    'bootstrap3',
    'compressor',
    # my app(s)
    'quizzes',
    'quiz_service',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # CAS
    'cas.middleware.CASMiddleware',
)

ROOT_URLCONF = 'IW.urls'

WSGI_APPLICATION = 'IW.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True
USE_TZ = True

# CAS
CAS_SERVER_URL = "https://fed.princeton.edu/cas/"
# Auth / CAS
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'cas.backends.CASBackend',
)
CAS_RESPONSE_CALLBACKS = (
    'IW.cas.callback',
)

# soap url for quiz service
QUIZ_SERVICE_URL = 'http://10.8.241.134:8080/Initial/services/Main?wsdl'
QUIZ_SERVICE_DEBUG = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

# search each app directory for static files
STATIC_ROOT = ''
# static files stored under /static/ for each app
STATIC_URL = '/static/'
# general static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)
# add precompilers for coffeescript, etc.
COMPRESS_PRECOMPILERS = (
    ('text/coffeescript', 'coffee --compile --stdio'),
)

# Directories containing templates
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

# Deployment
if False:
    with open('secret_key.txt') as f:
        SECRET_KEY = f.read().strip()
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    QUIZ_SERVICE_DEBUG = False
    DEBUG = False
    ALLOWED_HOSTS = [
        '.princeton.edu'  # Allow princeton domain and subdomains
    ]

