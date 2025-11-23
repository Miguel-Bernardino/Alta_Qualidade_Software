from abc import ABC, abstractmethod


class PoliticaDesconto(ABC):
    """Strategy para cálculo de desconto de produtos.

    Cada implementação decide o valor de desconto sobre um ItemPedido.
    """

    @abstractmethod
    def calcular_desconto(self, item) -> float:  # item: ItemPedido (evita import circular)
        """Retorna o valor de desconto para o item informado."""
        raise NotImplementedError
