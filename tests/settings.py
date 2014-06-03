SECRET_KEY = 'SEKRIT'

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'tests'
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'enumfields.db',
    },
}

