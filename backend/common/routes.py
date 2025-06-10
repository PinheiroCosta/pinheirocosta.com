from .views import (
    RestViewSet, 
    ParametroSistemaViewSet, 
    AboutMeViewSet, 
    ProfessionalContactMessageViewSet
)

routes = [
    {"regex": r"rest", "viewset": RestViewSet, "basename": "Rest"},
    {"regex": r"parametros", "viewset": ParametroSistemaViewSet, "basename": "parametro-sistema"},
    {"regex": r"aboutme", "viewset": AboutMeViewSet, "basename": "aboutme"},
    {"regex": r"contato-profissional", "viewset": ProfessionalContactMessageViewSet, "basename": "contato-profissional"},
]
