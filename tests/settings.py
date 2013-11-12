SECRET_KEY = 'SEKRIT'

INSTALLED_APPS = (
    'tests',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'enumfields.db',
    },
}
