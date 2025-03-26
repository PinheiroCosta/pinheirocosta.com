from rest_framework.routers import DefaultRouter
from .views import BlogPostViewSet

routes = [
    {
        "regex": r"blog",
        "viewset": BlogPostViewSet,
        "basename": "blogpost",
    }
]

