"""
Django settings for task_manager project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

# ------------------------------------------------------------------------------
# Base
# ------------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

DEBUG = os.getenv("DEBUG", "False") == "True"

SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-secret-key-for-dev")

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "webserver",
]

if not DEBUG:
    ALLOWED_HOSTS.append(".onrender.com")

# ------------------------------------------------------------------------------
# Applications
# ------------------------------------------------------------------------------

INSTALLED_APPS = [
    "task_manager_app",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_bootstrap5",
    "django_filters",
]

# ------------------------------------------------------------------------------
# Middleware
# ------------------------------------------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "task_manager_app.rollbar_middleware.CustomRollbarNotifierMiddleware",
]

# ------------------------------------------------------------------------------
# URLs / WSGI
# ------------------------------------------------------------------------------

ROOT_URLCONF = "task_manager.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "task_manager.wsgi.application"

# ------------------------------------------------------------------------------
# Database
# ------------------------------------------------------------------------------

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ------------------------------------------------------------------------------
# Password validation
# ------------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ------------------------------------------------------------------------------
# I18N
# ------------------------------------------------------------------------------

LANGUAGE_CODE = "en"

TIME_ZONE = "UTC"

USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ("en", "English"),
    ("ru", "Russian"),
]

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

# ------------------------------------------------------------------------------
# Static
# ------------------------------------------------------------------------------

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
    if not DEBUG
    else "django.contrib.staticfiles.storage.StaticFilesStorage"
)

# ------------------------------------------------------------------------------
# Auth redirects
# ------------------------------------------------------------------------------

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "index"
LOGOUT_REDIRECT_URL = "index"

# ------------------------------------------------------------------------------
# Default PK
# ------------------------------------------------------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ------------------------------------------------------------------------------
# Rollbar
# ------------------------------------------------------------------------------

ROLLBAR_ACCESS_TOKEN = os.getenv("ROLLBAR_ACCESS_TOKEN")

if ROLLBAR_ACCESS_TOKEN and not DEBUG:
    ROLLBAR = {
        "access_token": ROLLBAR_ACCESS_TOKEN,
        "environment": "production",
        "root": BASE_DIR,
    }
else:
    ROLLBAR = {}
