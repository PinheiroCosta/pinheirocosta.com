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

    def valdade_about_image(self, value):
        """
        Verifica se a string recebida é um base64 válido.
        """

        try:
            if value:
                base64.b64decode(value)
        except Exception:
            raise serializers.ValidationError("Imagem inválida! Certifique-se de enviar um base64 válido.")
        return value
