from rest_framework import serializers
from .models import ParametroSistema, AboutMe


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()


class ParametroSistemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParametroSistema
        fields = ['chave', 'valor']

class AboutMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutMe
        fields = ['about_image', 'about_text', 'social_links']


