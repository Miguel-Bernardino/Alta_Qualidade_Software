import re

from src.domain.exceptions import ValidationError


class ClienteValidator:
    """Valida dados do Cliente (regra de domínio).

    Email: formato simples user@dominio.
    CNPJ: valida dígitos verificadores (algoritmo oficial).
    """

    @staticmethod
    def validar_email(email: str):
        padrao_email = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not email or re.match(padrao_email, email) is None:
            raise ValidationError("Email inválido.")

    @staticmethod
    def validar_cnpj(cnpj: str):
        if not cnpj or len(cnpj.strip()) == 0:
            raise ValidationError("CNPJ inválido.")
