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

MEDIA_ROOT = ''
MEDIA_URL = ''

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static_root')
STATIC_URL = '/static/'

STATICFILES_STORAGE = 'mediasync.CachedMediaSyncStorage'

ADMIN_MEDIA_PREFIX = "http://assets.sunlightfoundation.com/admin/1.3/"

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
    'mediasync.MediaSyncMiddleware',
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
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'debug_toolbar',
    'cloudmailin',
    'feedinator',
    'tagging',
    'honeypot',
    'blogdor',
    'haystack',
    'act.events',
    'act.resources',
    'act.tweets',
    'act.blogimport',
    'act',
    'gunicorn',
)

EMAIL_BACKEND = 'postmark.django_backend.EmailBackend'

AWS_ACCESS_KEY_ID = "***REMOVED***"
AWS_SECRET_ACCESS_KEY = "***REMOVED***"
AWS_STORAGE_BUCKET_NAME = "assets.sunlightfoundation.com"
AWS_LOCATION = "act/2.1"
AWS_IS_GZIPPED = True

# MEDIASYNC = {
#     'BACKEND': 'mediasync.backends.s3',
#     'AWS_KEY': AWS_ACCESS_KEY_ID,
#     'AWS_SECRET': AWS_SECRET_ACCESS_KEY,
#     'AWS_BUCKET': AWS_STORAGE_BUCKET_NAME,
#     'AWS_PREFIX': AWS_LOCATION,
#     'DOCTYPE': 'xhtml',
#     'CACHE_BUSTER': 201103021519,
#     'JOINED': {
#         'scripts/production.js': (
#             'scripts/jquery-1.5.min.js',
#             'scripts/jquery.placehold-0.2.min.js',
#             'scripts/act.js',
#         ),
#     }
# }

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
