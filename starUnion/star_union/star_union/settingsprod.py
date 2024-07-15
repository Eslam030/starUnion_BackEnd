"""
Django settings for star_union project.

Generated by 'django-admin startproject' using Django 4.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""


from pathlib import Path
from django.utils.crypto import get_random_string

# JWT settings
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# will activate it when deploying
# chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
# SECRET_KEY = get_random_string(50, chars)

SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['starunion.pythonanywhere.com', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'jazzmin',
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'events',
    'routing',
    'main',
    'workshops'
]

JAZZMIN_SETTINGS = {
    "site_title": "Star Union",
    "site_header": "Star Union",
    "site_footer": "Star Union",
    "site_brand": "Star Union",
    "welcome_sign": "Welcome to Star Union Admin",
    "copyright": "Star Union",
    "site_logo": "assets/img/logo.png",
    "changeform_format": "vertical_tabs",
    "site_favicon": "assets/img/logo.png",
    "show_ui_builder": True
}


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT', 'Bearer'),
    'ACCESS_TOKEN_LIFETIME': timedelta(seconds=20),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=10),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,

}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]


CORS_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True


# this will be changed
CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:5500',
    'http://localhost:5173'
]
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'PATCH',
    'POST',
    'PUT',
]

ROOT_URLCONF = 'star_union.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'html'],
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

WSGI_APPLICATION = 'star_union.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


DATABASES = {
    "default": {
    },
    "main_db": {
        "NAME": 'star_union',
        'USER': 'star_union_user',
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "PASSWORD": os.environ.get('DB_PASSWORD'),
        "HOST": 'localhost',
        "PORT": '',
    },
    "workshops_db": {
        "NAME": BASE_DIR / "workshops.sqlite3",
        "ENGINE": "django.db.backends.sqlite3",
    },
    "events_db": {
        "NAME": BASE_DIR / "events.sqlite3",
        "ENGINE": "django.db.backends.sqlite3",
    }
}
# DATABASES['default'] = dj_database_url.parse(
#     'postgres://teststarunion_user:KYiGJalY8eEZqIJR672AaY6y6SjPjQu7@dpg-cnieso779t8c73brv2ug-a.oregon-postgres.render.com/teststarunion')

# Custom Authentication to our custom user
AUTHENTICATION_BACKEND = []

DATABASE_ROUTERS = ['star_union.routers.mainRouter']

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Cairo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'public'
]
STATIC_ROOT = BASE_DIR / 'static'

INTERAL_IPS = [
    'localhost',
    '127.0.0.1'
]
