# StringUtils API

Pequeno microsserviço FastAPI para manipulação de strings.  
Faz parte do meu portfólio de projetos Python.

## Endpoints Disponíveis

- `/api/v1/stringutils/reverse`
- `/api/v1/stringutils/uppercase`
- `/api/v1/stringutils/lowercase`
- `/api/v1/stringutils/slugify`
- `/api/v1/stringutils/uuid`
- `/api/v1/stringutils/ascii`
- `/api/v1/stringutils/palindrome`
- `/api/v1/stringutils/charcount`

## Como rodar localmente

```bash
# Build Docker
docker build -t stringutils .

# Run container
docker run -p 5010:5010 stringutils
```
ou usando Uvicorn diretamente:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 5010
```

## Requisitos de desenvolvimento
- Python 3.12+
- FastAPI
- Uvicorn
- Pydantic

