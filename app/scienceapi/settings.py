"""
Django settings for scienceapi project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import environ

app = environ.Path(__file__) - 1
root = app - 1
env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
    USE_S3=(bool, True),
    CORS_WHITELIST=(tuple, ()),
    CORS_REGEX_WHITELIST=(tuple, ()),
    GH_TOKEN=(str, None),
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = root()

APP_DIR = app()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env('ALLOWED_HOSTS')

GH_TOKEN = env('GH_TOKEN')

# Application definition

INSTALLED_APPS = list(filter(None, [
    'filebrowser_s3' if env('USE_S3') else None,

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    "django.contrib.redirects",
    'django.contrib.sessions',
    "django.contrib.sites",
    "django.contrib.sitemaps",
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'whitenoise.runserver_nostatic',
    'django_extensions',
    'rest_framework',
    'rest_framework_docs',
    'storages',
    'gunicorn',
    'corsheaders',

    'scienceapi.users',
    'scienceapi.projects',
    'scienceapi.events',
    'scienceapi.study_groups',
    'scienceapi.resources',
    "scienceapi.scienceblog",

    "mezzanine.boot",
    "mezzanine.conf",
    "mezzanine.core",
    "mezzanine.generic",
    "mezzanine.pages",
    "mezzanine.blog",
    "mezzanine.forms",
    "mezzanine.galleries",
    "mezzanine.twitter",

]))

MIDDLEWARE_CLASSES = [
    "mezzanine.core.middleware.UpdateCacheMiddleware",

    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    "mezzanine.core.request.CurrentRequestMiddleware",
    "mezzanine.core.middleware.RedirectFallbackMiddleware",
    "mezzanine.core.middleware.TemplateForDeviceMiddleware",
    "mezzanine.core.middleware.TemplateForHostMiddleware",
    "mezzanine.core.middleware.AdminLoginInterfaceSelectorMiddleware",
    "mezzanine.core.middleware.SitePermissionMiddleware",
    "mezzanine.pages.middleware.PageMiddleware",
    "mezzanine.core.middleware.FetchFromCacheMiddleware",
]

PACKAGE_NAME_FILEBROWSER = "filebrowser_safe"
PACKAGE_NAME_GRAPPELLI = "grappelli_safe"

#########################
# OPTIONAL APPLICATIONS #
#########################

# These will be added to ``INSTALLED_APPS``, only if available.
OPTIONAL_APPS = (
    PACKAGE_NAME_FILEBROWSER,
    PACKAGE_NAME_GRAPPELLI
)

ROOT_URLCONF = 'scienceapi.urls'

ADMIN_REMOVAL = [
    'mezzanine.pages.models.Page',
    'mezzanine.generic.models.ThreadedComment',
]

BLOG_USE_FEATURED_IMAGE = True

# We hit https://github.com/stephenmcd/mezzanine/issues/1748
# in Mezzanine 4.2.3 while importing blogs from wordpress,
# so removing thumbnails filter.
# To Do: Remove this after mezzanine update.
RICHTEXT_FILTERS = ()

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [root('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.static",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.template.context_processors.tz",
                "mezzanine.conf.context_processors.settings",
                "mezzanine.pages.context_processors.page",
            ],
            "builtins": [
                "mezzanine.template.loader_tags",
            ],

        },
    },
]

WSGI_APPLICATION = 'scienceapi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': env.db("DATABASE_URL"),
}

DATABASES['default']['ATOMIC_REQUESTS'] = True


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.NumericPasswordValidator',
    },
]


# Location of root django.contrib.admin URL, use {% url 'admin:index' %}
ADMIN_URL = r'^admin/'


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    app('static'),
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_ROOT = root('staticfiles')

# Storage for user generated files
USE_S3 = env('USE_S3')

if USE_S3:
    # Use S3 to store user files if the corresponding environment var is set
    DEFAULT_FILE_STORAGE = 'filebrowser_s3.storage.S3MediaStorage'

    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = env('AWS_S3_CUSTOM_DOMAIN')
    AWS_LOCATION = env('AWS_LOCATION')

    MEDIA_URL = 'https://' + AWS_S3_CUSTOM_DOMAIN + '/'
    MEDIA_ROOT = ''

    FILEBROWSER_DIRECTORY = env('FILEBROWSER_DIRECTORY')

else:
    # Otherwise use the default filesystem storage
    MEDIA_ROOT = root('media/')
    MEDIA_URL = '/media/'

# Rest Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination'
                                '.PageNumberPagination',
    'ORDERING_PARAM': 'sort',
    'PAGE_SIZE': 9,
}

SITE_ID = 1


# CORS
CORS_ALLOW_CREDENTIALS = False


if '*' in env('CORS_WHITELIST'):
    CORS_ORIGIN_ALLOW_ALL = True
else:
    CORS_ORIGIN_WHITELIST = env('CORS_WHITELIST')
    CORS_ORIGIN_REGEX_WHITELIST = env('CORS_REGEX_WHITELIST')


####################
# DYNAMIC SETTINGS #
####################

# set_dynamic_settings() will rewrite globals based on what has been
# defined so far, in order to provide some better defaults where
# applicable. We also allow this settings module to be imported
# without Mezzanine installed, as the case may be when using the
# fabfile, where setting the dynamic settings below isn't strictly
# required.
try:
    from mezzanine.utils.conf import set_dynamic_settings
except ImportError:
    pass
else:
    set_dynamic_settings(globals())
