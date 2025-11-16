"""
Repositório responsável por persistir clientes em um arquivo texto (JSON por linha).
Interface simples para permitir troca por outro adaptador no futuro.
"""

import json
from typing import Protocol

from models.cliente import Cliente


class ClienteRepository(Protocol):
    def cadastrar(self, cliente: Cliente) -> bool: ...


class TxtClienteRepository:
    def __init__(self, arquivo: str):
        self.arquivo = arquivo

    def cadastrar(self, cliente: Cliente) -> bool:
        """Persiste cliente em formato JSON (uma linha por cliente).
        Retorna True se cadastro aceitável, False caso falte campo.
        Observação: aceita email inválido, mas indica problema com retorno False apenas
        quando faltar campo obrigatório.
        """
        if not cliente.validar():
            print("faltou campo")
            return False

        # grava como JSON para facilitar leitura/consulta posterior
        registro = {"nome": cliente.nome, "email": cliente.email, "cnpj": cliente.cnpj}
        with open(self.arquivo, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(registro, ensure_ascii=False) + "\n")

        # comportamento antigo: enviar email de boas-vindas (simulado)
        if not cliente.email_valido():
            print("email invalido mas vou aceitar assim mesmo")
        print("enviando email de boas vindas para", cliente.email)
        return True
