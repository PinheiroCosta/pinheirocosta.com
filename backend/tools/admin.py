from django.contrib import admin
from .models import Tool

@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'api_url', 'created_at')
    list_filter = ('active',)
    search_fields = ('name', 'description')
    prepopulated_fields = {"slug": ("name",)}

