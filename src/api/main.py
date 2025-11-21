from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

from ..data.schemas import CupomInput, ProdutoOutput
from .cupom_desconto import CupomDesconto

app = FastAPI()

# Modelo de dados
class Produto(BaseModel):
    id: int
    nome: str
    preco: float


# Banco de dados simulado
produtos_db = [
    {"id": 1, "nome": "Notebook", "preco": 3000.00},
    {"id": 2, "nome": "Mouse", "preco": 50.00},
    {"id": 3, "nome": "Teclado", "preco": 150.00},
]


# Endpoints
@app.get("/")
def home():
    """
    Endpoint raiz - mensagem de boas-vindas
    """
    return {"mensagem": "Bem-vindo à API de Produtos"}

@app.get("/health")
def health_check():
    """
    Health check - verifica se API está funcionando
    """
    return {
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/produtos")
def listar_produtos():
    """
    Lista todos os produtos.
    """
    return {"produtos": produtos_db}

@app.get("/produtos/{produto_id}", response_model=ProdutoOutput)
def consultar_produto(produto_id: int):
    """
    Retorna um determinado produto pelo ID.
    """
    produto = next((p for p in produtos_db if p["id"] == produto_id), None)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@app.post("/produtos/{produto_id}/calcular_desconto", response_model=dict) 
def aplicar_desconto(produto_id: int, cupom: CupomInput):
    """
    Calcular o desconto de um produto através do cupom informado.
    """
    produto = next((p for p in produtos_db if p["id"] == produto_id), None)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    cupom_desconto = CupomDesconto(cupom.cupom)

    if not cupom_desconto.is_valid:
        raise HTTPException(status_code=400, detail="Cupom inválido")
    
    preco_original = produto["preco"]
    produto["preco"] = preco_original *  cupom_desconto.fator_desconto    
    return {
        "id": produto["id"],
        "nome": produto["nome"],
        "preco_original": preco_original,
        "desconto_percentual":  (1 - cupom_desconto.fator_desconto) * 100,
        "preco_final": produto["preco"]
    }

if __name__ == "__main__":
    uvicorn.run('src.api.main:app', host="127.0.0.1", port=8000, reload=True)