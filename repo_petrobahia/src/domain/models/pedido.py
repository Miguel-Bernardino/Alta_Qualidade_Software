from dataclasses import dataclass, field

from src.domain.models.cliente import Cliente

from .item_pedido import ItemPedido


@dataclass
class Pedido:
    cliente: Cliente
    itens: list[ItemPedido] = field(default_factory=list)

    @property
    def preco_total(self) -> float:
        return sum(item.preco_final for item in self.itens)
