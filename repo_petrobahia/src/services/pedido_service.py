from typing import Callable, Dict, List, Optional, Tuple
from persistence.produtos_persistencia import ProdutosPersistencia
from models.produto import Produto
from models.pedido import Pedido

class PrecoNegativoError(Exception):
"""Erro lançado quando o cálculo do preço gera valor negativo indevido."""
pass

class PedidoService:
def init(self, produtos_persistencia: ProdutosPersistencia):
self.produtos_persistencia = produtos_persistencia
# lista de cupons: (nome, função que recebe preco_base e devolve preco_modificado)
self.cupons: List[Tuple[Optional[str], Callable[[float], float]]] = [
("MEGA10", lambda p: p - (p * 0.10)),
("NOVO5", lambda p: p - (p * 0.05)),
# cupom que subtrai valor fixo de 2 quando produto é lubrificante
("LUB2", lambda p, prod_tipo=None: p - 2 if prod_tipo == "lubrificante" else p),
]

def _aplicar_cupom(self, preco: float, cupom: Optional[str], prod_tipo: str) -> float:
    if not cupom:
        return preco
    for nome, func in self.cupons:
        if nome == cupom:
            # alguns cupons precisam do tipo de produto (LUB2)
            try:
                # detecta se func aceita 1 ou 2 argumentos
                import inspect
                params = len(inspect.signature(func).parameters)
                if params == 2:
                    return func(preco, prod_tipo)
                else:
                    return func(preco)
            except Exception:
                # fallback: tenta chamar com só preco
                return func(preco)
    return preco

def processar_pedido(self, p: Dict) -> float:
    """
    Processa um pedido (estrutura dict esperada com chaves: cliente, produto, qtd, cupom).
    Retorna o preço final.
    Pode lançar PrecoNegativoError caso preco calculado inicialmente seja negativo.
    """
    prod_tipo = p.get("produto")
    qtd = p.get("qtd", 0)
    cupom = p.get("cupom")

    if qtd == 0:
        print("qtd zero, retornando 0")
        return 0.0

    # construir model Produto
    produto = Produto.from_tipo(prod_tipo, self.produtos_persistencia)

    # construir pedido
    pedido = Pedido(
        cliente=p.get("cliente"),
        produto_tipo=prod_tipo,
        qtd=qtd,
        cupom=cupom,
    )

    # calcular preco bruto a partir do produto
    pedido.atribuir_preco_bruto(produto)

    if pedido.preco_bruto < 0:
        # Antes: preco = 0 silenciosamente. Agora lançamos exceção para sinalizar erro.
        raise PrecoNegativoError(f"Preço bruto negativo para pedido: {pedido.preco_bruto}")

    # Aplicar cupom
    preco_com_cupom = self._aplicar_cupom(pedido.preco_bruto, cupom, prod_tipo)
    # set preco_final (antes do arredondamento)
    pedido.preco_final = preco_com_cupom

    # delega arredondamento / truncamento à classe Pedido
    pedido.arredondar_preco()

    print("pedido ok:", pedido.cliente, prod_tipo, qtd, "=>", pedido.preco_final)
    return pedido.preco_final