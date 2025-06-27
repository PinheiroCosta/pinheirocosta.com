from .views import BlogPostViewSet

routes = [
    {
        "regex": r"blog",
        "viewset": BlogPostViewSet,
        "basename": "blogpost",
    }
]
