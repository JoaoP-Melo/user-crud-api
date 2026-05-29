# API de Usuários com FastAPI

API REST desenvolvida com Python utilizando o framework FastAPI e SQLAlchemy para integração com o banco de dados PostgreSQL. A aplicação disponibiliza operações completas de CRUD, permitindo cadastrar, listar, atualizar e remover usuários do banco de dados. Cada usuário possui os campos id, username, age, email e password. O sistema conta com autenticação baseada em JWT (JSON Web Token), onde determinadas rotas são protegidas e só podem ser acessadas após a autenticação de um usuário já cadastrado. O token gerado deve ser enviado no header das requisições para autorização de acesso. Todas as funcionalidades podem ser testadas diretamente pela documentação automática interativa fornecida pelo FastAPI. A aplicação também possui testes automatizados desenvolvidos com Pytest para validar o comportamento e o retorno correto das rotas. Além disso, toda a estrutura do projeto foi preparada para execução em containers Docker, facilitando a padronização do ambiente, deploy e escalabilidade da aplicação.


## Funcionalidades

* Criar usuário
* Listar usuários
* Buscar usuário por ID
* Atualizar usuário
* Deletar usuário
* Criar acesso por token

## Tecnologias

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* Pytest
* Hash de senha
* JWT  
* Docker

## Estrutura do projeto

src/  
  ├── app.py  
  ├── database.py  
  ├── models.py  
  ├── schemas.py  
  ├── security.py  
test/   
  ├── conftest.py   
  ├── test_app.py  

## Como Executar o Projeto

### Pré-requisitos

Configurar as Variáveis de Ambiente:

Crie um arquivo .env na raiz do projeto utilizando o arquivo .env.example como base e preencha as variáveis com os valores desejados.  
O campo DATABASE_URL utiliza o endereço do serviço do banco de dados que será executado dentro do container Docker.  

Antes de começar, você precisa ter instalado:

* Docker
* Docker Compose

### 1. Clone o repositório

git clone https://github.com/JoaoP-Melo/user-crud-api

### 2. Acesse a pasta do projeto

cd user-crud-api

### 3. Execute os comandos no terminal
Montar e subir os containers:
* docker compose up --build

Após iniciar os containers, acesse o navegador a documentação automática do FastAPI estará disponível em:
* Swagger UI
  `http://127.0.0.1:8000/docs`

* ReDoc
  `http://127.0.0.1:8000/redoc`
 
Acessar o terminal do container da API:
* docker compose exec api  bash  

Executar os testes automatizados:  
* pytest -v  

Parar e remover os containers:
* docker compose down

## Objetivo

* Praticar construção de APIs REST
* Trabalhar com banco de dados
* Organizar projetos back-end
* Implementar autenticação e segurança
* Explorar containers e conceitos relacionados à infraestrutura e cloud

## Autor

João Pedro, projeto desenvolvido para fins de estudo em back-end.