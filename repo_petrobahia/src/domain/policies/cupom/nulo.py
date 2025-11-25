from .base import Cupom


class CupomNulo(Cupom):
    def calcular_desconto(self, preco_bruto: float, produto_tipo: str = "") -> float:
        return 0.0
