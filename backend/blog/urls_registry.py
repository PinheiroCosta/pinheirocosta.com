from django.urls import include, path
from .sitemaps import BlogPostSitemap
from .routes import routes as blog_routes
from . import urls as blog_urls


SITEMAPS = {
    "blogposts": BlogPostSitemap,
}

URLPATTERNS = [
    path("blog/", include((blog_urls, "blog"), namespace="blog")),
]

ROUTES = blog_routes
