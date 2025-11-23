from abc import ABC, abstractmethod

from src.domain.models.pedido import Pedido


class IPedidoRepository(ABC):
    """Interface para persistência de pedidos."""

    @abstractmethod
    def salvar(self, pedido: Pedido) -> None:
        """Persiste um pedido."""
        raise NotImplementedError

    @abstractmethod
    def buscar_por_cliente(self, cliente: str) -> list[Pedido]:
        """Retorna todos os pedidos de um cliente."""
        raise NotImplementedError
