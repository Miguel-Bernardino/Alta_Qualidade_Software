"""Testes para modelos de domínio usando pytest."""

import pytest

from src.domain.models.cliente import Cliente
from src.domain.models.item_pedido import ItemPedido
from src.domain.models.pedido import Pedido
from src.domain.models.produto import Produto
from src.domain.policies.cupom import CupomNulo, CupomPercentual, CupomValorFixo
from src.domain.policies.desconto.politica_desconto_produto_disel import (
    PoliticaDescontoProdutoDisel,
)
from src.domain.policies.desconto.politica_desconto_produto_none import (
    PoliticaDescontoProdutoNone,
)


class TestCliente:
    """Testes para modelo Cliente."""

    def test_criar_cliente_valido(self):
        """Deve criar cliente com dados válidos."""
        cliente = Cliente(email="teste@empresa.com", nome="Empresa Teste", cnpj="12345678000199")
        assert cliente.email == "teste@empresa.com"
        assert cliente.nome == "Empresa Teste"
        assert cliente.cnpj == "12345678000199"

    def test_cliente_nome_vazio_invalido(self):
        """Deve rejeitar cliente com nome vazio."""
        with pytest.raises(ValueError, match="Nome não pode ser vazio"):
            Cliente(email="teste@empresa.com", nome="", cnpj="12345678000199")


class TestProduto:
    """Testes para modelo Produto."""

    def test_criar_produto_com_politica(self):
        """Deve criar produto com política de desconto."""
        politica = PoliticaDescontoProdutoDisel()
        produto = Produto(tipo="diesel", preco=5.5, politica_desconto=politica)
        assert produto.tipo == "diesel"
        assert produto.preco == 5.5
        assert produto.politica_desconto == politica

    def test_produto_sem_desconto(self):
        """Deve retornar 0 para produto sem política de desconto."""
        politica = PoliticaDescontoProdutoNone()
        produto = Produto(tipo="lubrificante", preco=35.0, politica_desconto=politica)
        # Criar um item para testar
        item = ItemPedido(produto=produto, quantidade=10, cupom=CupomNulo())
        desconto = produto.politica_desconto.calcular_desconto(item)
        assert desconto == 0.0


class TestItemPedido:
    """Testes para ItemPedido."""

    def test_item_pedido_sem_cupom(self):
        """Deve calcular preço de item sem cupom."""
        produto = Produto(
            tipo="gasolina", preco=6.2, politica_desconto=PoliticaDescontoProdutoNone()
        )
        cupom = CupomNulo()
        item = ItemPedido(produto=produto, quantidade=100, cupom=cupom)

        assert item.preco_unitario == 6.2
        assert item.quantidade == 100
        assert item.desconto_produto == 0.0
        assert item.desconto_cupom == 0.0
        assert item.preco_final == 620.0

    def test_item_pedido_com_cupom_percentual(self):
        """Deve calcular preço com cupom de desconto percentual."""
        produto = Produto(tipo="etanol", preco=4.8, politica_desconto=PoliticaDescontoProdutoNone())
        cupom = CupomPercentual(percentual=0.10)
        item = ItemPedido(produto=produto, quantidade=50, cupom=cupom)

        assert item.desconto_cupom == 24.0  # 50 * 4.8 * 0.10
        assert item.preco_final == 216.0  # 240 - 24

    def test_item_pedido_com_cupom_valor_fixo(self):
        """Deve calcular preço com cupom de valor fixo."""
        produto = Produto(
            tipo="gasolina", preco=6.2, politica_desconto=PoliticaDescontoProdutoNone()
        )
        cupom = CupomValorFixo(valor=50.0)
        item = ItemPedido(produto=produto, quantidade=20, cupom=cupom)

        assert item.desconto_cupom == 50.0
        assert item.preco_final == 74.0  # 124 - 50

    def test_item_pedido_quantidade_invalida(self):
        """Deve rejeitar quantidade zero ou negativa."""
        produto = Produto(tipo="diesel", preco=5.5, politica_desconto=PoliticaDescontoProdutoNone())
        cupom = CupomNulo()

        with pytest.raises(ValueError, match="Quantidade deve ser positiva"):
            ItemPedido(produto=produto, quantidade=0, cupom=cupom)

    def test_item_pedido_com_desconto_diesel(self):
        """Deve calcular desconto diesel para quantidade > 1000L."""
        produto = Produto(
            tipo="diesel", preco=5.5, politica_desconto=PoliticaDescontoProdutoDisel()
        )
        item = ItemPedido(produto=produto, quantidade=1200, cupom=CupomNulo())

        # Desconto produto: 1200 * 5.5 * 0.10 = 660
        assert item.desconto_produto == 660.0
        # Preço final: (1200 * 5.5) - 660 = 6600 - 660 = 5940
        assert item.preco_final == 5940.0


class TestPedido:
    """Testes para agregado Pedido."""

    def test_pedido_calcula_preco_total(self):
        """Deve calcular preço total somando itens."""
        cliente = Cliente(email="teste@empresa.com", nome="Cliente Teste", cnpj="12345678000199")
        produto1 = Produto(
            tipo="diesel", preco=5.5, politica_desconto=PoliticaDescontoProdutoNone()
        )
        produto2 = Produto(
            tipo="gasolina", preco=6.2, politica_desconto=PoliticaDescontoProdutoNone()
        )

        item1 = ItemPedido(produto=produto1, quantidade=100, cupom=CupomNulo())
        item2 = ItemPedido(produto=produto2, quantidade=50, cupom=CupomNulo())

        pedido = Pedido(cliente=cliente, itens=[item1, item2])

        assert pedido.preco_total == 860.0  # (100*5.5) + (50*6.2)

    def test_pedido_sem_itens(self):
        """Deve aceitar pedido sem itens (preco_total = 0)."""
        cliente = Cliente(email="teste@empresa.com", nome="Cliente Teste", cnpj="12345678000199")
        pedido = Pedido(cliente=cliente, itens=[])
        assert pedido.preco_total == 0.0
