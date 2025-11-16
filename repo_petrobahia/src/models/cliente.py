import re
from dataclasses import dataclass

EMAIL_REGEX = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


@dataclass
class Cliente:
    nome: str
    email: str
    cnpj: str

    def validar(self) -> bool:
        """
        Valida presença de campos e formato de email.
        Retorna True se estiver ok, False se faltar campo.
        """
        if not self.nome or not self.email:
            return False
        return True

    def email_valido(self) -> bool:
        return re.match(EMAIL_REGEX, self.email) is not None
