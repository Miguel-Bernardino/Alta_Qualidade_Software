from .base import Cupom


class CupomPercentual(Cupom):
    def __init__(self, percentual: float):
        if not 0 <= percentual <= 1:
            raise ValueError("Percentual deve estar entre 0 e 1.")
        self._percentual = percentual

    def calcular_desconto(self, preco_bruto: float, produto_tipo: str = "") -> float:
        return preco_bruto * self._percentual
