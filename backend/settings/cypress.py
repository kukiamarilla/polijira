from .dev import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test_polijira',
        'USER': 'polijira',
        'PASSWORD': 'polijira',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

CYPRESS_SETUP_TEST_DATA_MODULE="tests.e2e.db.setup_test_data"
