from .dev import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test_django-vue-template',
        'USER': 'django-vue-template',
        'PASSWORD': 'django-vue-template',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

CYPRESS_SETUP_TEST_DATA_MODULE="tests.e2e.db.setup_test_data"
