from rest_framework import serializers
from .models import Tool, ToolIOField, ToolIOOption


class ToolIOOptionSerializer(serializers.ModelSerializer):
    """ Serializa as opções de um campo (usado para selects). """
    class Meta:
        model = ToolIOOption
        fields = ["value", "label"]

class ToolIOFieldSerializer(serializers.ModelSerializer):
    """ Serializa os campos de entrada e saída de uma ferramenta. """
    options = ToolIOOptionSerializer(many=True, read_only=True)

    class Meta:
        model = ToolIOField
        fields = ["name", "label", "field_type", "required", "options"]

class ToolSerializer(serializers.ModelSerializer):
    """ Serializa a ferramenta, separando inputs e outputs. """
    inputs = serializers.SerializerMethodField()
    outputs = serializers.SerializerMethodField()

    class Meta:
        model = Tool
        fields = ["id", "name", "slug", "description", "category", "api_url", "active", "inputs", "outputs"]

    def get_inputs(self, obj):
        """ Retorna apenas os campos de entrada. """
        inputs = obj.io_fields.filter(io_type="input")
        return ToolIOFieldSerializer(inputs, many=True).data

    def get_outputs(self, obj):
        """ Retorna apenas os campos de saída. """
        outputs = obj.io_fields.filter(io_type="output")
        return ToolIOFieldSerializer(outputs, many=True).data

