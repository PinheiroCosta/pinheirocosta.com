from django.urls import include, path
from .routes import routes as motd_routes
from . import urls as motd_urls


SITEMAPS = {}

URLPATTERNS = [
    path("motd/", include((motd_urls, "motd"), namespace="motd")),
]

ROUTES = motd_routes
