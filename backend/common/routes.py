from .views import RestViewSet, ParametroSistemaViewSet, AboutMeViewSet


routes = [
    {"regex": r"rest", "viewset": RestViewSet, "basename": "Rest"},
    {"regex": r"parametros", "viewset": ParametroSistemaViewSet, "basename": "parametro-sistema"},
    {"regex": r"aboutme", "viewset": AboutMeViewSet, "basename": "aboutme"},
]
