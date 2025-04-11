from rest_framework.routers import DefaultRouter
from .views import MOTDViewSet, MOTDConfigViewSet

routes = [
    {
        "regex": r"motd",
        "viewset": MOTDViewSet,
        "basename": "motd",
    },
    {
        "regex": r"motd-config",
        "viewset": MOTDConfigViewSet,
        "basename": "motdconfig",
    }
]

