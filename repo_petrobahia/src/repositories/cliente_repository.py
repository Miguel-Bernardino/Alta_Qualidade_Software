import ast
from pathlib import Path
from typing import Iterable

from src.domain.models.cliente import Cliente
from src.repositories.interfaces.i_cliente_repository import IClienteRepository


class ClienteRepositoryArquivo(IClienteRepository):
    """Persistência simples em arquivo texto (exemplo).

    Formato dict string.
    """

    def __init__(self, caminho_arquivo: str = "clientes.txt"):
        self._path = Path(caminho_arquivo)
        if not self._path.exists():
            self._path.write_text("", encoding="utf-8")

    def salvar(self, cliente: Cliente) -> None:  # type: ignore[override]
        linha = str({"nome": cliente.nome, "email": cliente.email, "cnpj": cliente.cnpj})
        with self._path.open("a", encoding="utf-8") as file:
            file.write(linha + "\n")
        print(f"Cliente salvo: {cliente.cnpj}")

    def listar(self) -> Iterable[Cliente]:
        if not self._path.exists():
            return
        with self._path.open("r", encoding="utf-8") as file:
            for linha in file:
                linha = linha.strip()
                if not linha:
                    continue
                dados = ast.literal_eval(linha)
                yield Cliente(email=dados["email"], nome=dados["nome"], cnpj=dados["cnpj"])
