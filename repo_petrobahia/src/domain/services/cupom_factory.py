from src.domain.policies.cupom.base import Cupom
from src.domain.policies.cupom.lubrificante import CupomLubrificante
from src.domain.policies.cupom.nulo import CupomNulo
from src.domain.policies.cupom.percentual import CupomPercentual
from src.domain.policies.cupom.valor_fixo import CupomValorFixo


class CupomFactory:
    """Factory para instanciar cupons a partir de códigos (Domain Service)."""

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
