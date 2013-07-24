"""
Django settings for TextbookArb project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
SETTINGS_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_DIR =  os.path.join(SETTINGS_DIR, '..')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8$%qe_p_sspl$iighwl2+xlnl3q*d8!&(qhm#j*ac9a%cufwx8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ta',
    #'south',
    'gunicorn',
    'djcelery',
    'djkombu',
    'south',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'TextbookArb.urls'

WSGI_APPLICATION = 'TextbookArb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'ta',                      # Or path to database file if using sqlite3.
        'USER': 'brandon',                      # Not used with sqlite3.
        'PASSWORD': 'secret',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'

# django-celery

import djcelery
djcelery.setup_loader()

BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"
BROKER_VHOST = "/"

CELERYD_CONCURRENCY = 15
CELERY_RESULT_BACKEND = "amqp"
CELERY_AMQP_TASK_RESULT_EXPIRES = 30  # 5 hours.
CELERYD_MAX_TASKS_PER_CHILD = 3
CELERYD_TASK_TIME_LIMIT = 900

from datetime import timedelta
from celery.schedules import crontab

#CELERY_QUEUES = {
#    "default": {
#        "exchange": "default",
#        "binding_key": "default"},
#    "quickqueue": {
#        "exchange": "quickq",
#        "exchange_type": "topic",
#        "binding_key": "quickq.quick",
#    },
#}
#
#CELERY_ROUTES = (
#    {
#        "ta.tasks.updateBCs": {
#            "queue": "quickqueue"
#        },
#    },
#)

#CELERY_DEFAULT_QUEUE = "default"
#CELERY_DEFAULT_EXCHANGE = "default"
#CELERY_DEFAULT_EXCHANGE_TYPE = "direct"
#CELERY_DEFAULT_ROUTING_KEY = "default"

CELERYBEAT_SCHEDULE = {
    #    "runs-every-600-seconds": {
    #        "task": "ta.tasks.updateBCs",
    #        "schedule": timedelta(seconds=180),
    #    },
    # Executes every morning at 4am
    #    "every-morning": {
    #        "task": "ta.tasks.findNewBooks",
    #        "schedule": crontab(hour="*/12"),
    #    },
    # Executes every morning at 4am
    "every-evening": {
        "task": "ta.amazon.detailAllBooks",
        "schedule": crontab(hour=19, minute=00,),
        },
    "every-morning3": {
        "task": "ta.amazon.detailAllBooks",
        "schedule": crontab(hour=7, minute=00,),
        },
    #    "every-morning2": {
    #        "task": "ta.tasks.lookForNewBooks",
    #        "schedule": crontab(hour=0, minute=0,),
    #    },
}

#end django-celery
