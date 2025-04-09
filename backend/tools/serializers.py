from rest_framework import serializers
from .models import Tool, ToolField, ToolFieldOption


class ToolFieldOptionSerializer(serializers.ModelSerializer):
    """ Serializa as opções de um campo (usado para selects). """
    class Meta:
        model = ToolFieldOption
        fields = ["value", "label"]

class ToolFieldSerializer(serializers.ModelSerializer):
    """ Serializa os campos de entrada e saída de uma ferramenta. """
    options = ToolFieldOptionSerializer(many=True, read_only=True)

    class Meta:
        model = ToolField
        fields = ["name", "label", "data_type", "widget_type", "required", "options"]

class ToolSerializer(serializers.ModelSerializer):
    """ Serializa a ferramenta, separando inputs e outputs. """
    inputs = serializers.SerializerMethodField()
    outputs = serializers.SerializerMethodField()

    class Meta:
        model = Tool
        fields = ["id", "name", "slug", "description", "category", "active", "inputs", "outputs"]

    def get_inputs(self, obj):
        """ Retorna apenas os campos de entrada. """
        inputs = obj.fields.filter(io_type="input")
        return ToolFieldSerializer(inputs, many=True).data

    def get_outputs(self, obj):
        """ Retorna apenas os campos de saída. """
        outputs = obj.fields.filter(io_type="output")
        return ToolFieldSerializer(outputs, many=True).data

