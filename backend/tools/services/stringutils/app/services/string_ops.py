import uuid
import re
import unicodedata

def reverse(text: str) -> str:
    return text[::-1]

def uppercase(text: str) -> str:
    return text.upper()

def lowercase(text: str) -> str:
    return text.lower()

def slugify(text: str) -> str:
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^a-zA-Z0-9]+', '-', text)
    return text.strip('-').lower()

def generate_uuid() -> str:
    return str(uuid.uuid4())

