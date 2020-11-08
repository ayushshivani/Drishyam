#########################################
    ##  IMPORT LOCAL SETTINGS ##
#########################################
try:
    from .local_settings import *
except ImportError:
    pass




DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'predictiondb',
        'USER': 'postgres_user',
        'PASSWORD': 'postgres_password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}