from os import environ
from pathlib import Path
import sys

# from nephele.logging import configure_logging
import django_stubs_ext

# configure_logging()
django_stubs_ext.monkeypatch()

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_ROOT = BASE_DIR / "statics"

SECRET_KEY = "django-insecure-e+!x__nj(73il5*hr5)o(hv3+0)1%8b$$_j$^--psv87j^!^&="

DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    "unfold.contrib.inlines",  # optional, if special inlines are needed
    "unfold.contrib.import_export",  # optional, if django-import-export package is used
    "unfold.contrib.guardian",  # optional, if django-guardian package is used
    "unfold.contrib.simple_history",  # optional, if django-simple-history package is used
    "django.contrib.admin",  # required
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "django_celery_beat",
    # "django_celery_results",
    "apps.user",
    "apps.cloud",
    "apps.data",
    "apps.project",
    "apps.storage",
    "apps.task",
    "apps.usage",
    "ninja_extra",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "nephele.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "nephele.wsgi.application"

DATABASES = {
    # "default": {
    #     "ENGINE": "django.db.backends.sqlite3",
    #     "NAME": BASE_DIR / "db.sqlite3",
    # }
    # "default": {
    #     "ENGINE": "django.db.backends.mysql",
    #     "NAME": "test-db",
    #     "HOST": "localhost",
    #     "USER": "root",
    #     "PASSWORD": "test",
    # }
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "nephele",  # Replace with your actual database name
        "HOST": environ.get("DATABASES__DEFAULT__HOST", "localhost"),
        "USER": "postgres",
        "PASSWORD": "example",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

INTERNAL_IPS = [
    "127.0.0.1",
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Celery Configuration Options
CELERY_TIMEZONE = "UTC"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_BROKER_URL = "amqp://user:password@broker:5672//"
# CELERY_RESULT_BACKEND = 'django-cache'
CELERY_RESULT_BACKEND = "django-db"
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
# # pick which cache from the CACHES setting.
# CELERY_CACHE_BACKEND = 'default'

# # django setting.
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#         'LOCATION': 'celery_task_caches',
#     }
# }

TESTING = "test" in sys.argv
if DEBUG and not TESTING:
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]
    INSTALLED_APPS += [
        "debug_toolbar",
    ]

    INTERNAL_IPS = [
        "127.0.0.1",
    ]

    # this is the main reason for not showing up the toolbar
    import mimetypes

    mimetypes.add_type("application/javascript", ".js", True)

    DEBUG_TOOLBAR_CONFIG = {"INSERT_BEFORE": "</body>"}

    # from here down are desperate attempts to get it to load.
    def show_toolbar(request):
        return True

    SHOW_TOOLBAR_CALLBACK = show_toolbar

    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": lambda request: True,
    }
