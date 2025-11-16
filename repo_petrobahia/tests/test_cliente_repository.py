import json

from models.cliente import Cliente
from repositories.cliente_repository import TxtClienteRepository


def test_cadastrar_cliente_valido(tmp_path):
    arquivo = tmp_path / "clientes_test.txt"
    repo = TxtClienteRepository(str(arquivo))

    c = Cliente(nome="Teste", email="teste@example.com", cnpj="0001")
    ok = repo.cadastrar(c)
    assert ok is True

    # arquivo criado e contém uma linha JSON
    content = arquivo.read_text(encoding="utf-8").strip().splitlines()
    assert len(content) == 1
    registro = json.loads(content[0])
    assert registro["nome"] == "Teste"
    assert registro["email"] == "teste@example.com"


def test_cadastrar_cliente_invalido_nao_grava(tmp_path):
    arquivo = tmp_path / "clientes_test2.txt"
    repo = TxtClienteRepository(str(arquivo))

    c = Cliente(nome="", email="", cnpj="")
    ok = repo.cadastrar(c)
    assert ok is False

    # arquivo pode existir ou não; se existir deve estar vazio (sem linhas adicionais)
    if arquivo.exists():
        content = arquivo.read_text(encoding="utf-8").strip()
        assert content == "" or len(content.splitlines()) == 0
