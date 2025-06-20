"""
Schemas Pydantic usados como modelos de entrada para os endpoints da API StringUtils.
"""

from pydantic import BaseModel, Field

class TextInput(BaseModel):
    """
    Modelo de entrada com um único campo de texto.

    Atributos:
        text (str): Texto de entrada. Limite de 1 a 10.000 caracteres.
    """
    text: str = Field(..., min_length=1, max_length=10000)

class CharCountInput(BaseModel):
    """
    Modelo de entrada para o contador de caracteres.

    Atributos:
        text (str): Texto de entrada.
        count_spaces (bool): Incluir espaços na contagem.
        count_special (bool): Incluir caracteres especiais.
        count_escaped (bool): Incluir caracteres de escape.
    """
    text: str
    count_spaces: bool = True
    count_special: bool = True
    count_escaped: bool = True

