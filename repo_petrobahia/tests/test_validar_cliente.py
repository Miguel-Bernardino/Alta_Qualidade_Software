"""Testes unitários para validação de clientes usando unittest."""

import unittest

from src.domain.exceptions import ValidationError
from src.domain.services.validar_cliente import ClienteValidator


class TestClienteValidator(unittest.TestCase):
    """Testes para ClienteValidator."""

    def test_validar_email_valido(self):
        """Deve aceitar email válido."""
        try:
            ClienteValidator.validar_email("teste@empresa.com")
        except ValidationError:
            self.fail("Email válido não deveria lançar exceção")

    def test_validar_email_invalido_sem_arroba(self):
        """Deve rejeitar email sem @."""
        with self.assertRaises(ValidationError):
            ClienteValidator.validar_email("testeempresa.com")

    def test_validar_email_invalido_sem_dominio(self):
        """Deve rejeitar email sem domínio."""
        with self.assertRaises(ValidationError):
            ClienteValidator.validar_email("teste@")

    def test_validar_email_vazio(self):
        """Deve rejeitar email vazio."""
        with self.assertRaises(ValidationError):
            ClienteValidator.validar_email("")

    def test_validar_cnpj_valido(self):
        """Deve aceitar CNPJ não vazio."""
        try:
            ClienteValidator.validar_cnpj("12.345.678/0001-90")
        except ValidationError:
            self.fail("CNPJ válido não deveria lançar exceção")

    def test_validar_cnpj_vazio(self):
        """Deve rejeitar CNPJ vazio."""
        with self.assertRaises(ValidationError):
            ClienteValidator.validar_cnpj("")

    def test_validar_cnpj_none(self):
        """Deve rejeitar CNPJ None."""
        with self.assertRaises(ValidationError):
            ClienteValidator.validar_cnpj(None)


if __name__ == "__main__":
    unittest.main()
