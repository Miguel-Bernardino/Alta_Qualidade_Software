"""Validações de regras de negócio para Pedido."""

from src.domain.exceptions import ValidationError
from src.domain.models.pedido import Pedido


class ValidadorPedido:
    """Domain Service para validar regras de negócio de Pedido.

    Mantém validações que não pertencem à entidade Pedido.
    """

    QUANTIDADE_MINIMA_ITENS = 1

    @classmethod
    def validar(cls, pedido: Pedido) -> None:
        """Valida regras de negócio do pedido.

        Raises:
            ValidationError: Se alguma regra for violada
        """
        cls._validar_cliente(pedido)
        cls._validar_itens(pedido)

    @classmethod
    def _validar_cliente(cls, pedido: Pedido) -> None:
        if not pedido.cliente:
            raise ValidationError("Pedido deve ter um cliente informado.")

    @classmethod
    def _validar_itens(cls, pedido: Pedido) -> None:
        if len(pedido.itens) < cls.QUANTIDADE_MINIMA_ITENS:
            raise ValidationError(
                f"Pedido deve ter no mínimo {cls.QUANTIDADE_MINIMA_ITENS} item(ns)."
            )
