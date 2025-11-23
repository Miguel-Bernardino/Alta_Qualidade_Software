from abc import ABC, abstractmethod


class Cupom(ABC):
    """Abstração para cupons de desconto (Strategy Pattern).

    Cada cupom define sua própria lógica de cálculo.
    """

    @abstractmethod
    def calcular_desconto(self, preco_bruto: float, produto_tipo: str = "") -> float:
        """Calcula o valor de desconto a partir do preço bruto.
        
        Args:
            preco_bruto: Valor sem desconto
            produto_tipo: Tipo do produto (opcional, para cupons específicos)
        """
        raise NotImplementedError


class CupomNulo(Cupom):
    """Representa ausência de cupom (Null Object Pattern)."""

    def calcular_desconto(self, preco_bruto: float, produto_tipo: str = "") -> float:
        return 0.0


class CupomPercentual(Cupom):
    """Cupom com desconto percentual."""

    def __init__(self, percentual: float):
        if not 0 <= percentual <= 1:
            raise ValueError("Percentual deve estar entre 0 e 1.")
        self._percentual = percentual

    def calcular_desconto(self, preco_bruto: float, produto_tipo: str = "") -> float:
        return preco_bruto * self._percentual


class CupomValorFixo(Cupom):
    """Cupom com desconto de valor fixo."""

    def __init__(self, valor: float):
        if valor < 0:
            raise ValueError("Valor fixo deve ser não-negativo.")
        self._valor = valor

    def calcular_desconto(self, preco_bruto: float, produto_tipo: str = "") -> float:
        return min(self._valor, preco_bruto)


class CupomLubrificante(Cupom):
    """Cupom de valor fixo válido apenas para lubrificantes."""

    def __init__(self, valor: float):
        if valor < 0:
            raise ValueError("Valor fixo deve ser não-negativo.")
        self._valor = valor

    def calcular_desconto(self, preco_bruto: float, produto_tipo: str = "") -> float:
        """Aplica desconto apenas se o produto for lubrificante."""
        if produto_tipo.lower() == "lubrificante":
            return min(self._valor, preco_bruto)
        return 0.0


# Fábrica de cupons por código (pode ser movida para um repositório depois)
class CupomFactory:
    """Factory para instanciar cupons a partir de códigos."""

    _CUPONS = {
        "MEGA10": CupomPercentual(0.10),
        "NOVO5": CupomPercentual(0.05),
        "LUB2": CupomLubrificante(2.0),
    }

    @classmethod
    def criar(cls, codigo: str | None) -> Cupom:
        """Retorna o cupom correspondente ou CupomNulo se inválido."""
        if not codigo:
            return CupomNulo()
        return cls._CUPONS.get(codigo, CupomNulo())
