from django.contrib import admin
from .models import Tool, ToolIOField, ToolIOOption


class ToolIOOptionInline(admin.TabularInline):
    model = ToolIOOption
    extra = 1
    verbose_name = "Opção"
    verbose_name = "Opçõe"


class ToolIOFieldInline(admin.TabularInline):
    model = ToolIOField
    extra = 1
    show_change_link = True

@admin.register(ToolIOField)
class ToolIOFieldAdmin(admin.ModelAdmin):
    list_display = ("label", "io_type", "field_type", "tool")
    list_filter = ('io_type', 'field_type', 'tool')
    inlines = [ToolIOOptionInline]

@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('name', "category", "active")
    list_filter = ('active',)
    inlines = [ToolIOFieldInline]
    search_fields = ('name', 'description')
    prepopulated_fields = {"slug": ("name",)}

