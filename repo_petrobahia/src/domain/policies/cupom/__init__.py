"""Pacote de cupons (Strategy), sob policies.

Estrutura:
- base.py: Interface Cupom
- nulo.py: CupomNulo
- percentual.py: CupomPercentual
- valor_fixo.py: CupomValorFixo
- lubrificante.py: CupomLubrificante
- factory.py: CupomFactory
"""

from .base import Cupom
from .lubrificante import CupomLubrificante
from .nulo import CupomNulo
from .percentual import CupomPercentual
from .valor_fixo import CupomValorFixo

__all__ = [
    "Cupom",
    "CupomNulo",
    "CupomPercentual",
    "CupomValorFixo",
    "CupomLubrificante",
]
