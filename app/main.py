from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI()

class UsuarioEntrada(BaseModel):
    nome: str
    email: EmailStr
    idade: int

usuarios = []

@app.get("/")
def home():
    return {"message": "Microservico de usuários funcionando"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/users", status_code=201)
def criar_usuario(usuario: UsuarioEntrada):
    
    novo_usuario = {
        "id": len(usuarios) + 1,
        "nome": usuario.nome,
        "email": usuario.email,
        "idade": usuario.idade
    }
    
    usuarios.append(novo_usuario)
    return novo_usuario

@app.get("/users")
def listar_usuarios():
    return usuarios

@app.get("/users/{usuario_id}")
def buscar_usuario(usuario_id: int):
    
    for usuario in usuarios:
        if usuario["id"] == usuario_id:
            return usuario
    
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

    