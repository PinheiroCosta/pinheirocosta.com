from .views import ToolViewSet

routes = [
    {
        "regex": r"tools",
        "viewset": ToolViewSet,
        "basename": "tools",
    }
]
