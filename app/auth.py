import os
from pathlib import Path

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWKClient


# Carrega o arquivo .env
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)

# Busca as variáveis de ambiente do arquivo .env
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE")

ALGORITHMS = ["RS256"]

security = HTTPBearer(auto_error=False) # Cria uma instância de HTTPBearer para autenticação via token

# Função para validar o token JWT
def validar_token(
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    if credentials is None:
        print("ERRO: Nenhum token Bearer foi recebido")

        raise HTTPException(
            status_code=401,
            detail="Token de autenticação não fornecido",
        )

    token = credentials.credentials

    print("Token recebido pelo FastAPI")

    try:
        jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"

        print(f"JWKS URL: {jwks_url}")
        print(f"Audience esperado: {AUTH0_AUDIENCE}")
        print(f"Issuer esperado: https://{AUTH0_DOMAIN}/")

        jwks_client = PyJWKClient(jwks_url)

        signing_key = jwks_client.get_signing_key_from_jwt(token)

        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=ALGORITHMS,
            audience=AUTH0_AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/",
        )

        print("Token validado com sucesso")

        return payload

    except Exception as erro:
        print(f"ERRO NA VALIDAÇÃO DO TOKEN: {type(erro).__name__}: {erro}")

        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado",
        )
        
def exigir_permissions(permissao_necessaria: str):
    def verificar_permissão(
        payload=Security(validar_token)
    ):
        permissoes = payload.get("permissions", [])
        
        if permissao_necessaria not in permissoes:
            raise HTTPException(
                status_code=403,
                detail="Permissão insuficiente",
            )
        return payload
    return verificar_permissão