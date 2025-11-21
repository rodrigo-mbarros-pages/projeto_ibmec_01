# Dicionário de cupons de desconto
# Aplicar ao preço do produto para obter o valor final
# Exemplo: "PROMO10": 0.90 aplica 10% de desconto (valor final = preço * 0.90)

from data.schemas import CupomInput


class CupomDesconto:
    """
    Classe para gerenciar cupons de desconto.
    """

    # Dicionário de cupons de desconto
    _cupom_descontos = {"PROMO10": 0.90, "PROMO20": 0.80, "PROMO30": 0.70}

    # Atributos
    #   - codigo: código do cupom
    #   - is_valid: indica se o cupom é válido
    #   - fator_desconto: fator a ser aplicado ao preço do produto
    #   ---- Se cumpom não for válido, fator_desconto = 1.0 (sem desconto)
    codigo: str
    is_valid: bool = False
    fator_desconto: float = 1.0

    def __init__(self, codigo: str):
        self.codigo = codigo
        self.is_valid = codigo in self._cupom_descontos
        if self.is_valid:
            self.fator_desconto = self._cupom_descontos[codigo]

    def aplicar_desconto(self, preco: float):
        """
        Calcular o valor final do produto após aplicar o desconto.
        """
        return preco * self.fator_desconto

    def get_fator_desconto(self):
        """
        Retorna o valor a ser aplicado ao preço do produto conforme o cupom informado.
        """
        return self.fator_desconto
