import ast
from pathlib import Path
from typing import Iterable

from src.domain.models.cliente import Cliente
from src.domain.models.item_pedido import ItemPedido
from src.domain.models.pedido import Pedido
from src.domain.models.produto import Produto
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
from src.domain.services.cupom_service import CupomFactory
from src.repositories.interfaces.i_pedido_repository import IPedidoRepository


class PedidoRepositoryArquivo(IPedidoRepository):
    """Persistência de pedidos em arquivo TXT (formato dict string)."""

    _POLITICAS = {
        "diesel": PoliticaDescontoProdutoDisel,
        "gasolina": PoliticaDescontoProdutoGasolina,
        "etanol": PoliticaDescontoProdutoEtanol,
    }

    def __init__(self, caminho_arquivo: str = "pedidos.txt"):
        self._path = Path(caminho_arquivo)
        if not self._path.exists():
            self._path.write_text("", encoding="utf-8")

    def salvar(self, pedido: Pedido) -> None:
        """Salva pedido em formato dict string."""
        pedido_dict = {
            "cliente": {
                "nome": pedido.cliente.nome,
                "email": pedido.cliente.email,
                "cnpj": pedido.cliente.cnpj,
            },
            "itens": [
                {
                    "produto_tipo": item.produto.tipo,
                    "quantidade": item.quantidade,
                    "preco_unitario": item.preco_unitario,
                    "desconto_produto": item.desconto_produto,
                    "desconto_cupom": item.desconto_cupom,
                    "preco_final": item.preco_final,
                }
                for item in pedido.itens
            ],
            "preco_total": pedido.preco_total,
        }
        with self._path.open("a", encoding="utf-8") as file:
            file.write(str(pedido_dict) + "\n")
        print(f"Pedido salvo para cliente: {pedido.cliente.nome} (CNPJ: {pedido.cliente.cnpj})")

    def buscar_por_cliente(self, cnpj: str) -> list[Pedido]:
        """Retorna pedidos de um cliente pelo CNPJ."""
        pedidos = []
        if not self._path.exists():
            return pedidos

        with self._path.open("r", encoding="utf-8") as file:
            for linha in file:
                linha = linha.strip()
                if not linha:
                    continue

                dados = ast.literal_eval(linha)
                cliente_dados = dados["cliente"]

                if cliente_dados["cnpj"] == cnpj:
                    cliente = Cliente(
                        nome=cliente_dados["nome"],
                        email=cliente_dados["email"],
                        cnpj=cliente_dados["cnpj"],
                    )

                    itens = []
                    for item_dados in dados["itens"]:
                        politica_cls = self._POLITICAS.get(
                            item_dados["produto_tipo"], PoliticaDescontoProdutoNone
                        )
                        produto = Produto(
                            tipo=item_dados["produto_tipo"],
                            preco=item_dados["preco_unitario"],
                            politica_desconto=politica_cls(),
                        )
                        cupom = CupomFactory.criar(None)
                        item = ItemPedido(
                            produto=produto,
                            quantidade=item_dados["quantidade"],
                            cupom=cupom,
                        )
                        itens.append(item)

                    pedido = Pedido(cliente=cliente, itens=itens)
                    pedidos.append(pedido)

        return pedidos
