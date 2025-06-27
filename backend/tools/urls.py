from django.urls import path, include
from .views import ToolDetailView

app_name = "tools"

urlpatterns = [
    path("<slug:slug>/", ToolDetailView.as_view(), name="detail"),
]
