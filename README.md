# API de Usuários com FastAPI

API REST desenvolvida com FastAPI para praticar conceitos fundamentais de back-end: CRUD, integração com banco de dados e organização de código.

## Funcionalidades

* Criar usuário
* Listar usuários
* Buscar usuário por ID
* Atualizar usuário
* Deletar usuário

## Tecnologias

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* Pytest
* Uvicorn

## Estrutura do projeto

src/  
  ├── app.py  
  ├── models.py  
  ├── schemas.py  
  ├── database.py   
test/  
  ├── conftest.py   
  ├── test_app.py  

## Como executar

### 1. Clone o repositório

git clone https://github.com/JoaoP-Melo/user-crud-api
cd user-crud-api

### 2. Crie e ative o ambiente virtual

#### Windows
python -m venv venv
venv\Scripts\activate

#### Linux/Mac
python3 -m venv venv
source venv/bin/activate

### 3. Instale as dependências

pip install -r requirements.txt

### 4. Execute a aplicação

uvicorn src.main:app --reload

## Documentação automática

Após iniciar o servidor:

* Swagger: http://127.0.0.1:8000/docs

## Exemplo de JSON

{
  "username": "joao",
  "age": "19",
  "email": "joao@email.com",
}

## Objetivo

* Praticar construção de APIs REST
* Trabalhar com banco de dados
* Organizar projetos back-end
* Preparar base para autenticação e segurança

## Melhorias futuras

* Autenticação com JWT
* Hash de senha
* Uso de PostgreSQL
* Dockerização

## Autor

João Pedro, projeto desenvolvido para fins de estudo em back-end.