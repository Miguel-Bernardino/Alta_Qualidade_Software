from dataclasses import dataclass

from src.domain.policies.desconto.politica_desconto import PoliticaDesconto
from src.domain.policies.desconto.politica_desconto_produto_none import (
    PoliticaDescontoProdutoNone,
)


@dataclass
class Produto:
    """Produto de catálogo com política de desconto associada."""

    tipo: str
    preco: float = 0.0
    politica_desconto: PoliticaDesconto = PoliticaDescontoProdutoNone()
