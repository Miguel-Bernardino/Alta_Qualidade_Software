from .politica_desconto import PoliticaDesconto


class PoliticaDescontoProdutoDisel(PoliticaDesconto):
    """Descontos progressivos para Diesel."""

    def calcular_desconto(self, item):
        if item.quantidade > 1000:
            return item.preco_unitario * item.quantidade * 0.10
        if item.quantidade > 500:
            return item.preco_unitario * item.quantidade * 0.05
        return 0.0
