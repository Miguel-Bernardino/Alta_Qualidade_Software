from .politica_desconto import PoliticaDesconto


class PoliticaDescontoProdutoEtanol(PoliticaDesconto):
    """Desconto simples para etanol acima de 80 unidades."""

    def calcular_desconto(self, item):
        if item.quantidade > 80:
            return item.preco_unitario * item.quantidade * 0.03
        return 0.0
