"""
Schemas Pydantic para validação de dados
"""
from pydantic import BaseModel, Field
from typing import List

# Modelo de Produto
class ProdutoInput(BaseModel):
    """
    Schema para representaros dados de entrada de um produto
    """    
    nome: str = Field(..., min_length=1, max_length=256, description="Nome do produto")
    preco: float = Field(..., ge=0.01, le=99999.99, description="Preço do produto")


class MessageInput(BaseModel):
    """
    Schema para entrada de mensagem
    """
    text: str = Field(...,
                      min_length=1,
                      max_length=500,
                      description="Texto da mensagem"
                      )
    priority: int = Field(
        default=1,
        ge=1, #ge= greater equal
        le=5, #le= less equal
        description="Prioridade da mensagem (1-5)")
    
    class Config:
        json_schema_extra  = {
            "example": {
                "text": "Esta é uma mensagem de teste.",
                "priority": 3
            }
        }

class ProdutoOutput(BaseModel):
    """
    Schema para representaros dados de saída de um produto
    """
    id: int
    nome: str 
    preco: float 

class CupomInput(BaseModel):
    cupom: str = Field(..., min_length=1, max_length=50, description="Código do cupom de desconto")
