from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MOTDViewSet, MOTDConfigViewSet

router = DefaultRouter()
router.register(r'api/motd', MOTDViewSet, basename='motd')
router.register(r'api/motd-config', MOTDConfigViewSet, basename='motdconfig')

urlpatterns = [
    path('', include(router.urls)),
]

