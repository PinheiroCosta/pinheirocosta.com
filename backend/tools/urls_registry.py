from django.urls import include, path
from .sitemaps import ToolSitemap
from .routes import routes as tool_routes
from . import urls as tool_urls


SITEMAPS = {
    "tools": ToolSitemap,
}

URLPATTERNS = [
    path("tool/", include((tool_urls, "tools"), namespace="tools")),
]

ROUTES = tool_routes
