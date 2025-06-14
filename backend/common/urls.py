from django.urls import path, re_path
from . import views 


app_name = "common"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    re_path(r"^(?!api/|admin/|static/|media/).*", views.SpaIndexView.as_view(), name="catch_all"),
]
