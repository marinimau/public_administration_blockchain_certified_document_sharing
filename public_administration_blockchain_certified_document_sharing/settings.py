"""
 ________  ________  ________  ________  ________  ________
|\   __  \|\   __  \|\   __  \|\   ____\|\   ___ \|\   ____\
\ \  \|\  \ \  \|\  \ \  \|\ /\ \  \___|\ \  \_|\ \ \  \___|_
 \ \   ____\ \   __  \ \   __  \ \  \    \ \  \ \\ \ \_____  \
  \ \  \___|\ \  \ \  \ \  \|\  \ \  \____\ \  \_\\ \|____|\  \
   \ \__\    \ \__\ \__\ \_______\ \_______\ \_______\____\_\  \
    \|__|     \|__|\|__|\|_______|\|_______|\|_______|\_________\
                                                     \|_________|

public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
Created at: 19/06/21
By: mauromarini
License: MIT
Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
Credits: @marinimau (https://github.com/marinimau)


Django settings for public_administration_blockchain_certified_document_sharing project.

Generated by 'django-admin startproject' using Django 3.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

PROJECT_INFO = {
    'NAME': 'Public Administration Blockchain Certified Document Sharing',
    'DESCRIPTION': 'A dApp to share blockchain certified documents from Public Administration to Citizen',
    'VERSION': '1.0.0-beta'
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@uc-%1m^jdz%6bd(-wxp&g@tk*n%@lucl=g_)u7!dwmb#ffhpg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# SITE URL
SITE_URL = 'https://siteurl.com/'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'gnosis',
    'qr_code',
    'api.user',
    'api.document',
    'api.transaction',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'public_administration_blockchain_certified_document_sharing.urls'

LOGIN_REDIRECT_URL = '/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'public_administration_blockchain_certified_document_sharing.wsgi.application'

# Rest Framework

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ],
    'TEST_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'TEST_REQUEST_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ]
}

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Blockchain params

HTTP_PROVIDER_URL = 'https://rinkeby.infura.io/v3/3ef38272cfde40faa0af05d47918d339'
GAS_CONTRACT_DEPLOY = 1500000
GAS_PRICE = 30000000000


# Media directory
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    'static/',
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
