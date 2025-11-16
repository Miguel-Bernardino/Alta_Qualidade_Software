"""
Ponto de entrada do processamento PetroBahia.
Aplica validações, escreve o arquivo clientes.txt com schema,
registra clientes e processa pedidos usando serviços de domínio.
"""

from models.cliente import Cliente
from persistence.produtos_persistencia import ProdutosPersistencia
from repositories.cliente_repository import TxtClienteRepository
from services.pedido_service import PedidoService

CLIENTES_FILE = "clientes.txt"


def garantir_schema_clientes(caminho: str):
    """Garante que o arquivo de clientes exista e contenha um cabeçalho com a 'tabela'."""
    header = (
        "# Tabela: clientes\n"
        "# colunas: nome, email, cnpj\n"
        "# formato por linha: JSON\n"
    )
    try:
        # cria arquivo com header apenas se não existir
        with open(caminho, "x", encoding="utf-8") as fh:
            fh.write(header + "\n")
    except FileExistsError:
        # já existe: não sobrescreve
        pass


def main():
    garantir_schema_clientes(CLIENTES_FILE)

    cliente_repo = TxtClienteRepository(CLIENTES_FILE)
    produtos_repo = ProdutosPersistencia()  # fonte de preços e regras
    pedido_service = PedidoService(produtos_repo)

    clientes = [
        Cliente(nome="Ana Paula", email="ana@@petrobahia", cnpj="123"),
        Cliente(nome="Carlos", email="carlos@petrobahia.com", cnpj="456"),
    ]

    pedidos = [
        {"cliente": "TransLog", "produto": "diesel", "qtd": 1200, "cupom": "MEGA10"},
        {"cliente": "MoveMais", "produto": "gasolina", "qtd": 300, "cupom": None},
        {"cliente": "EcoFrota", "produto": "etanol", "qtd": 50, "cupom": "NOVO5"},
        {"cliente": "PetroPark", "produto": "lubrificante", "qtd": 12, "cupom": "LUB2"},
    ]

    print("==== Início processamento PetroBahia ====")

    for c in clientes:
        ok = cliente_repo.cadastrar(c)
        if ok:
            print("cliente ok:", c.nome)
        else:
            print("cliente com problema:", c)

    valores = []
    for p in pedidos:
        try:
            v = pedido_service.processar_pedido(p)
            valores.append(v)
            print("pedido:", p, "-- valor final:", v)
        except Exception as e:
            print("erro ao processar pedido", p, "->", e)
            valores.append(0)

    print("TOTAL =", sum(valores))
    print("==== Fim processamento PetroBahia ====")


if __name__ == "__main__":
    main()
