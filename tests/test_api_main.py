"""
Testes para a API de produtos e descontos.
"""
import pytest
from fastapi.testclient import TestClient
from src.api.main import app
from src.config import API_VERSION

# Cria um cliente de teste para a aplicação FastAPI
client = TestClient(app)


def test_home():
    """Testa o endpoint raiz '/'."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"mensagem": "Bem-vindo à API de produtos e descontos"}


def test_health_check():
    """Testa o endpoint de health check '/health'."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": API_VERSION}


def test_listar_produtos():
    """Testa o endpoint para listar todos os produtos '/produtos'."""
    response = client.get("/produtos")
    assert response.status_code == 200
    data = response.json()
    assert "produtos" in data
    assert isinstance(data["produtos"], list)
    assert len(data["produtos"]) == 3  # Baseado no banco de dados simulado


def test_consultar_produto_existente():
    """Testa a consulta de um produto que existe."""
    response = client.get("/produtos/1")
    assert response.status_code == 200
    produto = response.json()
    assert produto["id"] == 1
    assert produto["nome"] == "Notebook"
    assert produto["preco"] == 3000.00


def test_consultar_produto_inexistente():
    """Testa a consulta de um produto que não existe."""
    response = client.get("/produtos/99")
    assert response.status_code == 404
    assert response.json() == {"detail": "Produto não encontrado"}


def test_aplicar_desconto_valido():
    """Testa a aplicação de um cupom de desconto válido."""
    response = client.post(
        "/produtos/1/calcular_desconto",
        json={"cupom": "PROMO10"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["nome"] == "Notebook"
    assert data["preco_original"] == 3000.00
    assert data["desconto_percentual"] == pytest.approx(10.0)
    assert data["preco_final"] == 2700.00


def test_aplicar_desconto_invalido():
    """Testa a aplicação de um cupom de desconto inválido."""
    response = client.post(
        "/produtos/2/calcular_desconto",
        json={"cupom": "INVALIDO"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Cupom inválido"}


def test_aplicar_desconto_produto_inexistente():
    """Testa a aplicação de desconto em um produto que não existe."""
    response = client.post(
        "/produtos/99/calcular_desconto",
        json={"cupom": "PROMO10"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Produto não encontrado"}


def test_aplicar_desconto_cupom_vazio():
    """Testa a aplicação de um cupom vazio (deve falhar na validação do Pydantic)."""
    response = client.post(
        "/produtos/1/calcular_desconto",
        json={"cupom": ""}
    )
    # O FastAPI retorna 422 para erros de validação de entrada
    assert response.status_code == 422


def test_aplicar_desconto_payload_invalido():
    """Testa o endpoint de desconto com um payload malformado."""
    response = client.post(
        "/produtos/1/calcular_desconto",
        json={"codigo_cupom": "PROMO10"}  # Chave errada
    )
    assert response.status_code == 422