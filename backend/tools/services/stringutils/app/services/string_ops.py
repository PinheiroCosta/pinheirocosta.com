"""
Módulo de operações de string para a API StringUtils.

Contém funções utilitárias para manipulação de texto, incluindo
conversões de case, contagem de caracteres, geração de UUID, etc.
"""

import re
import unicodedata
import uuid


def count_characters(text: str, count_spaces=True, count_special=True, count_escaped=True):
    """
    Conta caracteres, palavras, vogais, consoantes e números em uma string.

    Args:
        text (str): Texto de entrada.
        count_spaces (bool): Incluir espaços na contagem de caracteres.
        count_special (bool): Incluir caracteres especiais.
        count_escaped (bool): Incluir caracteres de escape.

    Returns:
        dict: Contagem de caracteres, palavras, vogais, consoantes e números.
    """

    ESCAPED_CHARS = {"\n", "\t", "\r", "\b", "\f", "\\", "\v"}
    filtered = []
    vowel_count = 0
    consonant_count = 0

    for ch in text:
        if ch in ESCAPED_CHARS:
            if count_escaped:
                filtered.append(ch)
            continue

        if ch.isspace():
            if count_spaces:
                filtered.append(ch)
            continue

        if not ch.isalnum():
            if count_special:
                filtered.append(ch)
            continue

        filtered.append(ch)

        if ch.lower() in "aeiou":
            vowel_count += 1
        elif ch.isalpha():
            consonant_count += 1 

    return {
        "characters": len(filtered),
        "vowels": vowel_count,
        "consonants": consonant_count,
        "words": len("".join(filtered).split()),
    }

def reverse(text: str) -> str:
    """
    Inverte a string fornecida.

    Args:
        text (str): Texto de entrada.

    Returns:
        str: Texto invertido.
    """
    return text[::-1]

def uppercase(text: str) -> str:
    """
    Converte a string para letras maiúsculas.

    Args:
        text (str): Texto de entrada.

    Returns:
        str: Texto em maiúsculas.
    """
    return text.upper()

def lowercase(text: str) -> str:
    """
    Converte a string para letras minúsculas.

    Args:
        text (str): Texto de entrada.

    Returns:
        str: Texto em minúsculas.
    """
    return text.lower()

def slugify(text: str) -> str:
    """
    Converte a string em um slug URL-friendly.

    Remove acentuação, caracteres especiais e substitui espaços por hífens.

    Args:
        text (str): Texto de entrada.

    Returns:
        str: Slug gerado.
    """
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^a-zA-Z0-9]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-').lower()

def generate_uuid() -> str:
    """
    Gera um UUID v4.

    Returns:
        str: UUID gerado.
    """
    return str(uuid.uuid4())

def ascii_converter(text: str) -> str:
    """
    Remove acentuação e caracteres especiais, convertendo para ASCII puro.

    Args:
        text (str): Texto de entrada.

    Returns:
        str: Texto convertido para ASCII.
    """
    text = unicodedata.normalize('NFKD', text)
    return text.encode('ascii', 'ignore').decode('ascii')

def is_palindrome(text: str) -> bool:
    """
    Verifica se a string é um palíndromo.

    Ignora espaços, pontuação e diferença entre maiúsculas/minúsculas.

    Args:
        text (str): Texto de entrada.

    Returns:
        bool: True se for palíndromo, False caso contrário.
    """
    normalized = re.sub(r'[^a-zA-Z0-9]', '', text).lower()
    return normalized == normalized[::-1]
