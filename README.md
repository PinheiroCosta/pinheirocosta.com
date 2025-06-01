# Pinheirocosta.com

[![License: MIT](https://img.shields.io/github/license/vintasoftware/django-react-boilerplate.svg)](LICENSE.txt)

## Bem-vindo ao meu site pessoal
Este é um espaço dedicado ao meu universo como desenvolvedor de software. Aqui compartilho ferramentas úteis que crio, além de dividir minhas experiências e aprendizados através do blog.
Se você busca conteúdos práticos, insights reais e um olhar sincero sobre desenvolvimento, está no lugar certo.
Sinta-se à vontade para explorar, usar as ferramentas e acompanhar os posts. Feedbacks e colaborações são sempre bem-vindos!

## Origem do Projeto
Este site pessoal foi desenvolvido a partir do [django-react-boilerplate da Vinta](https://github.com/vintasoftware/django-react-boilerplate), um boilerplate sólido que integra Django e React com Webpack para acelerar o desenvolvimento. A partir dessa base, customizei e ampliei para abrigar minhas ferramentas, blog e outras funcionalidades.

## Como Rodar Localmente
Se você quiser testar o projeto localmente, siga os passos básicos abaixo:

1. Clone este repositório
2. Configure as variáveis de ambiente (exemplo: DJANGO_SETTINGS_MODULE, banco de dados, etc)
3. Realize o Setup inicial `make docker_setup`
4. Rode as migrations: `make docker_migrate`
5. Rode em ambiente de desenvolvimento: `make docker_dev_up`

## Tecnologias Utilizadas
- Backend: Django 4+, Django REST Framework, Python 3.12, Poetry
- Frontend: React 18, Webpack, TypeScript, React-Bootstrap
- Infra: Nginx, Gunicorn, Docker, PostgreSQL
- Outros: OpenAPI, Celery, Redis (em microserviços)

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

## Exemplo de Variaveis de ambiente para desenvolvimento:
```bash
ENVIRONMENT=dev
DJANGO_SETTINGS_MODULE=devsite.settings.local
CELERY_BROKER_URL=amqp://broker:5672//
REDIS_URL=redis://result:6379
POSTGRES_USER=devsite
POSTGRES_PASSWORD=devsitepass
POSTGRES_DB=devsite
DATABASE_URL=postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
SECRET_KEY=RaCLW_Qd6YYyEqDPFkLxmMULK-0zVnaOYrN8UPHY0sebnm36C1cSwI4pKCKjHRk7C-a
ALLOWED_HOSTS=localhost, 127.0.0.1
SENDGRID_USERNAME=
SENDGRID_PASSWORD=
```
