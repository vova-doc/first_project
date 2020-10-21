import os
from pathlib import Path

import dj_database_url
import sentry_sdk
from dynaconf import settings as _ds
from sentry_sdk.integrations.django import DjangoIntegration

DEBUG = _ds.DEBUG

if not DEBUG:
    sentry_sdk.init(
     dsn=_ds.SENTRY_DSN,
     integrations=[DjangoIntegration()],
     traces_sample_rate=1.0,
     send_default_pii=True,
 )

REPO_DIR = Path(__file__).resolve().parent.parent.parent
BASE_DIR = REPO_DIR / "src"
PROJECT_DIR = BASE_DIR / "project"

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = _ds.SECRET_KEY

DEBUG = _ds.DEBUG

ALLOWED_HOSTS = _ds.ALLOWED_HOSTS + ["localhost", "127.0.0.1"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # ниже регестрация своих приложений
    "applications.hello.apps.HelloConfig",
    "applications.home.apps.HomeConfig",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [PROJECT_DIR / "templates",],
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

WSGI_APPLICATION = 'project.wsgi.application'

database_url = os.getenv("DATABASE_URL", _ds.DATABASE_URL)

DATABASES = {
    "default": dj_database_url.parse(database_url),
}

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



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



STATIC_URL = "/s/"
STATICFILES_DIRS = [
     PROJECT_DIR / "static",
 ]
STATIC_ROOT = REPO_DIR / ".static"
if not DEBUG:
     STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

