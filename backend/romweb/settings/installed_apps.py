def validate_app_dependencies(optional_apps, dependencies):
    enabled_apps = {app for app, enabled in optional_apps.items() if enabled} 
    for app, deps in dependencies.items():
        if app in enabled_apps:
            missing = [dep for dep in deps if dep not in enabled_apps and dep not in BASE_APPS]
            if missing:
                raise RuntimeError(
                    f"App '{app}' requer que os apps {missing} também estejam ativados."
                )


BASE_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django_js_reverse",
    "django_guid",
    "import_export",
    "rest_framework",
    "corsheaders",
    "django_filters",
    "drf_spectacular",
    "webpack_loader",
    "defender",
    "users",
    "common",
    "tinymce",
]

OPTIONAL_APPS = {
    "blog": True,
    "tools": True,
    "motd": True,
    "parceria": True,
}

APP_DEPENDENCIES = {
    'tools': ['common'],
    "parceria": ['users'],
}

validate_app_dependencies(OPTIONAL_APPS, APP_DEPENDENCIES)

INSTALLED_APPS = BASE_APPS + [app for app, enabled in OPTIONAL_APPS.items() if enabled]
