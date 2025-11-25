"""Sistema simples de notificações (Application Service)."""

from src.domain.models.cliente import Cliente
from src.domain.models.pedido import Pedido


class NotificacaoService:
    """Application Service para notificações simples via console."""

    @staticmethod
    def notificar_cliente_criado(cliente: Cliente) -> None:
        """Notifica sobre novo cliente cadastrado."""
        print(f"✓ Cliente cadastrado: {cliente.nome} ({cliente.email})")

    @staticmethod
    def notificar_pedido_criado(pedido: Pedido) -> None:
        """Notifica sobre novo pedido criado."""
        print(f"✓ Pedido criado para {pedido.cliente.nome}: R$ {pedido.preco_total:.2f}")

    @staticmethod
    def notificar_pedido_valor_alto(pedido: Pedido, limite: float = 5000.0) -> None:
        """Alerta sobre pedido de alto valor."""
        if pedido.preco_total >= limite:
            print(
                f"⚠ ALERTA: Pedido de alto valor - {pedido.cliente.nome}: R$ {pedido.preco_total:.2f}"
            )
