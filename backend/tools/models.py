from django.db import models


class Tool(models.Model):
    TOOL_CATEGORIES = [
        ("conversao", "Conversão"),
        ("gerador", "Gerador"),
        ("validacao", "Validacão"),
        ("calculadora", "Calculadora"),
        ("simulador", "Simulador"),
        ("codificacao", "Codificação"),
        ("tradutor", "Tradutor"),
        ("utilitario", "Utilitário Geral"),
    ]
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=TOOL_CATEGORIES, default="utilitario")
    api_url = models.CharField(max_length=255)  # URL do microserviço da ferramenta
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ToolField(models.Model):
    IO_TYPES = [
        ("input", "Entrada"),
        ("output", "Saída"),
    ]

    DATA_TYPES = [
        ("string", "Texto simples"),
        ("int", "Número inteiro"),
        ("float", "Número decimal"),
        ("bool", "Booleano"),
        ("list", "Lista"),
        ("dict", "Dicionário"),
    ]

    WIDGET_TYPES = [
        ("text", "Área de texto"),
        ("input", "Campo de entrada"),
        ("checkbox", "Caixa de seleção"),
        ("select", "Dropdown"),
        ("radio", "Botões de opção"),
        ("date", "Formato de data dd/mm/aaaa"),
        ("", "Padrão automático"),
    ]
    
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name="fields")
    name = models.CharField(max_length=255)     # Nome interno do campo (ex: 'cpf')
    label = models.CharField(max_length=255)    # Nome amigável (ex: "CPF do usuário")
    io_type = models.CharField(max_length=20, choices=IO_TYPES)
    data_type = models.CharField(max_length=20, choices=DATA_TYPES)
    widget_type = models.CharField(max_length=50, choices=WIDGET_TYPES, blank=True, null=True, default="")
    required = models.BooleanField(default=False)
    help_text = models.CharField(max_length=255, blank=True)
    min_value = models.IntegerField(null=True, blank=True, default=0)
    max_value = models.IntegerField(null=True, blank=True)
    default_value = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["tool", "io_type", "id"]

    def __str__(self):
        return f"[{self.io_type.upper()}] {self.tool.slug}::{self.name} ({self.data_type})"


class ToolFieldOption(models.Model):
    field = models.ForeignKey(ToolField, on_delete=models.CASCADE, related_name="options")
    value = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.field.tool.slug}::{self.field.name} -> {self.label}"
