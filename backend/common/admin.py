from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import redirect
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.template.response import TemplateResponse
from .models import ParametroSistema, AboutMe


@admin.register(AboutMe)
class AboutMeAdmin(admin.ModelAdmin):
    list_display = ["preview", "about_text"]
    readonly_fields = ["preview"]
    exclude = ("about_image",)
    change_form_template = "admin/common/aboutme/change_form.html"

    def has_add_permission(self, request):
        """Impede que o botão 'Add About Me' seja mostrado se já houver um registro."""
        if AboutMe.objects.exists():
            return False
        return True

    def save_model(self, request, obj, form, change):
        if not change and AboutMe.objects.exists():
            self.message_user(
                request,
                "Só é permitido um único registro de 'Sobre Mim'.",
                level=messages.ERROR
            )
        else:
            super().save_model(request, obj, form, change)
        
    def preview(self, obj):
        """Exibe a imagem base64 no Django Admin."""
        if obj.about_image:
            return format_html('<img src="{}" width="200"/>', obj.about_image)
        return "(Sem imagem)"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "remove_image/<int:pk>/",
                self.admin_site.admin_view(self.remove_image),
                name="remove_about_image",
            ),
        ]
        return custom_urls + urls

    def remove_image(self, request, pk):
        """Remove a imagem e redireciona para a página de edição"""
        obj = AboutMe.objects.get(pk=pk)
        obj.about_image = ""
        obj.save()
        self.message_user(request, "A imagem foi removida com sucesso!", level=messages.SUCCESS)
        return redirect(f"/admin/common/aboutme/{pk}/change/")

admin.site.register(ParametroSistema)
