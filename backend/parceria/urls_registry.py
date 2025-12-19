from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .routes import routes

router = DefaultRouter()
for route in routes:
    router.register(
        route["regex"].replace("parcerias/", ""),
        route["viewset"],
        basename=route["basename"],
    )

URLPATTERNS = [
    path("api/parcerias/", include((router.urls, "parcerias"), namespace="parcerias")),
]

SITEMAPS = {}
ROUTES = routes
