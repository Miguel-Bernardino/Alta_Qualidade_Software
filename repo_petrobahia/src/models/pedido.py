from dataclasses import dataclass, field
from typing import Optional

from models.produto import Produto


@dataclass
class Pedido:
    cliente: str
    produto_tipo: str
    qtd: int
    cupom: Optional[str] = None
    preco_bruto: float = field(default=0.0)
    preco_final: float = field(default=0.0)

    def atribuir_preco_bruto(self, produto: Produto):
        """Atribui ao pedido o preço bruto calculado a partir do produto."""
        self.preco_bruto = produto.calcular_preco_para_qtd(self.qtd)

    def aplicar_cupom(self, cupom_func):
        """Aplica função de cupom (mutates preco_final)."""
        self.preco_final = cupom_func(self.preco_bruto)

    def arredondar_preco(self):
        """
        Aplica a regra de arredondamento final dependendo do tipo do produto:
        - diesel: arredonda para 0 casas
        - gasolina: 2 casas
        - outros: trunca para 2 casas sem arredondar (comportamento original)
        """
        if self.produto_tipo == "diesel":
            self.preco_final = round(self.preco_final, 0)
        elif self.produto_tipo == "gasolina":
            self.preco_final = round(self.preco_final, 2)
        else:
            # truncar para 2 casas (comportamento anterior: int(preco*100)/100.0)
            self.preco_final = float(int(self.preco_final * 100) / 100.0)
