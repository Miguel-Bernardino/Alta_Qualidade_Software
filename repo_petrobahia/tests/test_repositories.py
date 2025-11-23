"""Testes para repositórios usando unittest com mocks."""
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.domain.models.cliente import Cliente
from src.domain.models.item_pedido import ItemPedido
from src.domain.models.pedido import Pedido
from src.domain.models.produto import Produto
from src.domain.policies.politica_desconto_produto_none import PoliticaDescontoProdutoNone
from src.domain.services.cupom_service import CupomNulo
from src.repositories.cliente_repository import ClienteRepositoryArquivo
from src.repositories.pedido_repository import PedidoRepositoryArquivo


class TestClienteRepository(unittest.TestCase):
    """Testes para ClienteRepositoryArquivo."""

    def setUp(self):
        """Configuração antes de cada teste."""
        self.temp_dir = TemporaryDirectory()
        self.arquivo_path = Path(self.temp_dir.name) / "clientes_test.txt"
        self.repository = ClienteRepositoryArquivo(str(self.arquivo_path))

    def tearDown(self):
        """Limpeza após cada teste."""
        self.temp_dir.cleanup()

    def test_salvar_cliente(self):
        """Deve salvar cliente no arquivo."""
        cliente = Cliente(
            email="teste@empresa.com", nome="Empresa Teste", cnpj="12345678000199"
        )
        self.repository.salvar(cliente)

        # Verificar se arquivo foi criado
        self.assertTrue(self.arquivo_path.exists())

        # Verificar conteúdo
        conteudo = self.arquivo_path.read_text(encoding="utf-8")
        self.assertIn("Empresa Teste", conteudo)
        self.assertIn("teste@empresa.com", conteudo)
        self.assertIn("12345678000199", conteudo)

    def test_listar_clientes(self):
        """Deve listar clientes salvos."""
        cliente1 = Cliente(
            email="teste1@empresa.com", nome="Empresa 1", cnpj="11111111000199"
        )
        cliente2 = Cliente(
            email="teste2@empresa.com", nome="Empresa 2", cnpj="22222222000199"
        )

        self.repository.salvar(cliente1)
        self.repository.salvar(cliente2)

        clientes = list(self.repository.listar())

        self.assertEqual(len(clientes), 2)
        self.assertEqual(clientes[0].nome, "Empresa 1")
        self.assertEqual(clientes[1].nome, "Empresa 2")

    def test_listar_arquivo_vazio(self):
        """Deve retornar lista vazia para arquivo sem clientes."""
        clientes = list(self.repository.listar())
        self.assertEqual(len(clientes), 0)


class TestPedidoRepository(unittest.TestCase):
    """Testes para PedidoRepositoryArquivo."""

    def setUp(self):
        """Configuração antes de cada teste."""
        self.temp_dir = TemporaryDirectory()
        self.arquivo_path = Path(self.temp_dir.name) / "pedidos_test.txt"
        self.repository = PedidoRepositoryArquivo(str(self.arquivo_path))

    def tearDown(self):
        """Limpeza após cada teste."""
        self.temp_dir.cleanup()

    def test_salvar_pedido(self):
        """Deve salvar pedido no arquivo."""
        cliente = Cliente(
            email="teste@empresa.com", nome="Empresa Teste", cnpj="12345678000199"
        )
        produto = Produto(
            tipo="diesel", preco=5.5, politica_desconto=PoliticaDescontoProdutoNone()
        )
        item = ItemPedido(produto=produto, quantidade=100, cupom=CupomNulo())
        pedido = Pedido(cliente=cliente, itens=[item])

        self.repository.salvar(pedido)

        # Verificar se arquivo foi criado
        self.assertTrue(self.arquivo_path.exists())

        # Verificar conteúdo
        conteudo = self.arquivo_path.read_text(encoding="utf-8")
        self.assertIn("Empresa Teste", conteudo)
        self.assertIn("12345678000199", conteudo)
        self.assertIn("diesel", conteudo)

    def test_buscar_por_cliente(self):
        """Deve buscar pedidos por CNPJ do cliente."""
        cliente1 = Cliente(
            email="teste1@empresa.com", nome="Empresa 1", cnpj="11111111000199"
        )
        cliente2 = Cliente(
            email="teste2@empresa.com", nome="Empresa 2", cnpj="22222222000199"
        )

        produto = Produto(
            tipo="gasolina", preco=6.2, politica_desconto=PoliticaDescontoProdutoNone()
        )
        item = ItemPedido(produto=produto, quantidade=50, cupom=CupomNulo())

        pedido1 = Pedido(cliente=cliente1, itens=[item])
        pedido2 = Pedido(cliente=cliente2, itens=[item])

        self.repository.salvar(pedido1)
        self.repository.salvar(pedido2)

        # Buscar pedidos do cliente1
        pedidos = self.repository.buscar_por_cliente("11111111000199")

        self.assertEqual(len(pedidos), 1)
        self.assertEqual(pedidos[0].cliente.cnpj, "11111111000199")
        self.assertEqual(pedidos[0].cliente.nome, "Empresa 1")

    def test_buscar_cliente_sem_pedidos(self):
        """Deve retornar lista vazia para cliente sem pedidos."""
        pedidos = self.repository.buscar_por_cliente("99999999000199")
        self.assertEqual(len(pedidos), 0)


if __name__ == "__main__":
    unittest.main()
