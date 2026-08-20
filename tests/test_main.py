import pytest

from fastapi.testclient import TestClient

from app.main import app, usuarios
from app.auth import validar_token


client = TestClient(app)


def token_com_todas_permissoes():
    return {
        "permissions": [
            "read:users",
            "create:users"
        ]
    }


def token_apenas_leitura():
    return {
        "permissions": [
            "read:users"
        ]
    }


@pytest.fixture(autouse=True)
def limpar_estado():
    usuarios.clear()
    app.dependency_overrides = {}

    yield

    usuarios.clear()
    app.dependency_overrides = {}


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_acesso_sem_token():
    response = client.get("/users")

    assert response.status_code == 401


def test_criar_usuario():
    app.dependency_overrides[validar_token] = token_com_todas_permissoes

    response = client.post(
        "/users",
        json={
            "nome": "Alex",
            "email": "alex@email.com",
            "idade": 30
        }
    )

    assert response.status_code == 201

    dados = response.json()

    assert dados["id"] == 1
    assert dados["nome"] == "Alex"
    assert dados["email"] == "alex@email.com"
    assert dados["idade"] == 30


def test_email_invalido():
    app.dependency_overrides[validar_token] = token_com_todas_permissoes

    response = client.post(
        "/users",
        json={
            "nome": "Alex",
            "email": "email-invalido",
            "idade": 30
        }
    )

    assert response.status_code == 422


def test_buscar_usuario():
    app.dependency_overrides[validar_token] = token_com_todas_permissoes

    client.post(
        "/users",
        json={
            "nome": "Maria",
            "email": "maria@email.com",
            "idade": 28
        }
    )

    response = client.get("/users/1")

    assert response.status_code == 200

    dados = response.json()

    assert dados["id"] == 1
    assert dados["nome"] == "Maria"


def test_usuario_nao_encontrado():
    app.dependency_overrides[validar_token] = token_com_todas_permissoes

    response = client.get("/users/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Usuário não encontrado"
    }


def test_leitura_com_permissao():
    app.dependency_overrides[validar_token] = token_apenas_leitura

    response = client.get("/users")

    assert response.status_code == 200


def test_criacao_sem_permissao():
    app.dependency_overrides[validar_token] = token_apenas_leitura

    response = client.post(
        "/users",
        json={
            "nome": "Alex",
            "email": "alex@email.com",
            "idade": 30
        }
    )

    assert response.status_code == 403
    assert response.json() == {
        "detail": "Permissão insuficiente"
    }