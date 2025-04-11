from django.conf import settings


def is_rich_text_enabled() -> bool:
    return 'tinymce' in settings.INSTALLED_APPS
