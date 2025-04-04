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
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=TOOL_CATEGORIES, default="utilitario")
    api_url = models.CharField(max_length=255)  # URL do microserviço da ferramenta
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ToolIOField(models.Model):
    IO_TYPES = [
        ("input", "Entrada"),
        ("output", "Saída"),
    ]
    FIELD_TYPES = [
        ("text", "Texto"),
        ("number", "Número"),
        ("checkbox", "Caixa de seleção"),
        ("select", "Seleção"),
    ]
    
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name="io_fields")
    name = models.CharField(max_length=255)     # Nome interno do campo (ex: 'cpf')
    label = models.CharField(max_length=255)    # Nome amigável (ex: "CPF do usuário")
    io_type = models.CharField(max_length=20, choices=IO_TYPES)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    required = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.tool.name} - {self.label} ({self.io_type})"

class ToolIOOption(models.Model):
    io_option = models.ForeignKey(ToolIOField, on_delete=models.CASCADE, related_name="options")
    value = models.CharField(max_length=255)
    label = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.io_option.label} -> {self.label}"
