# Microsserviço de Usuários

Projeto desenvolvido como exercício prático de **Arquitetura de Microsserviços**, com foco na criação de um microsserviço simples, validação de dados, testes automatizados e automação de integração contínua (CI).

## Objetivo

O objetivo deste projeto é aplicar conceitos relacionados a:

* Arquitetura de microsserviços;
* Desenvolvimento de APIs REST;
* Validação de dados de entrada;
* Tratamento de erros HTTP;
* Testes automatizados;
* Integração Contínua (CI);
* Segurança e defesa em profundidade.

O microsserviço implementado é responsável pelo **cadastro e consulta de usuários**.

## Tecnologias utilizadas

* **Python 3.11** — linguagem utilizada no desenvolvimento;
* **FastAPI** — framework utilizado para criação da API;
* **Pydantic** — utilizado para modelagem e validação dos dados;
* **Uvicorn** — servidor ASGI utilizado para executar a aplicação;
* **Pytest** — framework utilizado para os testes automatizados;
* **HTTPX / TestClient** — utilizado para realizar requisições durante os testes;
* **GitHub Actions** — utilizado para executar os testes automaticamente através de CI.

## Estrutura do projeto

```text
microservico-usuarios/
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── app/
│   ├── __init__.py
│   └── main.py
│
├── tests/
│   ├── __init__.py
│   └── test_main.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

### `app/main.py`

Contém a aplicação FastAPI, os modelos de dados e os endpoints do microsserviço.

### `tests/test_main.py`

Contém os testes automatizados da API utilizando Pytest e TestClient.

### `.github/workflows/tests.yml`

Define o workflow do GitHub Actions responsável por instalar as dependências e executar automaticamente os testes.

### `requirements.txt`

Contém as dependências Python necessárias para executar o projeto.

---

## Funcionalidades

Atualmente o microsserviço permite:

* Verificar se a aplicação está funcionando;
* Cadastrar usuários;
* Listar usuários cadastrados;
* Buscar um usuário pelo ID;
* Validar os dados enviados para cadastro;
* Retornar erros HTTP quando um recurso não é encontrado.

## Endpoints

### Verificar a aplicação

```http
GET /
```

Retorna uma mensagem informando que o microsserviço está funcionando.

Exemplo:

```json
{
  "message": "Microsserviço de usuários funcionando"
}
```

### Health Check

```http
GET /health
```

Permite verificar se o serviço está disponível.

Resposta:

```json
{
  "status": "ok"
}
```

### Listar usuários

```http
GET /users
```

Retorna a lista de usuários cadastrados.

### Buscar usuário

```http
GET /users/{usuario_id}
```

Busca um usuário através do seu ID.

Exemplo:

```http
GET /users/1
```

Caso o usuário não exista, a API retorna:

```http
404 Not Found
```

com:

```json
{
  "detail": "Usuário não encontrado"
}
```

### Cadastrar usuário

```http
POST /users
```

Exemplo de corpo da requisição:

```json
{
  "nome": "Alex",
  "email": "alex@email.com",
  "idade": 30
}
```

Quando o cadastro é realizado com sucesso, a API retorna:

```http
201 Created
```

Exemplo:

```json
{
  "id": 1,
  "nome": "Alex",
  "email": "alex@email.com",
  "idade": 30
}
```

---

## Validação de dados

O projeto utiliza o **Pydantic** para validar os dados recebidos pela API.

O modelo de entrada exige:

* `nome`: texto;
* `email`: endereço de e-mail válido;
* `idade`: número inteiro.

Por exemplo, uma requisição contendo um e-mail inválido:

```json
{
  "nome": "Alex",
  "email": "email-invalido",
  "idade": 30
}
```

é rejeitada automaticamente pela aplicação.

Essa validação representa uma das camadas de segurança utilizadas no projeto.

---

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
```

Entre na pasta:

```bash
cd microservico-usuarios
```

### 2. Criar o ambiente virtual

No Windows:

```powershell
python -m venv venv
```

### 3. Ativar o ambiente virtual

No PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Instalar as dependências

```powershell
python -m pip install -r requirements.txt
```

### 5. Executar a aplicação

```powershell
python -m uvicorn app.main:app --reload
```

A aplicação ficará disponível em:

```text
http://127.0.0.1:8000
```

## Documentação da API

O FastAPI gera automaticamente uma interface para visualizar e testar os endpoints.

Com a aplicação executando, acesse:

```text
http://127.0.0.1:8000/docs
```

Através dessa interface é possível executar requisições diretamente contra os endpoints disponíveis.

---

## Testes automatizados

Os testes foram implementados utilizando **Pytest**.

Para executá-los:

```powershell
python -m pytest -v
```

Os testes verificam:

* funcionamento do endpoint `/health`;
* cadastro de usuário;
* validação de e-mail inválido;
* busca de usuário existente;
* retorno `404` para usuário inexistente.

A aplicação não precisa estar sendo executada pelo Uvicorn durante os testes, pois o `TestClient` carrega a aplicação FastAPI diretamente.

---

## Integração Contínua — CI

O projeto utiliza **GitHub Actions** para executar automaticamente os testes.

O workflow está definido em:

```text
.github/workflows/tests.yml
```

Quando ocorre um `push` ou `pull request`, o GitHub Actions:

```text
Código enviado ao GitHub
        ↓
GitHub Actions é iniciado
        ↓
Configura o ambiente Python
        ↓
Instala as dependências
        ↓
Executa os testes com Pytest
        ↓
Informa sucesso ou falha
```

Isso permite detectar automaticamente alterações que causem falhas nos testes.

---

## Segurança

O projeto já implementa **validação de entrada** através do Pydantic.

A arquitetura de segurança será evoluída utilizando o conceito de **Defesa em Profundidade**, no qual diferentes mecanismos de proteção são aplicados em camadas.

As próximas etapas previstas incluem:

* autenticação através do Auth0;
* utilização de tokens JWT;
* proteção de endpoints;
* autorização de acesso a recursos;
* testes de acesso autenticado e não autenticado.

A utilização de um serviço especializado de identidade evita que o próprio microsserviço tenha que implementar diretamente mecanismos sensíveis de autenticação e armazenamento de senhas.

---

## Armazenamento dos dados

Nesta versão, os usuários são armazenados em uma lista Python em memória.

Isso significa que os dados são perdidos quando a aplicação é reiniciada.

Essa abordagem foi escolhida para manter o foco do exercício nos conceitos de microsserviços, segurança, testes e automação.

Em uma aplicação real, essa camada poderia ser substituída por um banco de dados.

---

## Fluxo atual

```text
Cliente
   │
   │ HTTP
   ▼
FastAPI
   │
   ├── Validação com Pydantic
   │
   ├── GET  /health
   │
   ├── GET  /users
   │
   ├── GET  /users/{id}
   │
   └── POST /users
   │
   ▼
Lista de usuários em memória
```

Durante o desenvolvimento:

```text
Desenvolvedor
      │
      │ git push
      ▼
GitHub
      │
      ▼
GitHub Actions
      │
      ├── Configura Python
      ├── Instala dependências
      └── Executa Pytest
```

## Status do projeto

* [x] Criação do microsserviço com FastAPI
* [x] Endpoint de health check
* [x] Cadastro de usuários
* [x] Listagem de usuários
* [x] Busca de usuário por ID
* [x] Validação de dados de entrada
* [x] Tratamento de usuário não encontrado
* [x] Testes automatizados com Pytest
* [x] Integração Contínua com GitHub Actions
* [ ] Autenticação com Auth0
* [ ] Validação de JWT
* [ ] Proteção de endpoints
* [ ] Testes de autenticação e autorização

## Contexto acadêmico

Este projeto foi desenvolvido como exercício prático para aplicar conceitos de **segurança e automação de implantação em uma arquitetura de microsserviços**.

O foco é demonstrar de forma prática como um serviço independente pode possuir validações, testes automatizados e um processo de integração contínua, além de permitir a evolução para mecanismos adicionais de segurança.
