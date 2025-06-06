from django.urls import path, include
from .views import ToolDetailView

app_name = "tools"

urlpatterns = [
    path('tools/<slug:slug>/', ToolDetailView.as_view(), name="detail"),
]

