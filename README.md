# Microsserviço de Usuários

Projeto desenvolvido como exercício prático de **Arquitetura de Microsserviços**, com foco na criação de um microsserviço REST, segurança em camadas, testes automatizados e integração contínua.

O microsserviço é responsável pelo **cadastro e consulta de usuários** e utiliza o **Auth0** para autenticação e autorização através de tokens JWT.

## Objetivo

O objetivo deste projeto é aplicar, de forma prática, conceitos relacionados a:

- Arquitetura de microsserviços;
- Desenvolvimento de APIs REST;
- Validação de dados de entrada;
- Tratamento de erros HTTP;
- Autenticação;
- Autorização baseada em permissões;
- Tokens JWT;
- Defesa em profundidade;
- Testes automatizados;
- Integração Contínua (CI).

## Tecnologias utilizadas

- **Python 3.11** — linguagem utilizada no desenvolvimento;
- **FastAPI** — framework utilizado para criação da API;
- **Pydantic** — modelagem e validação dos dados;
- **Uvicorn** — servidor ASGI utilizado para executar a aplicação;
- **Auth0** — serviço utilizado para autenticação e autorização;
- **JWT / PyJWT** — validação dos Access Tokens;
- **python-dotenv** — carregamento das configurações locais;
- **Pytest** — execução dos testes automatizados;
- **HTTPX / TestClient** — realização de requisições durante os testes;
- **GitHub Actions** — execução automática dos testes através de CI.

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
│   ├── auth.py
│   └── main.py
│
├── tests/
│   ├── __init__.py
│   └── test_main.py
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

### `app/main.py`

Contém a aplicação FastAPI, os modelos de dados e os endpoints do microsserviço.

### `app/auth.py`

Contém a lógica responsável pela segurança da API, incluindo:

- recebimento do Bearer Token;
- validação do JWT;
- validação do `issuer`;
- validação do `audience`;
- obtenção da chave pública através do JWKS do Auth0;
- leitura das permissões do token;
- autorização de acesso aos endpoints.

### `tests/test_main.py`

Contém os testes automatizados da API utilizando Pytest e TestClient.

Os testes também utilizam substituição de dependências do FastAPI para testar autenticação e autorização sem depender de tokens reais do Auth0.

### `.github/workflows/tests.yml`

Define o workflow do GitHub Actions responsável por instalar as dependências e executar automaticamente os testes.

### `.env`

Contém configurações locais necessárias para integração com o Auth0.

Esse arquivo está incluído no `.gitignore` e **não deve ser enviado ao repositório**.

---

## Funcionalidades

O microsserviço permite:

- verificar se a aplicação está funcionando;
- verificar a disponibilidade através de health check;
- cadastrar usuários;
- listar usuários cadastrados;
- buscar um usuário pelo ID;
- validar os dados enviados para cadastro;
- autenticar requisições utilizando JWT;
- controlar acesso através de permissões;
- retornar erros HTTP adequados;
- executar testes automatizados;
- executar os testes automaticamente através do GitHub Actions.

---

## Endpoints

### Verificar a aplicação

```http
GET /
```

Endpoint público que retorna uma mensagem informando que o microsserviço está funcionando.

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

Endpoint público utilizado para verificar se o serviço está disponível.

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

Requer:

```text
Autenticação: Bearer Token
Permissão: read:users
```

### Buscar usuário

```http
GET /users/{usuario_id}
```

Busca um usuário através do seu ID.

Exemplo:

```http
GET /users/1
```

Requer:

```text
Autenticação: Bearer Token
Permissão: read:users
```

Caso o usuário não exista:

```http
404 Not Found
```

Resposta:

```json
{
  "detail": "Usuário não encontrado"
}
```

### Cadastrar usuário

```http
POST /users
```

Requer:

```text
Autenticação: Bearer Token
Permissão: create:users
```

Exemplo de corpo da requisição:

```json
{
  "nome": "Alex",
  "email": "alex@email.com",
  "idade": 30
}
```

Quando o cadastro é realizado com sucesso:

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

- `nome`: texto;
- `email`: endereço de e-mail válido;
- `idade`: número inteiro.

Por exemplo:

```json
{
  "nome": "Alex",
  "email": "email-invalido",
  "idade": 30
}
```

A requisição é rejeitada pela validação da aplicação.

Uma entrada inválida pode resultar em:

```http
422 Unprocessable Entity
```

Essa validação representa uma das camadas de segurança do microsserviço.

---

# Segurança

A API utiliza diferentes mecanismos de segurança seguindo o conceito de **Defesa em Profundidade**.

A ideia é não depender de apenas uma proteção.

O fluxo implementado é:

```text
Requisição
    │
    ▼
Bearer Token
    │
    ▼
Validação do JWT
    │
    ├── Assinatura
    ├── Issuer
    ├── Audience
    └── Validade
    │
    ▼
Token válido?
   │
   ├── NÃO → 401 Unauthorized
   │
   └── SIM
        │
        ▼
Verificação de permissão
        │
        ├── read:users
        └── create:users
        │
        ▼
Possui a permissão?
   │
   ├── NÃO → 403 Forbidden
   │
   └── SIM
        │
        ▼
Validação dos dados
        │
        ▼
Execução do endpoint
```

## Autenticação com Auth0

O **Auth0** é utilizado como serviço externo de identidade.

O microsserviço não implementa diretamente mecanismos de armazenamento e gerenciamento de senhas.

O Auth0 emite um **Access Token JWT**, que é enviado para a API através do cabeçalho:

```http
Authorization: Bearer <ACCESS_TOKEN>
```

O FastAPI recebe esse token e realiza sua validação antes de permitir acesso aos endpoints protegidos.

## Validação do JWT

A API verifica informações importantes do token, incluindo:

- assinatura digital;
- emissor (`issuer`);
- destinatário (`audience`);
- validade do token.

As chaves públicas utilizadas para validar a assinatura são obtidas através do endpoint JWKS disponibilizado pelo Auth0.

Um token inválido ou ausente resulta em:

```http
401 Unauthorized
```

## Autorização

Além de possuir um token válido, algumas operações exigem permissões específicas.

Foram configuradas duas permissões:

```text
read:users
create:users
```

A distribuição é:

| Endpoint | Permissão |
|---|---|
| `GET /users` | `read:users` |
| `GET /users/{id}` | `read:users` |
| `POST /users` | `create:users` |

Por exemplo, um token contendo apenas:

```json
{
  "permissions": [
    "read:users"
  ]
}
```

pode consultar usuários, mas não pode cadastrar um novo usuário.

Uma tentativa de executar uma operação sem a permissão necessária resulta em:

```http
403 Forbidden
```

Resposta:

```json
{
  "detail": "Permissão insuficiente"
}
```

### Diferença entre 401 e 403

```text
401 Unauthorized
→ autenticação ausente ou inválida

403 Forbidden
→ autenticado, mas sem permissão para realizar a operação
```

---

# Configuração do Auth0

Para executar os endpoints protegidos é necessário configurar uma API no Auth0.

O projeto utiliza duas variáveis de ambiente:

```env
AUTH0_DOMAIN=SEU_DOMINIO.auth0.com
AUTH0_AUDIENCE=https://microservico-usuarios-api
```

O valor de `AUTH0_AUDIENCE` deve ser exatamente igual ao **Identifier** configurado para a API no Auth0.

O arquivo deve ser criado na raiz do projeto:

```text
microservico-usuarios/
│
├── .env
├── app/
├── tests/
└── ...
```

O `.env` não deve ser enviado ao GitHub.

No Auth0 também devem existir as permissões:

```text
read:users
create:users
```

A aplicação utilizada para acessar a API deve receber as permissões necessárias através do **Application Access / Client Access**.

---

# Como executar o projeto

## 1. Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
```

Entre na pasta:

```bash
cd microservico-usuarios
```

## 2. Criar o ambiente virtual

No Windows:

```powershell
python -m venv venv
```

## 3. Ativar o ambiente virtual

No PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

## 4. Instalar as dependências

```powershell
python -m pip install -r requirements.txt
```

## 5. Configurar as variáveis de ambiente

Crie:

```text
.env
```

na raiz do projeto.

Exemplo:

```env
AUTH0_DOMAIN=SEU_DOMINIO.auth0.com
AUTH0_AUDIENCE=https://microservico-usuarios-api
```

## 6. Executar a aplicação

```powershell
python -m uvicorn app.main:app --reload
```

A aplicação ficará disponível em:

```text
http://127.0.0.1:8000
```

---

# Documentação da API

O FastAPI gera automaticamente uma interface Swagger para visualizar e testar os endpoints.

Com a aplicação executando, acesse:

```text
http://127.0.0.1:8000/docs
```

Para testar endpoints protegidos:

```text
Auth0
  ↓
obter Access Token
  ↓
Swagger /docs
  ↓
Authorize
  ↓
colar o Access Token
  ↓
executar endpoint
```

O token deve ser inserido no campo de autorização do Swagger.

---

# Testes automatizados

Os testes foram implementados utilizando **Pytest**.

Para executá-los:

```powershell
python -m pytest -v
```

A aplicação não precisa estar sendo executada pelo Uvicorn durante os testes, pois o `TestClient` carrega a aplicação FastAPI diretamente.

Atualmente são executados **8 testes automatizados**, cobrindo:

- funcionamento do `/health`;
- tentativa de acesso sem token;
- cadastro de usuário autorizado;
- validação de e-mail inválido;
- busca de usuário existente;
- retorno `404` para usuário inexistente;
- leitura com a permissão `read:users`;
- tentativa de criação sem `create:users`, retornando `403`.

## Testes de autenticação e autorização

Os testes não utilizam um Access Token real do Auth0.

O FastAPI permite substituir dependências durante os testes através de:

```python
app.dependency_overrides
```

Assim, os testes conseguem simular diferentes situações.

Por exemplo:

```text
Token simulado
├── read:users
└── create:users
```

permite testar operações de leitura e criação.

Enquanto:

```text
Token simulado
└── read:users
```

permite testar que a leitura funciona, mas a criação retorna:

```http
403 Forbidden
```

Isso mantém os testes independentes do Auth0 e de uma conexão externa.

---

# Integração Contínua — CI

O projeto utiliza **GitHub Actions** para executar automaticamente os testes.

O workflow está definido em:

```text
.github/workflows/tests.yml
```

Quando ocorre um `push` ou `pull request`, o processo é:

```text
Código enviado ao GitHub
        │
        ▼
GitHub Actions
        │
        ▼
Configura o ambiente Python
        │
        ▼
Instala as dependências
        │
        ▼
Executa Pytest
        │
        ▼
8 testes automatizados
        │
        ├── falha → workflow vermelho
        │
        └── sucesso → workflow verde
```

Os testes de autenticação e autorização utilizam dependências simuladas, portanto o workflow não precisa armazenar um Access Token real do Auth0.

---

# Armazenamento dos dados

Nesta versão, os usuários são armazenados em uma lista Python em memória.

Isso significa que os dados são perdidos quando a aplicação é reiniciada.

Essa abordagem foi escolhida para manter o foco do exercício em:

- microsserviços;
- validação;
- segurança;
- testes;
- automação.

Em uma aplicação real, essa camada poderia ser substituída por um banco de dados.

---

# Arquitetura simplificada

```text
                         Auth0
                           │
                           │ Access Token JWT
                           ▼
Cliente ───────────────► FastAPI
                           │
                           ├── Validação JWT
                           │      ├── assinatura
                           │      ├── issuer
                           │      └── audience
                           │
                           ├── Autorização
                           │      ├── read:users
                           │      └── create:users
                           │
                           ├── Validação Pydantic
                           │
                           └── Endpoints
                                  │
                                  ├── GET  /health
                                  ├── GET  /users
                                  ├── GET  /users/{id}
                                  └── POST /users
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
                │
                ▼
             8 testes
```

---

# Status do projeto

- [x] Criação do microsserviço com FastAPI
- [x] Endpoint de health check
- [x] Cadastro de usuários
- [x] Listagem de usuários
- [x] Busca de usuário por ID
- [x] Validação de dados de entrada
- [x] Tratamento de usuário não encontrado
- [x] Testes automatizados com Pytest
- [x] Integração Contínua com GitHub Actions
- [x] Autenticação com Auth0
- [x] Utilização de Access Token JWT
- [x] Validação de JWT
- [x] Validação de `issuer`
- [x] Validação de `audience`
- [x] Proteção de endpoints
- [x] Autorização baseada em permissões
- [x] Permissão `read:users`
- [x] Permissão `create:users`
- [x] Tratamento de `401 Unauthorized`
- [x] Tratamento de `403 Forbidden`
- [x] Testes automatizados de autenticação
- [x] Testes automatizados de autorização
- [x] Execução dos testes de segurança no GitHub Actions

---

# Defesa em Profundidade

O exercício propõe a utilização de **Defesa em Profundidade**, ou seja, a aplicação de diferentes mecanismos de segurança em camadas.

Neste projeto foram aplicadas as seguintes camadas:

```text
Camada 1
Validação de entrada com Pydantic
        │
        ▼
Camada 2
Autenticação através do Auth0
        │
        ▼
Camada 3
Validação do Access Token JWT
        │
        ▼
Camada 4
Validação de issuer e audience
        │
        ▼
Camada 5
Autorização baseada em permissões
        │
        ▼
Camada 6
Testes automatizados de segurança
        │
        ▼
Camada 7
Execução automática dos testes através de CI
```

Assim, a segurança do microsserviço não depende de apenas um mecanismo.

---

# Contexto acadêmico

Este projeto foi desenvolvido como exercício prático para aplicar conceitos de **segurança e automação em uma arquitetura de microsserviços**.

O exercício propunha:

1. definir um microsserviço;
2. implementar automação;
3. aplicar ou projetar mecanismos de Defesa em Profundidade;
4. testar o microsserviço.

Neste projeto, esses pontos foram implementados através de:

```text
Microsserviço
→ FastAPI

Automação
→ GitHub Actions

Autenticação
→ Auth0

Token
→ JWT

Autorização
→ read:users / create:users

Validação
→ Pydantic

Testes
→ Pytest

Integração Contínua
→ GitHub Actions
```

Dessa forma, o projeto demonstra de maneira prática a aplicação de segurança, autorização, testes automatizados e integração contínua em um microsserviço.