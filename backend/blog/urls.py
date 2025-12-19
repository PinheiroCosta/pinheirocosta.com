from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogPostViewSet, BlogPostDetailView, tinymce_upload


app_name = "blog"

urlpatterns = [
    path("<slug:slug>/", BlogPostDetailView.as_view(), name="post_detail"),
    path("tinymce/upload/", tinymce_upload, name="tinymce-upload"),
]
