from rest_framework import serializers
from .utils.recaptcha import verify_recaptcha
from .models import ParametroSistema, AboutMe, ProfessionalContactMessage
from common.validators.sanitize import (
    validate_no_html, 
    sanitize_html, 
    validate_no_sql_injection,
)


class ProfessionalContactMessageCreateSerializer(serializers.ModelSerializer):
    """
    Serializer usado apenas na criação de mensagens de contato (POST).

    Inclui:
    - Validação de reCAPTCHA.
    - Campos UTM para rastreamento de origem
    - Validações de segurança contra HTML e SQL Injection

    Obs: O campo `recaptcha_token` não é persistido no banco.
    """

    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    subject = serializers.ChoiceField(choices=ProfessionalContactMessage.SUBJECT_CHOICES)
    message = serializers.CharField()
    utm_source = serializers.CharField(required=False, allow_blank=True)
    utm_medium = serializers.CharField(required=False, allow_blank=True)
    utm_campaign = serializers.CharField(required=False, allow_blank=True)
    recaptcha_token = serializers.CharField(write_only=True)

    class Meta:
        model = ProfessionalContactMessage
        fields = ['name', 'email', 'subject', 'message', 'utm_source', 'utm_medium', 'utm_campaign', 'recaptcha_token']

    def validate_name(self, value):
        value = validate_no_html("name", value)
        value = validate_no_sql_injection("name", value)
        return value

    def validate_message(self, value):
        value = validate_no_html("message", value)
        value = validate_no_sql_injection("message", value)
        return value

    def validate_recaptcha_token(self, value):
        if not verify_recaptcha(value, action="contact_form"):
            raise serializers.ValidationError("Falha na verificação reCAPTCHA")
        return value

    def create(self, validated_data):
        validated_data.pop("recaptcha_token", None)
        validated_data["message"] = sanitize_html(validated_data["message"])
        return super().create(validated_data)

    
class ProfessionalContactMessageSerializer(serializers.ModelSerializer):
    """
    Serializer de leitura para mensagens de contato.

    Usado apenas para visualização no painel admin
    Não expõe o campo recaptcha_token.
    """

    class Meta:
        model = ProfessionalContactMessage
        fields = ['name', 'email', 'subject', 'message', 'utm_source', 'utm_medium', 'utm_campaign']
        read_only_fields = ['id', 'created_at']


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()


class ParametroSistemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParametroSistema
        fields = ['chave', 'valor']

class AboutMeSerializer(serializers.ModelSerializer):
    social_links = serializers.DictField(
        child=serializers.CharField(), required=False
    )

    class Meta:
        model = AboutMe
        fields = ['about_image', 'about_text', 'social_links']


