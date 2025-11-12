"""
Fonte de verdade para preços base e regras de variação por produto.
Separado para seguir o princípio de responsabilidade única.
Aqui poderia ser trocado para um DB real sem alterar a lógica de domínio.
"""

from typing import Dict

BASES: Dict[str, float] = {
    "diesel": 3.99,
    "gasolina": 5.19,
    "etanol": 3.59,
    "lubrificante": 25.0,
}

class ProdutosPersistencia:
def init(self):
# no futuro ler de arquivo/DB; por enquanto usa dicionário em memória
self.bases = BASES.copy()

def obter_preco_base(self, tipo: str) -> float:
    return float(self.bases.get(tipo, 0.0))

def listar_produtos(self):