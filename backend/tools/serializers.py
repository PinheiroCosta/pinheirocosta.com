from rest_framework import serializers
from .models import Tool, ToolField, ToolFieldOption
from drf_spectacular.utils import extend_schema_field


class ToolFieldOptionSerializer(serializers.ModelSerializer):
    """Serializa as opções de um campo (usado para selects)."""

    class Meta:
        model = ToolFieldOption
        fields = ["id", "value", "label"]


class ToolFieldSerializer(serializers.ModelSerializer):
    """Serializa os campos de entrada e saída de uma ferramenta."""

    options = ToolFieldOptionSerializer(many=True, read_only=True)

    class Meta:
        model = ToolField
        fields = [
            "id",
            "name",
            "label",
            "data_type",
            "widget_type",
            "default_value",
            "min_value",
            "max_value",
            "help_text",
            "required",
            "options",
        ]


class ToolSerializer(serializers.ModelSerializer):
    """Serializa a ferramenta, separando inputs e outputs."""

    inputs = serializers.SerializerMethodField()
    outputs = serializers.SerializerMethodField()

    class Meta:
        model = Tool
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "category",
            "active",
            "inputs",
            "outputs",
        ]

    @extend_schema_field(ToolFieldSerializer(many=True))
    def get_inputs(self, obj):
        """Retorna apenas os campos de entrada."""
        inputs = obj.fields.filter(io_type="input")
        return ToolFieldSerializer(inputs, many=True).data

    @extend_schema_field(ToolFieldSerializer(many=True))
    def get_outputs(self, obj):
        """Retorna apenas os campos de saída."""
        outputs = obj.fields.filter(io_type="output")
        return ToolFieldSerializer(outputs, many=True).data
