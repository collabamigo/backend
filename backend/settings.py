"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import base64
import json
import os

import firebase_admin
import pymongo
import environ
from dotenv import load_dotenv
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

load_dotenv()

env = environ.Env(
    DATABASE_URL=(str, ""),
    CORS_ORIGIN_WHITELIST=(str, '["http://localhost:3000", "https://collabamigo.xyz"]'),
    ALLOWED_HOSTS=(str, '["localhost", "blooming-peak-53825.herokuapp.com"]'),
    DEVELOPMENT=(bool, True),
    CICD=(bool, False),
    SENTRY_DSN=(str, ""),
    GOOGLE_OAUTH_CLIENT_ID=(str, "109135106784-vn1e2elm5doejfucvusr3fer4rm4mcda.apps.googleusercontent.com"),
)
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEVELOPMENT = env("DEVELOPMENT") or env("CICD")
DEBUG = DEVELOPMENT
GOOGLE_OAUTH_CLIENT_ID = env("GOOGLE_OAUTH_CLIENT_ID")

REST_FRAMEWORK = {'DEFAULT_PERMISSION_CLASSES': [
    'authenticate.permissions.IsTrulyAuthenticatedOrReadOnly'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'authenticate.authentication.DummyAuthentication',
        'authenticate.authentication.CustomAuthentication']}


if DEVELOPMENT and env("CORS_ORIGIN_WHITELIST") == "":
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ORIGIN_WHITELIST = json.loads(env("CORS_ORIGIN_WHITELIST"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "TESTSEcret" if DEVELOPMENT else os.environ['SECRET_KEY']

ALLOWED_HOSTS = json.loads(env("ALLOWED_HOSTS"))

# DataFlair neeche hai
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv("EMAIL")
EMAIL_HOST_PASSWORD = os.getenv("PASS_KEY")

# Application definition hai ye
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'connect.apps.ConnectConfig',
    'corsheaders',
    'autocomplete',
    'club',
    'form',
    'ecell',
    'authenticate',
    'rest_framework.authtoken',
    'users'
]
AUTH_USER_MODEL = 'users.User'

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# TODO: Enable CSRF
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

APPEND_SLASH = True

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

v1 = 'django.contrib.auth.password_validation.'
v2 = 'UserAttributeSimilarityValidator'
v3 = v1 + v2

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': v3,
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

FRONTEND_URL = "https://collabamigo-testing.web.app" if DEVELOPMENT \
    else "https://collabamigo.com"

USE_I18N = True
USE_L10N = True
USE_TZ = True
TIME_ZONE = 'Asia/Kolkata'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]

# CSRF_COOKIE_SECURE = bool(os.getenv("PRODUCTION"))
SECURE_SSL_REDIRECT = bool(os.getenv("PRODUCTION"))
SESSION_COOKIE_SECURE = bool(os.getenv("PRODUCTION"))

if not bool(os.getenv("CICD")):
    MongoClient = pymongo.MongoClient(os.environ['MONGODB_URI'])

ALLOWED_IN_DEBUG = ['aditya20016@iiitd.ac.in', 'shikhar20121@iiitd.ac.in',
                    'heemank20064@iiitd.ac.in', 'heemankv@gmail.com',
                    'pragyan20226@iiitd.ac.in', "dummy.user@collabamigo.com",
                    "khwaish20212@iiitd.ac.in"]

JWT_VALIDITY_IN_DAYS = 1
TOKEN_VALIDITY_IN_DAYS = 3
JWT_SECRET = "TESTSEcret" if DEVELOPMENT else os.environ["JWT_SECRET"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

SENTRY_TRACES_SAMPLE_RATE = 0.001 if DEVELOPMENT else 0.1

sentry_sdk.init(
    dsn=env("SENTRY_DSN"),
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,
    send_default_pii=True
)

if env("DATABASE_URL"):
    DATABASES["default"] = env.db("DATABASE_URL")
    DATABASES["default"]["ATOMIC_REQUESTS"] = True
    DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)

if os.getenv("FIREBASE_CREDENTIALS"):
    print("Firebase credentials found")
    firebase_cred = firebase_admin.credentials.Certificate(json.loads(base64.b64decode(os.getenv(
        "FIREBASE_CREDENTIALS")).decode("utf-8")))
    firebase_app = firebase_admin.initialize_app(firebase_cred)
else:
    firebase_app = None
