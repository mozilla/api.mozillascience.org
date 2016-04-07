from .common import *

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
DATABASES['default'] = env.db("DATABASE_URL")
