from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import redirect
from django.utils.html import format_html
from .models import ParametroSistema, AboutMe, RobotsTxt


@admin.register(RobotsTxt)
class RobotsTxtAdmin(admin.ModelAdmin):
    list_display = ["id", "last_modified"]
    readonly_fields = ["last_modified"]


@admin.register(AboutMe)
class AboutMeAdmin(admin.ModelAdmin):
    list_display = ["preview", "about_text"]
    readonly_fields = ["preview"]

    def has_add_permission(self, request):
        """Impede que o botão 'Add About Me' seja mostrado se já houver um registro."""
        return not AboutMe.objects.exists()

    def save_model(self, request, obj, form, change):
        if not change and AboutMe.objects.exists():
            self.message_user(
                request,
                "Só é permitido um único registro de 'Sobre Mim'.",
                level=messages.ERROR
            )
            return
        super().save_model(request, obj, form, change)
        
    def preview(self, obj):
        """Previsualização da imagem no Django Admin."""
        if obj.about_image and hasattr(obj.about_image, 'url'):
            return format_html('<img src="{}" width="200" style="object-fit:contain;"/>', obj.about_image.url)
        return "(Sem imagem)"


admin.site.register(ParametroSistema)
