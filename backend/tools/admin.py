from django.contrib import admin
from .models import Tool, ToolField, ToolFieldOption


class ToolFieldOptionInline(admin.TabularInline):
    model = ToolFieldOption
    extra = 1
    ordering = ["order"]
    verbose_name = "Opção"
    verbose_name_plural = "Opções"


class ToolFieldInline(admin.TabularInline):
    model = ToolField
    extra = 1
    show_change_link = True


@admin.register(ToolField)
class ToolFieldAdmin(admin.ModelAdmin):
    list_display = ("label", "name", "io_type", "data_type", "widget_type", "tool")
    list_filter = ("io_type", "data_type", "widget_type", "tool")
    search_fields = ("label", "name", "tool__name")
    inlines = [ToolFieldOptionInline]
    ordering = ["tool", "io_type", "id"]


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('name', "category", "active", "slug")
    list_filter = ('category', 'active',)
    search_field = ("name", "description", "slug")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ToolFieldInline]
    ordering = ["category", "name"]
