from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogPostViewSet, BlogPostDetailView


app_name = "blog"

urlpatterns = [
    path("<slug:slug>/", BlogPostDetailView.as_view(), name="post_detail"),
]
