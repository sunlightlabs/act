# Django settings for act project.
import os
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

ADMINS = (
    ('Jeremy Carbaugh', 'jcarbaugh@sunlightfoundation.com'),
)

MANAGERS = ADMINS
TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True

SITE_ID = 1

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = "http://assets.sunlightfoundation.com/admin/1.2.1/"

SECRET_KEY = '***REMOVED***'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'act.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'mediasync',
    'feedinator',
)

MEDIASYNC_AWS_KEY = '***REMOVED***'
MEDIASYNC_AWS_SECRET = '***REMOVED***'
MEDIASYNC_AWS_BUCKET = 'assets.sunlightfoundation.com'
MEDIASYNC_AWS_PREFIX = 'act/1.0'

try:
    from local_settings import *
except ImportError:
    pass