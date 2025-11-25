from .politica_desconto import PoliticaDesconto


class PoliticaDescontoProdutoGasolina(PoliticaDesconto):
    """Desconto fixo para grandes quantidades de gasolina."""

    def calcular_desconto(self, item):
        if item.quantidade > 200:
            return 100.0
        return 0.0
