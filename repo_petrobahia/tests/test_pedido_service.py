from persistence.produtos_persistencia import ProdutosPersistencia
from services.pedido_service import PedidoService


def test_processar_pedidos_basicos():
    persist = ProdutosPersistencia()
    service = PedidoService(persist)

    pedidos = [
        (
            {
                "cliente": "TransLog",
                "produto": "diesel",
                "qtd": 1200,
                "cupom": "MEGA10",
            },
            3878.0,
        ),
        (
            {"cliente": "MoveMais", "produto": "gasolina", "qtd": 300, "cupom": None},
            1457.0,
        ),
        (
            {"cliente": "EcoFrota", "produto": "etanol", "qtd": 50, "cupom": "NOVO5"},
            170.52,
        ),
        (
            {
                "cliente": "PetroPark",
                "produto": "lubrificante",
                "qtd": 12,
                "cupom": "LUB2",
            },
            298.0,
        ),
    ]

    for pedido_dict, esperado in pedidos:
        valor = service.processar_pedido(pedido_dict)
        # comparar com aproximação aceitável para floats
        assert round(valor, 2) == round(esperado, 2)
