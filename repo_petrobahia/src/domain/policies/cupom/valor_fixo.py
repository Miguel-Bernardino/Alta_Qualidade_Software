from .base import Cupom


class CupomValorFixo(Cupom):
    def __init__(self, valor: float):
        if valor < 0:
            raise ValueError("Valor fixo deve ser não-negativo.")
        self._valor = valor

    def calcular_desconto(self, preco_bruto: float, produto_tipo: str = "") -> float:
        return min(self._valor, preco_bruto)
