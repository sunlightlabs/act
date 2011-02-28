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
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'act.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.markup',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'debug_toolbar',
    'cloudmailin',
    'mediasync',
    'feedinator',
    'tagging',
    'honeypot',
    'blogdor',
    'haystack',
    'act.events',
    'act.resources',
    'act.tweets',
    'act.blogimport',
    'gunicorn',
)

EMAIL_BACKEND = 'postmark.django_backend.EmailBackend'

MEDIASYNC = {
    'BACKEND': 'mediasync.backends.s3',
    'AWS_KEY': "***REMOVED***",
    'AWS_SECRET': "***REMOVED***",
    'AWS_BUCKET': "assets.sunlightfoundation.com",
    'AWS_PREFIX': "act/2.0",
    'DOCTYPE': 'xhtml',
    'CACHE_BUSTER': 1234567890,
    'JOINED': {
        'scripts/production.js': (
            'scripts/jquery-1.5.min.js',
            'scripts/jquery.placehold-0.2.min.js',
            'scripts/act.js',
        ),
    }
}

INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

# blogdor configuration
BLOGDOR_POSTS_PER_PAGE = 10
BLOGDOR_AUTHOR_GROUP = None
BLOGDOR_FROM_EMAIL = 'bounce@%s'
BLOGDOR_DEFAULT_MARKUP = 'markdown'
#AKISMET_KEY = ''
#GRAVATAR_DEFAULT = ''
#GRAVATAR_SIZE = 96

HONEYPOT_FIELD_NAME = 'zipcode'

HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_SITECONF = 'act.search_sites'

try:
    from local_settings import *
except ImportError:
    pass