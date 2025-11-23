from dataclasses import dataclass, field

from src.domain.models.produto import Produto
from src.domain.services.cupom_service import Cupom, CupomNulo


@dataclass
class ItemPedido:
    """Representa um item dentro de um pedido.

    Responsável por consolidar valores e aplicar descontos.
    Utiliza Strategy Pattern para políticas de desconto e cupons.
    """

    produto: Produto
    quantidade: int
    cupom: Cupom = field(default_factory=CupomNulo)

    preco_unitario: float = field(init=False)
    preco_bruto: float = field(init=False)
    desconto_produto: float = field(init=False)
    desconto_cupom: float = field(init=False)
    preco_final: float = field(init=False)

    def __post_init__(self):
        if self.quantidade <= 0:
            raise ValueError("Quantidade deve ser positiva.")
        self.preco_unitario = self.produto.preco
        self.preco_bruto = self.preco_unitario * self.quantidade

        self.desconto_produto = self.produto.politica_desconto.calcular_desconto(self)
        self.desconto_cupom = self.cupom.calcular_desconto(self.preco_bruto, self.produto.tipo)

        self.preco_final = max(self.preco_bruto - self.desconto_produto - self.desconto_cupom, 0.0)
