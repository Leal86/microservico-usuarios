from fastapi.testclient import TestClient

from app.main import app, usuarios

client = TestClient(app)

def test_health():
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    

def test_criar_usuario():
    usuarios.clear()
    
    response = client.post(
        "/users", 
        json={
            "nome": "Alex", 
            "email":"alex@email.com", 
            "idade": 40
        }
    )
    
    assert response.status_code == 201
    
    dados = response.json()
    
    assert dados["id"] == 1
    assert dados["nome"] == "Alex"
    assert dados["email"] == "alex@email.com"
    assert dados["idade"] == 40
    

def test_email_invalido():
    usuarios. clear()
    
    response = client.post(
        "/users",
        json={
            "nome": "Alex",
            "email": "email-invalido",
            "idade": 40
        }
    )
    
    assert response.status_code == 422
    
def test_buscar_usuario():
    usuarios.clear()
    
    client.post(
        "/users",
        json={
            "nome": "Maria",
            "email": "maria@email.com",
            "idade": 70
        }
    )
    
    response = client.get("/users/1")
    
    assert response.status_code == 200
    
    dados = response.json()
    
    assert dados["id"] == 1
    assert dados["nome"] == "Maria"
    
    
def test_usuario_nao_encontrado():
    usuarios.clear()
    
    response = client.get("/users/666")
    
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Usuário não encontrado"
    }
