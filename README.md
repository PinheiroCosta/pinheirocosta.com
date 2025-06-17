# Pinheirocosta.com

[![License: MIT](https://img.shields.io/github/license/vintasoftware/django-react-boilerplate.svg)](LICENSE.txt)

## Sumário

- [Visão Geral](#visão-geral)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Origem do Projeto](#origem-do-projeto)
- [Como Rodar Localmente](#como-rodar-localmente)
- [Organização do Projeto](#organização-do-projeto)
- [Recursos em Destaque](#recursos-em-destaque)
- [Variáveis de ambiente para desenvolvimento](#variaveis-de-ambiente-para-desenvolvimento)
- [Como Contribuir](#como-contribuir)
  
## Visão Geral
Site pessoal com ferramentas, blog e microserviços, desenvolvido em Django + React com Webpack.

## Tecnologias Utilizadas
- Backend: Django 4+, Django REST Framework, Python 3.12, Poetry
- Frontend: React 18, Webpack, TypeScript, React-Bootstrap
- Infra: Nginx, Gunicorn, Docker, PostgreSQL
- Outros: OpenAPI, Celery, Redis (em microserviços)

## Origem do Projeto
Este site pessoal foi desenvolvido a partir do [django-react-boilerplate da Vinta](https://github.com/vintasoftware/django-react-boilerplate), um boilerplate sólido que integra Django e React com Webpack para acelerar o desenvolvimento. A partir dessa base, customizei e ampliei para abrigar minhas ferramentas, blog e outras funcionalidades.

## Como Rodar Localmente

```bash
git clone https://github.com/SeuUsuario/SeuRepo.git
cd SeuRepo
make docker_setup
make docker_migrate
make docker_dev_up
```


## Organização do Projeto
- backend/ – Projeto Django e apps (blog, ferramentas, motd, etc)
- backend/tools/ – Microserviços independentes (ex: Contador de caracteres, ficha de RPG etc)
- frontend/ – Aplicação React com Webpack

## Recursos em Destaque
- Sistema de ferramentas dinâmicas com forms auto-gerados a partir de schemas OpenAPI
- Microserviços integrados com Django como API Gateway
- Blog pessoal com Richtext e destaque de sintaxe
- Componente de "Mensagem do Dia" modularizado (MOTD)
- Interface minimalista e responsiva

## Variaveis de ambiente para desenvolvimento
```bash
ENVIRONMENT=dev
DJANGO_SETTINGS_MODULE=devsite.settings.local
CELERY_BROKER_URL=amqp://broker:5672//
REDIS_URL=redis://result:6379
POSTGRES_USER=<seu_user_aqui>
POSTGRES_PASSWORD=<seu_pass_aqui>
POSTGRES_DB=<seu_db_name_aqui>
DATABASE_URL=postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
SECRET_KEY=<sua_secret_key_aqui>
ALLOWED_HOSTS=localhost, 127.0.0.1
SENDGRID_USERNAME=
SENDGRID_PASSWORD=
```

## Como contribuir

Contribuições são bem-vindas via issues ou pull requests.  
Para sugestões, erros ou melhorias, abra uma issue para discutirmos antes de enviar código.
