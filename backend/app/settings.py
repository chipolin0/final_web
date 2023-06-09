"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

from datetime import timedelta
import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')

# SECURITY WARNING: don't run with debug turned on in production!
# To disable debug, remove the variable from the environment instead of trying to type cast
DEBUG = int(os.environ.get("DEBUG", default=0))


# 'DJANGO_ALLOWED_HOSTS' should be a single string of hosts with a space between each.
# For example: 'DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]'
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost 127.0.0.1 [::1]").split(" ")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #'corsheaders',
    'solo.apps.SoloAppConfig',
    'rest_framework',
    'drf_yasg',
    'djoser',
    'django_celery_beat',
    'django_celery_results',
    'djcelery_email',

    # Local
    'users.apps.UsersConfig',
    'education.apps.EducationConfig',
    'pages.apps.PagesConfig',

    'django_cleanup.apps.CleanupConfig',
]

AUTH_USER_MODEL = 'users.CustomUser'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/staticfiles/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = '/mediafiles/'
MEDIA_ROOT = os.path.join(BASE_DIR, "/mediafiles/")


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}


SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT', 'Bearer'),
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),   # timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}


DJOSER = {
    'TOKEN_MODEL': None,  # needed for JWT
    'PERMISSIONS': {
        'user_delete': ['users.permissions.IsAdminUser'],
    },
    'SERIALIZERS': {
        'user_create': 'users.serializers.CustomUserCreateSerializer',
        'user': 'users.serializers.CustomUserWithProfileSerializer',
        'current_user': 'users.serializers.CustomUserSerializer',
    },
    # 'HIDE_USERS': If set to True, listing /users/ enpoint by normal user will return only that user’s
    # profile in the list. Beside that, accessing /users/<id>/ endpoints by user without
    # proper permission will result in HTTP 404 instead of HTTP 403.
    'HIDE_USERS': True,
    'ACTIVATION_URL': 'users/activation/{uid}/{token}',  # TODO: urls in frontend, POST to back
    'PASSWORD_RESET_CONFIRM_URL': 'users/password/reset/confirm/{uid}/{token}',  # TODO: urls in frontend, POST to back
    'USERNAME_RESET_CONFIRM_URL': 'users/reset/confirm/{uid}/{token}',  # TODO: urls in frontend, POST to back
    'SEND_ACTIVATION_EMAIL': False,
    'SEND_CONFIRMATION_EMAIL': False,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': False,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': False,
    'EMAIL': {
        'activation': 'users.emails.CustomActivationEmail',
        'confirmation': 'users.emails.CustomConfirmationEmail',
        'password_reset': 'users.emails.CustomPasswordResetEmail',
        'password_changed_confirmation': 'users.emails.CustomPasswordChangedConfirmationEmail',
        'username_changed_confirmation': 'users.emails.CustomUsernameChangedConfirmationEmail',
        'username_reset': 'users.emails.CustomUsernameResetEmail',
    }
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        }
    },
}


CELERY_BROKER_URL = os.environ.get('REDIS_URL')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE


EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'

EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.sendgrid.net')
EMAIL_PORT = os.environ.get('EMAIL_PORT', 587)
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', True)

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@webmaster')

CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = (
    # can be like r'^https://\w+\.example\.com$'
    os.environ.get('CORS_ORIGIN_WHITELIST', 'http://localhost:3000'),
)


if 'SENTRY_DSN' in os.environ:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=os.environ['SENTRY_DSN'], integrations=[DjangoIntegration()]
    )

# try:
#     from local_settings import *
# except ImportError as e:
#     # No local settings was found, skipping.
#     pass

# if not DEBUG and len(SECRET_KEY) < 25:
#     print(f'The value of DJANGO_SECRET_KEY does not contain enough characters ({len(SECRET_KEY)} characters)')
#     raise RuntimeError(f'DJANGO_SECRET_KEY is not long enough (in environment variable "DJANGO_SECRET_KEY")')
