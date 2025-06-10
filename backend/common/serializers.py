from rest_framework import serializers
from .models import ParametroSistema, AboutMe, ProfessionalContactMessage
from common.validators.sanitize import (
    validate_no_html, 
    sanitize_html, 
    validate_no_sql_injection,
)


class ProfessionalContactMessageCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    subject = serializers.ChoiceField(choices=ProfessionalContactMessage.SUBJECT_CHOICES)
    message = serializers.CharField()

    def validate_name(self, value):
        value = validate_no_html("name", value)
        value = validate_no_sql_injection("name", value)
        return value

    def validate_message(self, value):
        value = validate_no_html("message", value)
        value = validate_no_sql_injection("message", value)
        return value

    def create(self, validated_data):
        validated_data["message"] = sanitize_html(validated_data["message"])
        return super().create(validated_data)

    class Meta:
        model = ProfessionalContactMessage
        fields = ['name', 'email', 'subject', 'message', 'utm_source', 'utm_medium', 'utm_campaign']

    
class ProfessionalContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalContactMessage
        fields = '__all__'
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


