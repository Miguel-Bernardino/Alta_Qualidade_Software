"""Testes para serviços de domínio usando pytest."""
import pytest

from src.domain.exceptions import ValidationError
from src.domain.models.cliente import Cliente
from src.domain.models.item_pedido import ItemPedido
from src.domain.models.pedido import Pedido
from src.domain.models.produto import Produto
from src.domain.policies.politica_desconto_produto_none import PoliticaDescontoProdutoNone
from src.domain.services.cupom_service import (
    CupomFactory,
    CupomLubrificante,
    CupomNulo,
    CupomPercentual,
)
from src.domain.services.produto_factory import ProdutoFactory
from src.domain.services.validar_pedido import ValidadorPedido


class TestCupomService:
    """Testes para CupomFactory e tipos de cupom."""

    def test_criar_cupom_nulo(self):
        """Deve criar cupom nulo quando código é None."""
        cupom = CupomFactory.criar(None)
        assert isinstance(cupom, CupomNulo)
        assert cupom.calcular_desconto(100.0) == 0.0

    def test_criar_cupom_percentual_mega10(self):
        """Deve criar cupom MEGA10 (10% desconto)."""
        cupom = CupomFactory.criar("MEGA10")
        assert isinstance(cupom, CupomPercentual)
        assert cupom.calcular_desconto(1000.0) == 100.0

    def test_criar_cupom_codigo_invalido(self):
        """Deve retornar cupom nulo para código inválido."""
        cupom = CupomFactory.criar("INVALIDO")
        assert isinstance(cupom, CupomNulo)
        assert cupom.calcular_desconto(100.0) == 0.0

    def test_cupom_lubrificante_aplica_desconto(self):
        """Deve aplicar desconto LUB2 apenas para lubrificante."""
        cupom = CupomFactory.criar("LUB2")
        assert isinstance(cupom, CupomLubrificante)
        # Aplica desconto para lubrificante
        assert cupom.calcular_desconto(100.0, "lubrificante") == 2.0
        # Não aplica para outros produtos
        assert cupom.calcular_desconto(100.0, "diesel") == 0.0
        assert cupom.calcular_desconto(100.0, "gasolina") == 0.0


class TestProdutoFactory:
    """Testes para ProdutoFactory."""

    def test_criar_catalogo_padrao(self):
        """Deve criar catálogo com produtos padrão."""
        catalogo = ProdutoFactory.criar_catalogo_padrao()

        assert "diesel" in catalogo
        assert "gasolina" in catalogo
        assert "etanol" in catalogo
        assert "lubrificante" in catalogo

        assert catalogo["diesel"].preco == 5.5
        assert catalogo["gasolina"].preco == 6.2
        assert catalogo["etanol"].preco == 4.8
        assert catalogo["lubrificante"].preco == 35.0

    def test_produtos_tem_politicas_corretas(self):
        """Deve criar produtos com políticas de desconto corretas."""
        catalogo = ProdutoFactory.criar_catalogo_padrao()

        # Diesel, gasolina e etanol têm políticas específicas
        assert catalogo["diesel"].politica_desconto is not None
        assert catalogo["gasolina"].politica_desconto is not None
        assert catalogo["etanol"].politica_desconto is not None

        # Lubrificante usa política None
        assert isinstance(
            catalogo["lubrificante"].politica_desconto, PoliticaDescontoProdutoNone
        )


class TestValidadorPedido:
    """Testes para ValidadorPedido."""

    def test_pedido_valido(self):
        """Deve aceitar pedido válido."""
        cliente = Cliente(email="teste@empresa.com", nome="Cliente Teste", cnpj="12345678000199")
        produto = Produto(
            tipo="diesel", preco=5.5, politica_desconto=PoliticaDescontoProdutoNone()
        )
        item = ItemPedido(produto=produto, quantidade=200, cupom=CupomNulo())
        pedido = Pedido(cliente=cliente, itens=[item])

        # Não deve lançar exceção
        ValidadorPedido.validar(pedido)

    def test_pedido_sem_cliente(self):
        """Deve rejeitar pedido sem cliente."""
        produto = Produto(
            tipo="diesel", preco=5.5, politica_desconto=PoliticaDescontoProdutoNone()
        )
        item = ItemPedido(produto=produto, quantidade=100, cupom=CupomNulo())
        pedido = Pedido(cliente=None, itens=[item])

        with pytest.raises(ValidationError, match="Pedido deve ter um cliente"):
            ValidadorPedido.validar(pedido)

    def test_pedido_sem_itens(self):
        """Deve rejeitar pedido sem itens."""
        cliente = Cliente(email="teste@empresa.com", nome="Cliente Teste", cnpj="12345678000199")
        pedido = Pedido(cliente=cliente, itens=[])

        with pytest.raises(ValidationError, match="Pedido deve ter no mínimo 1 item"):
            ValidadorPedido.validar(pedido)
