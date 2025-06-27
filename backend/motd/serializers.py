from rest_framework import serializers
from .models import MOTD, MOTDConfig


class MOTDSerializer(serializers.ModelSerializer):
    class Meta:
        model = MOTD
        fields = "__all__"


class MOTDConfigSerializer(serializers.ModelSerializer):
    message_override_text = serializers.SerializerMethodField()

    class Meta:
        model = MOTDConfig
        fields = ["id", "message_override", "message_override_text"]

    def get_message_override_text(self, obj):
        return obj.message_override.text if obj.message_override else None
