from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page

from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import BlogPostSitemap
from tools.sitemaps import ToolSitemap
from common.sitemaps import AboutMeSitemap, StaticPrivacySitemap
from common.views import RobotsTxtView

import django_js_reverse.views
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter
from common.routes import routes as common_routes
from users.routes import routes as users_routes
from blog.routes import routes as blog_routes
from tools.routes import routes as tool_routes
from motd.routes import routes as motd_routes


router = DefaultRouter()
routes = common_routes + users_routes + blog_routes + tool_routes + motd_routes
for route in routes:
    router.register(route["regex"], route["viewset"], basename=route["basename"])

sitemaps = {
    "blogposts": BlogPostSitemap,
    "tools": ToolSitemap,
    "aboutme": AboutMeSitemap,
    "privacy": StaticPrivacySitemap,
}

urlpatterns = [
    path(
        "sitemap.xml",
        cache_page(60 * 60)(lambda request: sitemap(request, sitemaps=sitemaps)),
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path(
        "robots.txt",
        cache_page(60 * 60 * 48)(RobotsTxtView.as_view()),
        name="robots_txt",
    ),
    path("admin/", admin.site.urls, name="admin"),
    path("admin/defender/", include("defender.urls")),
    path("jsreverse/", django_js_reverse.views.urls_js, name="js_reverse"),
    path("api/", include(router.urls), name="api"),
    path("tinymce/", include("tinymce.urls")),
    path("blog/", include("blog.urls")),
    path("tools/", include("tools.urls")),
    path("", include("common.urls"), name="common"),
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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
