from .politica_desconto import PoliticaDesconto


class PoliticaDescontoProdutoNone(PoliticaDesconto):
    """Sem desconto definido."""

    def calcular_desconto(self, item):
        return 0.0
