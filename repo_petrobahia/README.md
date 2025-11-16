# PetroBahia S.A.

A **PetroBahia S.A.** é uma empresa fictícia do setor de óleo e gás. Seu sistema interno calcula preços de combustíveis, valida clientes e gera relatórios. 
O código está **mal estruturado** e **difícil de manter**. O objetivo é **refatorar** aplicando **PEP8**, **Clean Code** e **princípios SOLID** (SRP e OCP).

## Objetivos
- Melhorar legibilidade e clareza do código
- Extrair funções e classes coesas
- Eliminar duplicações e efeitos colaterais
- Melhorar nomes e modularidade

## Estrutura
```
src/
├── main.py
└── legacy/
    ├── clientes.py
    ├── pedido_service.py
    └── preco_calculadora.py
```

## Instruções
1. Leia o código legado.
2. Liste os problemas encontrados.
3. Refatore sem mudar o comportamento principal.
4. Documente suas **decisões de design** neste README.


## DECISÕES DE DESIGN
Descreva aqui as mudanças feitas e os motivos.

Ferramentas de Qualidade
------------------------

Instalação (ambiente virtual recomendado):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

Uso:

- Formatar código (isort + black):

```bash
./scripts/format.sh
```

- Rodar lint (pylint):

```bash
./scripts/lint.sh
```

Configurações adicionadas:

- `pyproject.toml` — configuração do `black` e `isort`.
- `.pylintrc` — configuração do `pylint` (adiciona `src` ao `PYTHONPATH`).
- `requirements-dev.txt` — dependências de desenvolvimento.
- `scripts/format.sh` e `scripts/lint.sh` — helpers para executar as ferramentas.

Dicas:

- Você pode integrar essas ferramentas em um `pre-commit` ou CI para aplicar automaticamente.
- Ajuste `max-line-length` e outras regras em `pyproject.toml` / `.pylintrc` conforme necessário.

Resultados das ferramentas (execução local)
-----------------------------------------

- **isort**: corrigiu imports em vários arquivos. Exemplo de saída: `Fixing src/main.py`, `Fixing src/services/pedido_service.py`, `Fixing src/repositories/cliente_repository.py`, `Fixing src/models/pedido.py`, `Fixing src/models/cliente.py`, `Fixing src/models/produto.py`, `Fixing tests/test_cliente_repository.py`.

- **Black**: reformatações aplicadas — `7 files reformatted, 4 files left unchanged.` Mensagem final: `All done! ✨ 🍰 ✨`.

- **Pylint**: score obtido — **9.01/10**.
    - Principais avisos gerados:
        - `line-too-long` em `src/main.py` e `src/services/pedido_service.py`.
        - `broad-exception-caught` (captura geral de `Exception`) em `src/main.py` e `src/services/pedido_service.py`.
        - `import-outside-toplevel` (uso de `inspect` dentro de função) em `src/services/pedido_service.py`.
        - `too-many-function-args` apontado para a chamada da lambda do cupom em `src/services/pedido_service.py`.
        - `unused-import` em `src/models/produto.py`.
        - vários `no-else-return` em `src/legacy/preco_calculadora.py`.

Comandos executados:

```bash
chmod +x scripts/*.sh
./scripts/format.sh   # isort + black
./scripts/lint.sh     # pylint src (saída resumida no README)
```

Se desejar, posso aplicar correções automáticas para avisos triviais (quebrar linhas longas, mover `import inspect` para o topo, remover import não utilizado, ajustar a lambda/call) e reexecutar o `pylint` para melhorar o score.

Conformidade SOLID — Mapeamento de Código
----------------------------------------

A seguir estão as partes do código que já demonstram alinhamento com alguns princípios SOLID, junto com uma breve justificativa e o arquivo associado.

- **Single Responsibility (SRP):**
    - **`src/persistence/produtos_persistencia.py`**: classe `ProdutosPersistencia` tem uma responsabilidade clara — fornecer preços base e lista de produtos. Está isolada de lógica de negócio e I/O de apresentação.
    - **`src/models/produto.py`** e **`src/models/pedido.py`**: `Produto` encapsula regras de cálculo por quantidade; `Pedido` encapsula atribuição de preço bruto e lógica de arredondamento. Essas classes cuidam de comportamento relacionado ao seu próprio estado.

- **Open/Closed (OCP):**
    - **`src/repositories/cliente_repository.py`**: existe um `Protocol` `ClienteRepository` (API estreita) e uma implementação `TxtClienteRepository`. Essa separação facilita a extensão por novas implementações (DB, mock) sem mudar o consumidor.

- **Liskov Substitution (LSP):**
    - Uso de `Protocol` para repositórios e o padrão de construção de `Produto`/`Pedido` permite substituir implementações por outras compatíveis (por exemplo, trocar `ProdutosPersistencia` por outra fonte), respeitando o contrato esperado.

- **Interface Segregation (ISP):**
    - `ClienteRepository` expõe uma interface pequena (`cadastrar`) — consumidores não precisam conhecer métodos desnecessários. `ProdutosPersistencia` tem métodos pequenos e específicos (`obter_preco_base`, `listar_produtos`).

- **Dependency Inversion (DIP):**
    - **`src/services/pedido_service.py`**: recebe `produtos_persistencia` no construtor, portanto depende de uma abstração/contrato (embora atualmente tipado para a classe concreta). Isso já permite injeção de dependência em `main.py`.

Observação geral: vários componentes já têm boa separação inicial (models, persistence, services), o que facilita conformidade com SOLID. No entanto, há *áreas que ainda violam* ou podem melhorar (por exemplo: `TxtClienteRepository` mistura persistência com notificação/email; `PedidoService` mantém lista interna de cupons com assinaturas não uniformes). Recomenda-se seguir as melhorias sugeridas na seção "Próximos passos" acima para completar a aderência a SOLID.
