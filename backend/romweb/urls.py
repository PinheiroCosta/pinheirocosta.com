from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.contrib.sitemaps.views import sitemap
from django.views.decorators.cache import cache_page
from django.conf.urls.static import static

from common.sitemaps import AboutMeSitemap, StaticPrivacySitemap
from common.views import RobotsTxtView
from rest_framework.routers import DefaultRouter
from common.routes import routes as common_routes
from users.routes import routes as users_routes

import django_js_reverse.views
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


router = DefaultRouter()
routes = common_routes + users_routes
sitemaps = {
    "aboutme": AboutMeSitemap,
    "privacy": StaticPrivacySitemap,
}

urlpatterns = []

OPTIONAL_URLS = {
    "blog": "blog.urls_registry",
    "tools": "tools.urls_registry",
    "motd": "motd.urls_registry",
    "parceria": "parceria.urls_registry",
}

for app, module_path in OPTIONAL_URLS.items():
    if settings.OPTIONAL_APPS.get(app, False):
        try:
            mod = __import__(module_path, fromlist=[""])
            if hasattr(mod, "SITEMAPS"):  # ou mod.SITEMAPS
                sitemaps.update(mod.SITEMAPS)
            if hasattr(mod, "URLPATTERNS"):  # ou mod.URLPATTERNS
                urlpatterns += mod.URLPATTERNS
            if hasattr(mod, "ROUTES"):  # para routers
                routes += mod.ROUTES
        except ImportError as e:
            raise RuntimeError(f"Erro ao importar URLs ou Sitemaps de {app}: {e}")


for route in routes:
    router.register(route["regex"], route["viewset"], basename=route["basename"])

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("admin/defender/", include("defender.urls")),
    path("api/", include(router.urls), name="api"),
    path("jsreverse/", django_js_reverse.views.urls_js, name="js_reverse"),
    path("blog/", include("blog.urls")),
    path("tools/", include("tools.urls")),
    path("robots.txt", cache_page(60 * 60 * 48)(RobotsTxtView.as_view())),
    path(
        "sitemap.xml",
        cache_page(60 * 60)(lambda request: sitemap(request, sitemaps=sitemaps)),
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("tinymce/", include("tinymce.urls")),
    # drf-spectacular
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("", include("common.urls"), name="common"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
