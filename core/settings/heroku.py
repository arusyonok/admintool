from .base import *
import dj_database_url

DEBUG = True

STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"


ALLOWED_HOSTS = ["homeadmin.herokuapp.com"]


DATABASES = {
    'default': dj_database_url.config(conn_max_age=600)
}
