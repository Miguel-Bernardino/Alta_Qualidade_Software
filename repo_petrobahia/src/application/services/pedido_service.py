from src.domain.models.cliente import Cliente
from src.domain.models.item_pedido import ItemPedido
from src.domain.models.pedido import Pedido
from src.domain.models.produto import Produto
from src.domain.services.cupom_factory import CupomFactory
from src.domain.services.validar_pedido import ValidadorPedido
from src.repositories.interfaces.i_pedido_repository import IPedidoRepository


class PedidoService:
    """Serviço de aplicação para processar pedidos.

    Orquestra criação de pedidos, aplicação de cupons, validações e persistência.
    Segue princípios SOLID: SRP (responsabilidade única), DIP (depende de interface).
    """

    def __init__(self, pedido_repository: IPedidoRepository):
        self._repository = pedido_repository

    def criar_pedido(
        self,
        cliente: Cliente,
        itens_dados: list[dict],
        catalogo_produtos: dict[str, Produto],
    ) -> Pedido:
        """Cria um pedido a partir de dados brutos.

        Args:
            cliente: Instância de Cliente
            itens_dados: Lista de dicts com 'produto_tipo', 'quantidade', 'cupom_codigo' (opcional)
            catalogo_produtos: Mapa de tipo de produto para instância Produto

        Returns:
            Pedido criado e calculado

        Raises:
            ValueError: Se produto não existir no catálogo ou dados inválidos
            ValidationError: Se regras de negócio forem violadas
        """
        if not cliente:
            raise ValueError("Cliente deve ser informado.")
        if not itens_dados:
            raise ValueError("Pedido deve ter ao menos um item.")

        itens = []
        for dados in itens_dados:
            produto_tipo = dados.get("produto_tipo")
            quantidade = dados.get("quantidade")
            cupom_codigo = dados.get("cupom_codigo")

            if not produto_tipo or quantidade is None:
                raise ValueError("Item deve ter produto_tipo e quantidade.")

            produto = catalogo_produtos.get(produto_tipo)
            if not produto:
                raise ValueError(f"Produto '{produto_tipo}' não encontrado no catálogo.")

            cupom = CupomFactory.criar(cupom_codigo)
            item = ItemPedido(produto=produto, quantidade=quantidade, cupom=cupom)
            itens.append(item)

        pedido = Pedido(cliente=cliente, itens=itens)

        # Validação de regras de negócio
        ValidadorPedido.validar(pedido)

        print(f"Pedido criado para {cliente.nome} com total: {pedido.preco_total:.2f}")
        return pedido

    def processar_e_salvar(
        self,
        cliente: Cliente,
        itens_dados: list[dict],
        catalogo_produtos: dict[str, Produto],
    ) -> Pedido:
        """Cria e persiste um pedido."""
        pedido = self.criar_pedido(cliente, itens_dados, catalogo_produtos)
        self._repository.salvar(pedido)
        return pedido

    def buscar_pedidos_cliente(self, cnpj: str) -> list[Pedido]:
        """Retorna histórico de pedidos de um cliente pelo CNPJ."""
        return self._repository.buscar_por_cliente(cnpj)
