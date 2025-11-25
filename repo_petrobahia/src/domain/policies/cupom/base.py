from abc import ABC, abstractmethod


class Cupom(ABC):
    """Abstração para cupons de desconto (Strategy Pattern)."""

    @abstractmethod
    def calcular_desconto(self, preco_bruto: float, produto_tipo: str = "") -> float:
        """Calcula o valor de desconto a partir do preço bruto."""
        raise NotImplementedError
