from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

from ..config import API_VERSION, API_TITLE, LOG_FORMAT, LOG_DIR

from ..data.schemas import CupomInput, ProdutoOutput
from .cupom_desconto import CupomDesconto


#configurar logging



LOG_DIR.mkdir(exist_ok=True)


def setup_logging():
    """
    Configura sistema de logging da aplicação
    """
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, handlers=[
            logging.FileHandler(LOG_DIR / "app.log", "w", "utf-8"),
            logging.StreamHandler()
        ])
   
    
    return logging.getLogger("api_produtos_descontos")


# Logger global
logger = setup_logging()
logger.info("Logging configurado com sucesso")


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
    logger.info("Requisição recebida no endpoint raiz")
    return {"mensagem": f"Bem-vindo à {API_TITLE}"}

@app.get("/health")
def health_check():
    """
    Health check - verifica se API está funcionando
    """
    logger.info("Requisição recebida no endpoint health")
    return {
        "status": "healthy",
        "version": API_VERSION
    }

@app.get("/produtos")
def listar_produtos():
    """
    Lista todos os produtos.
    """
    logger.info("Requisição recebida no endpoint listar_produtos")
    return {"produtos": produtos_db}

@app.get("/produtos/{produto_id}", response_model=ProdutoOutput)
def consultar_produto(produto_id: int):
    """
    Retorna um determinado produto pelo ID.
    """
    logger.info("Requisição recebida no endpoint consultar_produto")
    produto = next((p for p in produtos_db if p["id"] == produto_id), None)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@app.post("/produtos/{produto_id}/calcular_desconto", response_model=dict) 
def aplicar_desconto(produto_id: int, cupom: CupomInput):
    """
    Calcular o desconto de um produto através do cupom informado.
    """
    logger.info("Requisição recebida no endpoint aplicar_desconto")
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

# Problemas com a importação relativaquando executa o script diretamente
# if __name__ == "__main__":
#     uvicorn.run('src.api.main:app', host="127.0.0.1", port=8000, reload=True)