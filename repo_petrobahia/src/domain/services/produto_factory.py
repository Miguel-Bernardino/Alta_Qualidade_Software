"""Factory para criação de produtos com políticas de desconto."""

from src.domain.models.produto import Produto
from src.domain.policies.politica_desconto import PoliticaDesconto
from src.domain.policies.politica_desconto_produto_disel import (
    PoliticaDescontoProdutoDisel,
)
from src.domain.policies.politica_desconto_produto_etanol import (
    PoliticaDescontoProdutoEtanol,
)
from src.domain.policies.politica_desconto_produto_gasolina import (
    PoliticaDescontoProdutoGasolina,
)
from src.domain.policies.politica_desconto_produto_none import (
    PoliticaDescontoProdutoNone,
)


class ProdutoFactory:
    """Factory para criação de produtos com regras de negócio (Domain Service).

    Centraliza lógica de criação e mapeamento de políticas de desconto.
    """

    _POLITICAS_PADRAO = {
        "diesel": PoliticaDescontoProdutoDisel,
        "gasolina": PoliticaDescontoProdutoGasolina,
        "etanol": PoliticaDescontoProdutoEtanol,
    }

    _PRECOS_PADRAO = {
        "diesel": 5.50,
        "gasolina": 6.20,
        "etanol": 4.80,
        "lubrificante": 35.00,
    }

    @classmethod
    def criar(
        cls,
        tipo: str,
        preco: float | None = None,
        politica: PoliticaDesconto | None = None,
    ) -> Produto:
        """Cria produto com valores padrão se não especificados.

        Args:
            tipo: Tipo de produto (diesel, gasolina, etc)
            preco: Preço opcional (usa padrão se None)
            politica: Política de desconto opcional (usa padrão do tipo se None)

        Returns:
            Produto configurado
        """
        preco_final = preco if preco is not None else cls._PRECOS_PADRAO.get(tipo, 0.0)

        if politica is None:
            politica_cls = cls._POLITICAS_PADRAO.get(tipo, PoliticaDescontoProdutoNone)
            politica = politica_cls()

        return Produto(tipo=tipo, preco=preco_final, politica_desconto=politica)

    @classmethod
    def criar_catalogo_padrao(cls) -> dict[str, Produto]:
        """Retorna catálogo completo com produtos padrão."""
        return {
            "diesel": cls.criar("diesel"),
            "gasolina": cls.criar("gasolina"),
            "etanol": cls.criar("etanol"),
            "lubrificante": cls.criar("lubrificante"),
        }
