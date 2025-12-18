import os
from decouple import config
from dj_database_url import parse as db_url
from .installed_apps import INSTALLED_APPS, OPTIONAL_APPS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def base_dir_join(*args):
    return os.path.join(BASE_DIR, *args)


SITE_ID = 1

DEBUG = True

APPEND_SLASH = True

ADMINS = (("Admin", "romulo@pinheirocosta.com"),)

AUTH_USER_MODEL = "users.User"

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": config("DATABASE_URL", cast=db_url),
}



MIDDLEWARE = [
    "django.middleware.gzip.GZipMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django_permissions_policy.PermissionsPolicyMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "common.middleware.cache_control.DefaultCacheControlMiddleware",
    "csp.middleware.CSPMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "defender.middleware.FailedLoginMiddleware",
    "django_guid.middleware.guid_middleware",
]

CORS_ALLOWED_ORIGINS = [
    "https://www.pinheirocosta.com",
    "https://pinheirocosta.com",
]

ROOT_URLCONF = "romweb.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [base_dir_join("templates")],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "common.context_processors.sentry_dsn",
                "common.context_processors.commit_sha",
            ],
            "loaders": [
                (
                    "django.template.loaders.cached.Loader",
                    [
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                    ],
                ),
            ],
        },
    },
]

WSGI_APPLICATION = "romweb.wsgi.application"

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

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 6,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# drf-spectacular
SPECTACULAR_SETTINGS = {
    "TITLE": "Romweb API",
    "DESCRIPTION": "Api pública para o site pessoal pinheirocosta.com.",
    "VERSION": "0.1.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "COMPONENT_SPLIT_PATCH": True,
    "SORT_OPERATIONS": False,
    "SORT_OPERATION_PARAMETERS": False,
}

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True

STATICFILES_DIRS = (base_dir_join("../frontend/webpack_bundles"),)

# Webpack
WEBPACK_LOADER = {
    "DEFAULT": {
        "BUNDLE_DIR_NAME": "assets/",
        "CACHE": False,
        "STATS_FILE": base_dir_join("../webpack-stats.json"),
        "POLL_INTERVAL": 0.1,
        "IGNORE": [r".+\.hot-update.js", r".+\.map"],
    }
}

# Celery
# Recommended settings for reliability: https://gist.github.com/fjsj/da41321ac96cf28a96235cb20e7236f6
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_ACKS_LATE = True
CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_TRANSPORT_OPTIONS = {"confirm_publish": True, "confirm_timeout": 5.0}
CELERY_BROKER_POOL_LIMIT = config("CELERY_BROKER_POOL_LIMIT", cast=int, default=1)
CELERY_BROKER_CONNECTION_TIMEOUT = config(
    "CELERY_BROKER_CONNECTION_TIMEOUT", cast=float, default=30.0
)
CELERY_REDIS_MAX_CONNECTIONS = config(
    "CELERY_REDIS_MAX_CONNECTIONS", cast=lambda v: int(v) if v else None, default=None
)
CELERY_TASK_ACKS_ON_FAILURE_OR_TIMEOUT = config(
    "CELERY_TASK_ACKS_ON_FAILURE_OR_TIMEOUT", cast=bool, default=True
)
CELERY_TASK_REJECT_ON_WORKER_LOST = config(
    "CELERY_TASK_REJECT_ON_WORKER_LOST", cast=bool, default=False
)
CELERY_WORKER_PREFETCH_MULTIPLIER = config(
    "CELERY_WORKER_PREFETCH_MULTIPLIER", cast=int, default=1
)
CELERY_WORKER_CONCURRENCY = config(
    "CELERY_WORKER_CONCURRENCY", cast=lambda v: int(v) if v else None, default=None
)
CELERY_WORKER_MAX_TASKS_PER_CHILD = config(
    "CELERY_WORKER_MAX_TASKS_PER_CHILD", cast=int, default=1000
)
CELERY_WORKER_SEND_TASK_EVENTS = config(
    "CELERY_WORKER_SEND_TASK_EVENTS", cast=bool, default=True
)
CELERY_EVENT_QUEUE_EXPIRES = config(
    "CELERY_EVENT_QUEUE_EXPIRES", cast=float, default=60.0
)
CELERY_EVENT_QUEUE_TTL = config("CELERY_EVENT_QUEUE_TTL", cast=float, default=5.0)

# Sentry
SENTRY_DSN = config("SENTRY_DSN", default="")
COMMIT_SHA = config("RENDER_GIT_COMMIT", default="")

# Fix for Safari 12 compatibility issues, please check:
# https://github.com/vintasoftware/safari-samesite-cookie-issue
CSRF_COOKIE_SAMESITE = None
SESSION_COOKIE_SAMESITE = None

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# All available policies are listed at:
# https://github.com/w3c/webappsec-permissions-policy/blob/main/features.md
# Empty list means the policy is disabled
PERMISSIONS_POLICY = {
    "accelerometer": [],
    "camera": [],
    "display-capture": [],
    "encrypted-media": [],
    "geolocation": [],
    "gyroscope": [],
    "magnetometer": [],
    "microphone": [],
    "midi": [],
    "payment": [],
    "usb": [],
    "xr-spatial-tracking": [],
}

# Django-CSP
CSP_INCLUDE_NONCE_IN = ["script-src", "style-src", "font-src"]
CSP_SCRIPT_SRC = [
    "'self'",
    "'unsafe-inline'",
    "'unsafe-eval'",
    "https://browser.sentry-cdn.com",
    # drf-spectacular UI (Swagger and ReDoc)
    "https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest/",
    "https://cdn.jsdelivr.net/npm/redoc@latest/",
    "https://www.google.com",
    "https://www.gstatic.com",
    "blob:",
] + [f"*{host}" if host.startswith(".") else host for host in ALLOWED_HOSTS]
CSP_CONNECT_SRC = [
    "'self'",
    "*.sentry.io",
] + [f"*{host}" if host.startswith(".") else host for host in ALLOWED_HOSTS]
CSP_STYLE_SRC = [
    "'self'",
    "'unsafe-inline'",
    # drf-spectacular UI (Swagger and ReDoc)
    "https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest/",
    "https://cdn.jsdelivr.net/npm/redoc@latest/",
    "https://fonts.googleapis.com",
]
CSP_FONT_SRC = [
    "'self'",
    "'unsafe-inline'",
    # drf-spectacular UI (Swagger and ReDoc)
    "https://fonts.gstatic.com",
] + [f"*{host}" if host.startswith(".") else host for host in ALLOWED_HOSTS]
CSP_IMG_SRC = [
    "'self'",
    "blob:",
    "filesystem:",
    # drf-spectacular UI (Swagger and ReDoc)
    "data:",
    "https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest/",
    "https://cdn.redoc.ly/redoc/",
    "https://cdn.buymeacoffee.com",
    config("AWS_S3_CUSTOM_DOMAIN", default=""),
]
CSP_FRAME_SRC = [
    "https://www.google.com",
]
CSP_FRAME_ANCESTORS = ["'none'"]

# Django-defender
DEFENDER_LOGIN_FAILURE_LIMIT = 3
DEFENDER_COOLOFF_TIME = 300  # 5 minutes
DEFENDER_LOCKOUT_TEMPLATE = "defender/lockout.html"
DEFENDER_REDIS_URL = config("REDIS_URL")

# Idempotency
IDEMPOTENCY_TTL = 120

# Django-tinymce
TINYMCE_DEFAULT_CONFIG = {
    "height": 500,
    "width": "100%",
    "menubar": True,
    "plugins": "advlist autolink lists link image charmap preview anchor codesample "
    "searchreplace visualblocks code fullscreen insertdatetime media table code help wordcount",
    "toolbar": "undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | "
    "bullist numlist outdent indent | link image media | code codesample",
    "image_advtab": True,
    "media_live_embeds": True,
}

# RECAPTCHA CONFIG
RECAPTCHA_SECRET_KEY = config("RECAPTCHA_SECRET_KEY")
RECAPTCHA_MIN_SCORE = 0.8
RECAPTCHA_BYPASS = DEBUG

# JAZZMIN
JAZZMIN_SETTINGS = {
    "site_title": "Pinheirocosta.com",
    "site_brand": "Administração",
    "welcome_sign": None,
    "site_icon": None,
    "copyright": "- PinheiroCosta.com",
    "show_ui_builder":  True,
    "icons": {
         "auth": "fas fa-users-cog",
         "users.User": "fas fa-user",
         "auth.Group": "fas fa-users",
         "blog.Tag": "fas fa-tags",
         "blog.BlogPost": "fas fa-book",
         "defender.AccessAttempt": "fas fa-shield",
         "common.RobotsTxt": "fas fa-sitemap",
         "common.ProfessionalContactMessage": "fas fa-envelope",
         "common.AboutMe": "fas fa-address-card",
         "common.ParametroSistema": "fas fa-key",
         "motd.MOTD": "fas fa-quote-left",
         "motd.MOTDConfig": "fas fa-gears",
         "tools.Tool": "fas fa-gear",
         "tools.ToolField": "fas fa-gears",
         "parceria.Parceria": "fas fa-handshake",
         "parceria.PedidoServico": "fas fa-cart-shopping",
         "parceria.Servico": "fas fa-shop",
         "parceria.TicketSuporte": "fas fa-comment-medical",
         "parceria.ContratoServico": "fas fa-file-signature",
    },
}
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": True,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": True,
    "brand_colour": "navbar-teal",
    "accent": "accent-teal",
    "navbar": "navbar-teal navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-teal",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "sandstone",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}
