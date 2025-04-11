import html
from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from .models import MOTD, MOTDConfig
from .utils import is_rich_text_enabled
from django.utils.html import strip_tags


if is_rich_text_enabled():
    from tinymce.widgets import TinyMCE


class MOTDAdminForm(forms.ModelForm):
    class Meta:
        model = MOTD
        fields = '__all__'
        widgets = {
            'text': TinyMCE(attrs={'cols': 80, 'rows': 10}) if is_rich_text_enabled() else forms.Textarea(),
        }


@admin.register(MOTD)
class MOTDAdmin(admin.ModelAdmin):
    form = MOTDAdminForm
    list_display = ('short_text', 'active', 'created_at')
    list_filter = ('active',)
    readonly_fields = ('preview',)

    def preview(self, obj):
        if not obj.text:
            return "Mensagem vazia."
        return mark_safe(f'<div style="border:1px solid #ccc;padding:10px;">{obj.text}</div>')
    preview.short_description = "Prévia da mensagem"
    
    def short_text(self, obj):
        raw = strip_tags(obj.text or "")
        clean = html.unescape(raw)
        return (clean[:80] + '...') if len(clean) > 80 else clean
    short_text.short_description = "Mensagem (resumo)"


@admin.register(MOTDConfig)
class MOTDConfigAdmin(admin.ModelAdmin):
    list_display = ('message_override', 'updated_at')

