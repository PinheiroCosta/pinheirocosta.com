# Documentação de Arquitetura – Projeto Django/React 

## 1. Introdução
Este documento descreve a arquitetura do projeto, que nasceu a partir do boilerplate django-react-boilerplate. O objetivo é construir um site modular, onde cada recurso (por exemplo, o blog) pode ser ativado ou desativado via configuração armazenada no banco de dados. Inicialmente utilizado para um site pessoal, o projeto foi estruturado para possibilitar a comercialização futura, permitindo que os clientes ativem apenas os recursos que necessitarem.

## 2. Tecnologias Utilizadas
Backend: Django com Django REST Framework (DRF)
Frontend: React com TypeScript
Containerização: Docker (com arquivos separados para ambientes de desenvolvimento e produção)
Tarefas Assíncronas: Celery (integrado ao projeto pelo boilerplate)
Deploy: Implantação em VPS utilizando Docker (apesar do boilerplate sugerir o uso do Render)
Gerenciamento de Configurações: Variáveis de ambiente (.env) e futura implementação de parâmetros de sistema armazenados no banco de dados

## 3. Visão Geral da Arquitetura
A arquitetura do projeto está dividida basicamente em dois grandes blocos: o Frontend (React) e o Backend (Django + DRF). O backend é responsável por fornecer uma API REST para o frontend, gerenciar a lógica de negócio, tarefas assíncronas e comunicação com o banco de dados. A aplicação é containerizada com Docker para facilitar o deploy e a gestão dos diferentes ambientes (desenvolvimento e produção).

## 4. Diagrama
![romweb-diagram](https://github.com/user-attachments/assets/f1056a6e-2644-4ebc-a624-30c8a9cda825)

### Descrição do Diagrama:
**Usuário**:Interage com o site através do navegador.  
**Frontend (React)**: Implementado em TypeScript, consome a API fornecida pelo backend e gerencia a interface do usuário.  
**Backend (Django + DRF)**: Responsável por expor os endpoints da API, gerenciar a lógica dos apps (como o blog, usuários e recursos comuns) e interagir com o banco de dados. 
**Banco de Dados**: Armazena os dados do sistema, incluindo os registros dos apps e, futuramente, as configurações que definem a ativação dos recursos.  
**Celery**: Gerencia as tarefas assíncronas, mesmo que atualmente sua utilização seja mínima (herdada do boilerplate).  
**Tabela de Configurações**: Será utilizada para armazenar os parâmetros do sistema que definem se um recurso (como o blog) está ativo ou desativado.  
**Containerização (Docker)**: Todos os componentes principais estão containerizados, permitindo isolamento e facilidade de deploy.  
**VPS com Docker**: O deploy é realizado diretamente em uma VPS, utilizando Docker para orquestrar os serviços.  

## 5. Componentes Detalhados
### 5.1 Backend (Django)
**Apps:**  
    blog: Gerencia o conteúdo do blog.  
    common: Contém funcionalidades e utilitários comuns à aplicação.  
    users: Gerencia os usuários e autenticação para o painel de administração do blog.  
**API REST:**  
    Implementada com Django REST Framework, possibilitando a comunicação entre o frontend e o backend.  
**Tarefas Assíncronas:**  
    Integrado com Celery para execução de tarefas em background.  
**Configurações por Ambiente:**  
    Gerenciadas através de variáveis de ambiente (.env) e arquivos Docker específicos para cada ambiente.  
### 5.2 Frontend (React)  
**Estrutura:**
    Organizado em componentes, páginas, e utilitários.  
    Gerenciamento de estado e comunicação com a API foram herdados do boilerplate e poderão ser ajustados conforme necessário.  
**Comunicação com o Backend:**  
    Implementada por meio de uma camada de API no diretório frontend/js/api.  
### 5.3 Infraestrutura e Deploy  
**Containerização com Docker:**  
    Utiliza arquivos Dockerfile.dev e Dockerfile.prod para criar imagens específicas para cada ambiente.  
**Deploy em VPS:**  
    O deploy é feito diretamente em uma VPS utilizando Docker e Docker Compose, permitindo o isolamento dos serviços e escalabilidade.  
### 5.4 Gerenciamento de Recursos e Configurações  
**Feature Flags/Parâmetros de Sistema:**
    Planejamento de uma tabela no banco de dados para armazenar configurações que ativem ou desativem recursos (como o app do blog), evitando que o site quebre caso algum recurso seja desativado.  
### 5.5 Testes e CI/CD  
**Testes:**
    Estrutura já preparada (arquivos de teste no backend e configuração para testes no frontend com Jest), embora os testes automatizados ainda não estejam implementados.  
**CI/CD:**  
    Planejamento para a implementação de pipelines de integração e deploy contínuos para melhorar a qualidade do código e facilitar futuras atualizações.  

## 6. Considerações Finais
Escalabilidade e Modularidade:  
A arquitetura modular permite que recursos sejam adicionados ou removidos conforme a necessidade, facilitando a personalização do produto para futuros clientes.
  
Manutenção e Evolução:  
A documentação será mantida atualizada conforme o projeto evolui, servindo tanto para a equipe de desenvolvimento quanto para possíveis parceiros ou clientes.  

Próximos Passos:
Implementação do sistema de configurações/feature flags no banco de dados.
Desenvolvimento e integração dos testes automatizados.
Criação de pipelines de CI/CD para automação de testes e deploy.
