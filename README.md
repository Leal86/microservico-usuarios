Criar venv:  python -m venv venv  

Ativar a venv: .\venv\Scripts\Activate.ps1   

Criar arquivo de dependencias: pip freeze > requirements txt 
                                                                     
Instalar dependencias: pip install -r requirements.txt  

Executar projeto: python -m uvicorn app.main:app --reload

Executar testes: python -m pytest -v