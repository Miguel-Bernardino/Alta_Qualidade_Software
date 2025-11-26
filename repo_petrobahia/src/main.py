from src.application.services.cliente_service import ClienteService
from src.application.services.pedido_service import PedidoService
from src.domain.exceptions import ValidationError
from src.domain.services.produto_factory import ProdutoFactory
from src.repositories.cliente_repository import ClienteRepositoryArquivo
from src.repositories.pedido_repository import PedidoRepositoryArquivo


def executar():

    ########### Setup repositórios e serviços ##############

    cliente_repo = ClienteRepositoryArquivo()
    pedido_repo = PedidoRepositoryArquivo()
    cliente_service = ClienteService(cliente_repo)
    pedido_service = PedidoService(pedido_repo)
    catalogo = ProdutoFactory.criar_catalogo_padrao()

    clientes = [
        {
            "nome": "TransLog",
            "email": "translog@empresa.com",
            "cnpj": "04.252.011/0001-10",
        },
        {
            "nome": "MoveMais",
            "email": "movemais@empresa.com",
            "cnpj": "11.222.333/0001-81",
        },
        {
            "nome": "EcoFrota",
            "email": "ecofrota@empresa.com",
            "cnpj": "12.345.678/0001-90",
        },
        {
            "nome": "PetroPark",
            "email": "petropark@empresa.com",
            "cnpj": "98.765.432/0001-10",
        },
    ]

    print("Início processamento PetroBahia")
    print("\n[1] Cadastrando clientes...")
    clientes_criados = {}
    for client in clientes:
        try:
            cliente = cliente_service.criar_cliente(client["email"], client["nome"], client["cnpj"])
            clientes_criados[client["nome"]] = cliente
            print(f"✓ Cliente salvo: {client['nome']}")
        except ValidationError as e:
            print(f"✗ Falha validação {client['nome']}: {e}")
        except Exception as e:
            print(f"✗ Erro inesperado {client['nome']}: {e}")
    print("\n[2] Criando pedidos...")
    pedidos_dados = [
        {"cliente": "TransLog", "produto": "diesel", "qtd": 1200, "cupom": "MEGA10"},
        {"cliente": "MoveMais", "produto": "gasolina", "qtd": 300, "cupom": None},
        {"cliente": "EcoFrota", "produto": "etanol", "qtd": 50, "cupom": "NOVO5"},
        {"cliente": "PetroPark", "produto": "lubrificante", "qtd": 12, "cupom": "LUB2"},
    ]

    for pedido_dados in pedidos_dados:
        try:
            cliente = clientes_criados.get(pedido_dados["cliente"])
            if not cliente:
                print(f"✗ Cliente '{pedido_dados['cliente']}' não encontrado")
                continue

            itens_dados = [
                {
                    "produto_tipo": pedido_dados["produto"],
                    "quantidade": pedido_dados["qtd"],
                    "cupom_codigo": pedido_dados["cupom"],
                }
            ]

            pedido = pedido_service.processar_e_salvar(cliente, itens_dados, catalogo)
            print(f"✓ Pedido criado para {cliente.nome}: R$ {pedido.preco_total:.2f}")
        except ValidationError as error:
            print(f"✗ Erro validação pedido {pedido_dados['cliente']}: {error}")
        except Exception as error:
            print(f"✗ Erro inesperado pedido {pedido_dados['cliente']}: {error}")

    print("\nFim processamento PetroBahia")

    # Exemplo de leitura
    print("\n[3] Clientes persistidos:")
    for cliente in cliente_repo.listar():
        print(f"- {cliente}")


if __name__ == "__main__":  # pragma: no cover
    executar()
