"""
Django settings for django_project project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import logging
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import pathlib
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

SECRET_KEY = 'delab'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = (os.environ.get('DEBUG_VALUE') == 'True')
# DEBUG = 'true'

ALLOWED_HOSTS = ['127.0.0.1', '0.0.0.0', 'localhost']

# Application definition

INSTALLED_APPS = [
    'treenode',
    'rest_framework',
    'django_filters',
    'delab.apps.DelabConfig',
    'blog.apps.BlogConfig',
    'users.apps.UsersConfig',
    'background_task',
    'django_countries',
    'crispy_forms',
    'django_extensions',
    'reset_migrations',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'django_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'database/sqlite/db.sqlite3'),
    },

    'postgres': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'postgres',
        'PORT': 5432,
    },
    'postgres_local': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}
"""
'mysql': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'delab',
        'USER': 'delab',
        'PASSWORD': 'delab',
        'HOST': 'localhost',
        'PORT': '',
    }
"""

default_database = os.getenv('DJANGO_DATABASE', 'postgres_local')
# default_database= "postgres_local"
DATABASES['default'] = DATABASES[default_database]
print("using database: {}".format(DATABASES["default"]))

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 'DEFAULT_PERMISSION_CLASSES': [
#    'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
#    'rest_framework.permissions.DjangoModelPermissions
# ],

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.

    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'drf_renderer_xlsx.renderers.XLSXRenderer',

    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
}
#         'delab.api.TabbedTextRenderer'
# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_REDIRECT_URL = 'blog-home'
LOGIN_URL = 'login'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS')

# AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

# AWS_S3_FILE_OVERWRITE = False
# AWS_DEFAULT_ACL = None

# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

BACKGROUND_TASK_RUN_ASYNC = False
MAX_RUN_TIME = 2000000
# BACKGROUND_TASK_ASYNC_THREADS = 300
# BACKGROUND_TASK_ASYNC_THREADS = 4

TIME_ZONE = 'Europe/Berlin'

INTERNAL_IPS = [
    '127.0.0.1',
    '0.0.0.0'
]

DEBUG = True

# LOGGING

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            # 'filename': 'debug.log'
            'filename': os.getcwd() + "/logs/debug.log",
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
        },
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            # 'filename': 'debug.log'
            'filename': os.getcwd() + "/logs/error.log",
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
        },

    },
    'loggers': {
        '': {
            'handlers': ['console', 'file', 'file_error'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'numba': {
            'level': 'ERROR'
        },
        'requests': {
            'level': 'ERROR'
        },
        'praw': {
            'level': 'ERROR'
        },
        'prawcore': {
            'level': 'ERROR'
        },
        'neo4j': {
            'level': 'ERROR'
        },
        'twarc': {
            'level': 'WARNING'
        }
    },
}

# delab_settings
# max candidates when downloading Tweets by query must be bigger then 10, quota for lookup is 900
MAX_CANDIDATES = 10000
MIN_CONVERSATION_LENGTH = 10
MAX_CONVERSATION_LENGTH = 500  # tested for 300

TRAX_CAPABILITIES = False  # set this to true only if you running on a linux and have AVX commands available
# sys.setrecursionlimit(2000)
MAX_CANDIDATES_REDDIT = 300
MAX_CANDIDATES_TWITTER = 850

CURRENT_DUO_FLOW_METRIC = "sentiment"


# the number of people that need to label a tweet as intolerant for it to be labeled correctly
min_intolerance_coders_needed = 2
# the number of people that need to validate an answer before it can be sent
min_intolerance_answer_coders_needed = 2

performance_conversation_max_size = 100

MAX_CANDIDATES_DUO_FLOW_ANALYSIS = 50
MAX_DUO_FLOWS_FOR_ANALYSIS = 10

MAX_CCCP_CONVERSATION_CANDIDATES = 1000
CCCP_N_LARGEST = 10

# FLOW_DUO_API_COUNT = 50