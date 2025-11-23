from typing import Iterable

from src.domain.models.cliente import Cliente
from src.domain.services.validar_cliente import ClienteValidator
from src.repositories.interfaces.i_cliente_repository import IClienteRepository


class ClienteService:
    """Serviço de aplicação para gerenciar clientes.

    Orquestra operações de criação, validação e consulta de clientes.
    """

    def __init__(self, cliente_repository: IClienteRepository):
        self.cliente_repository = cliente_repository

    def criar_cliente(self, email: str, nome: str, cnpj: str) -> Cliente:
        """Cria e persiste um cliente após validações."""
        ClienteValidator.validar_email(email)
        ClienteValidator.validar_cnpj(cnpj)

        cliente = Cliente(email=email, nome=nome, cnpj=cnpj)
        self.cliente_repository.salvar(cliente)
        print(f"Cliente criado: {cnpj}")
        return cliente

    def listar_todos(self) -> Iterable[Cliente]:
        """Retorna todos os clientes cadastrados."""
        return self.cliente_repository.listar()
