"""
Django settings for application project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from decouple import config
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret! 
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production! 
DEBUG = config('DEBUG',True,cast=bool)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_spectacular',
    # authentication
    'django.contrib.sites',
    'rest_framework.authtoken',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    # password reset
    'django_rest_passwordreset',
    # login and logout
    'knox',
    # apps
    'customers.apps.CustomersConfig',
    'pocket',
    'products',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'application.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR/'templates',
        ],
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

WSGI_APPLICATION = 'application.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config("NAME"),
        'USER': config("USER"),
        'PASSWORD': config("PASSWORD"),
        'HOST': config("HOST"),
        'PORT': config("PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT= BASE_DIR/'staticfiles'

STATICFILES_DIRS= [BASE_DIR/'static']

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# REST Framework settings

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES" : ["knox.auth.TokenAuthentication",],
}


# KNOX SETTINGS

REST_KNOX = {
    "TOKEN_TTL": timedelta(days=1),
    "AUTH_HEADER_PREFIX": "Bearer",
}


# DJ-REST-AUTH SETTINGS

REST_AUTH = {
    'OLD_PASSWORD_FIELD_ENABLED': True, # old password is required during password change
    'LOGOUT_ON_PASSWORD_CHANGE': True, # forcefully logged out after password change
}

SITE_ID = 1


# ALLAUTH SETTINGS

AUTHENTICATION_BACKENDS = [
   'django.contrib.auth.backends.ModelBackend', # Needed to login by username in Django admin, regardless of `allauth`
   'allauth.account.auth_backends.AuthenticationBackend', # `allauth` specific authentication methods, such as login by email
]


# AUTHENTICATION AND VERIFICATION

ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_AUTHENTICATION_METHOD = 'email'

ACCOUNT_ADAPTER = 'pocket.views.EcommerceAPIAccountAdapter'

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3


# EMAIL CONFIGURATION

EMAIL_BACKEND = "anymail.backends.mailjet.EmailBackend"

DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")

ANYMAIL = {
    "MAILJET_API_KEY":config("MAILJET_API_KEY"),
    "MAILJET_SECRET_KEY":config("MAILJET_SECRET_KEY"),
}


# Spectacular settings

SPECTACULAR_SETTINGS = {
    "TITLE": "ECommerce",
    "DESCRIPTION": "Savannah Informatics Backend Developer Challenge",
    "VERSION": "1.0.0",
    "CONTACT":{
        "name": "George Mobisa",
        "email": "georgemobisa23@outlook.com",
    },
}