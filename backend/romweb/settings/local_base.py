from .base import *
from decouple import config

DEBUG = True

HOST = "http://localhost:8000"

SECRET_KEY = "secret"  # noqa: S105

STATIC_ROOT = base_dir_join("staticfiles")
STATIC_URL = "/static/"

MEDIA_ROOT = base_dir_join("media")
MEDIA_URL = "/media/"

USE_R2 = config("USE_R2", default=False, cast=bool)
STORAGES = {
    "default": {
        "BACKEND": (
            "common.storage_backends.MediaR2Storage"
            if USE_R2
            else "django.core.files.storage.FileSystemStorage"
        ),
        "OPTIONS": {
            "bucket_name": config("AWS_STORAGE_BUCKET_NAME"),
            "access_key": config("AWS_ACCESS_KEY_ID"),
            "secret_key": config("AWS_SECRET_ACCESS_KEY"),
            "endpoint_url": config("AWS_S3_ENDPOINT_URL"),
            "custom_domain": config("AWS_S3_CUSTOM_DOMAIN"),
            "region_name": "auto",
            "addressing_style": "path",
            "default_acl": None,
            "querystring_auth": False,
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config("REDIS_URL")+"/0",
    }

}

AUTH_PASSWORD_VALIDATORS = []  # allow easy passwords only on local

# Celery
CELERY_BROKER_URL = config("CELERY_BROKER_URL", default="")
CELERY_TASK_ALWAYS_EAGER = False
CELERY_TASK_EAGER_PROPAGATES = True

# Email settings for mailhog
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "mailhog"
EMAIL_PORT = 1025

LOG_REQUESTS = True

# HTTP_LOG_ENABLED
# ---------------------------------------------------------
# Enable/disable backend HTTP request/response logging.
# Used only for debugging communication with microservices.
# WARNING: Keep disabled in production unless 100% necessary.
HTTP_LOG_ENABLED = False

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "correlation_id": {"()": "django_guid.log_filters.CorrelationId"},
    },
    "formatters": {
        "standard": {
            "format": "[%(asctime)s] [%(correlation_id)s] [%(levelname)s] %(name)s: %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "filters": ["correlation_id"],
        },
    },
    "loggers": {
        "": {"handlers": ["console"], "level": "INFO"},
        "celery": {"handlers": ["console"], "level": "INFO"},
        "django_guid": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "backend.http": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

JS_REVERSE_JS_MINIFY = False

# Django-CSP
LOCAL_HOST_URL = "http://localhost:3000"
LOCAL_HOST_WS_URL = "ws://localhost:3000/ws"
CSP_SCRIPT_SRC += [LOCAL_HOST_URL, LOCAL_HOST_WS_URL]
CSP_CONNECT_SRC += [LOCAL_HOST_URL, LOCAL_HOST_WS_URL]
CSP_FONT_SRC += [LOCAL_HOST_URL]
CSP_IMG_SRC += [LOCAL_HOST_URL]
