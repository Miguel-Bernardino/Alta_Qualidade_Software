from dataclasses import dataclass


@dataclass
class Cliente:
    email: str
    nome: str
    cnpj: str

    def __post_init__(self):
        if not self.nome:
            raise ValueError("Nome não pode ser vazio.")
