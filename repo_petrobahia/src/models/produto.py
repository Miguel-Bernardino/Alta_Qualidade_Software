from dataclasses import dataclass
from typing import Optional

from persistence.produtos_persistencia import ProdutosPersistencia


@dataclass
class Produto:
    tipo: str
    preco_base_unitario: float = 0.0

    @classmethod
    def from_tipo(cls, tipo: str, persistencia: ProdutosPersistencia) -> "Produto":
        preco_unitario = persistencia.obter_preco_base(tipo)
        return cls(tipo=tipo, preco_base_unitario=preco_unitario)

    def calcular_preco_para_qtd(self, qtd: int) -> float:
        """Calcula preço bruto (sem cupons nem arredondamento final)
        com as regras de desconto por quantidade para cada tipo.
        - diesel: descontos por faixa
        - gasolina: desconto absoluto se qtd > 200
        - etanol: desconto percentual se qtd > 80
        - lubrificante: soma simples (poderia ter desconto em volume)
        """
        tipo = self.tipo
        base = self.preco_base_unitario
        if tipo == "diesel":
            total = base * qtd
            if qtd > 1000:
                total *= 0.9
            elif qtd > 500:
                total *= 0.95
            return total
        if tipo == "gasolina":
            total = base * qtd
            if qtd > 200:
                total -= 100
            return total
        if tipo == "etanol":
            total = base * qtd
            if qtd > 80:
                total *= 0.97
            return total
        if tipo == "lubrificante":
            # implementação simples: multiplicação direta
            return base * qtd
        # desconhecido
        return 0.0
