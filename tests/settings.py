SECRET_KEY = 'SEKRIT'

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.auth',
    'django.contrib.admin',
    'tests',
)

ROOT_URLCONF = 'tests.urls'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'enumfields.db',
        'TEST_NAME': 'enumfields.db',
    },
}

DEBUG = True

STATIC_URL = "/static/"