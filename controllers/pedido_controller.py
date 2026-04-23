from typing import List, Optional, Tuple

from models.item_pedido import ItemPedido
from models.pedido import Pedido
from controllers.estoque_controller import EstoqueController
from controllers.mesa_controller import MesaController
from controllers.produto_controller import ProdutoController


class PedidoController:
    def __init__(
        self,
        mesa_ctrl: MesaController,
        produto_ctrl: ProdutoController,
        estoque_ctrl: EstoqueController,
    ):
        self._pedidos: List[Pedido] = []
        self._proximo_id = 1
        self._proximo_item_id = 1
        self._mesa_ctrl = mesa_ctrl
        self._produto_ctrl = produto_ctrl
        self._estoque_ctrl = estoque_ctrl
        self._carregar()

    def _carregar(self):
        from models.database import Database
        dados = Database.carregar()
        contadores = dados.get("contadores", {})
        self._proximo_id = contadores.get("pedido", 1)
        self._proximo_item_id = contadores.get("item", 1)
        for pd in dados.get("pedidos", []):
            pedido = Pedido(pd["id"], pd["mesa_id"], pd.get("cliente_id"))
            for item_d in pd.get("itens", []):
                item = ItemPedido(
                    item_d["id"],
                    item_d["pedido_id"],
                    item_d["produto_id"],
                    item_d["nome_produto"],
                    item_d["preco_unitario"],
                    item_d["quantidade"],
                )
                pedido.adicionar_item(item)
            status = pd["status"]
            if status == Pedido.STATUS_FECHADO:
                pedido.fechar()
            elif status == Pedido.STATUS_PAGO:
                pedido.marcar_pago()
            self._pedidos.append(pedido)

    def _salvar(self):
        from models.database import Database
        dados = Database.carregar()
        dados["pedidos"] = [
            {
                "id": p.id,
                "mesa_id": p.mesa_id,
                "cliente_id": p.cliente_id,
                "status": p.status,
                "total": p.total,
                "itens": [
                    {
                        "id": i.id,
                        "pedido_id": i.pedido_id,
                        "produto_id": i.produto_id,
                        "nome_produto": i.nome_produto,
                        "preco_unitario": i.preco_unitario,
                        "quantidade": i.quantidade,
                        "subtotal": i.subtotal,
                    }
                    for i in p.itens
                ],
            }
            for p in self._pedidos
        ]
        dados["contadores"]["pedido"] = self._proximo_id
        dados["contadores"]["item"] = self._proximo_item_id
        Database.salvar(dados)

    def abrir(
        self, mesa_id: int, cliente_id: Optional[int] = None
    ) -> Tuple[Optional[Pedido], Optional[str]]:
        mesa = self._mesa_ctrl.buscar_por_id(mesa_id)
        if not mesa:
            return None, "Mesa nao encontrada."
        if not mesa.esta_livre():
            return None, "Mesa esta ocupada."
        pedido = Pedido(self._proximo_id, mesa_id, cliente_id)
        self._pedidos.append(pedido)
        self._proximo_id += 1
        self._mesa_ctrl.ocupar(mesa_id)
        self._salvar()
        return pedido, None

    def adicionar_item(
        self, pedido_id: int, produto_id: int, quantidade: int
    ) -> Tuple[Optional[ItemPedido], Optional[str]]:
        pedido = self.buscar_por_id(pedido_id)
        if not pedido:
            return None, "Pedido nao encontrado."
        if not pedido.esta_aberto():
            return None, "Pedido nao esta aberto."
        if quantidade <= 0:
            return None, "Quantidade deve ser maior que zero."
        produto = self._produto_ctrl.buscar_por_id(produto_id)
        if not produto:
            return None, "Produto nao encontrado."
        if not self._estoque_ctrl.verificar_disponibilidade(produto_id, quantidade):
            estoque = self._estoque_ctrl.obter(produto_id)
            disponivel = estoque.quantidade if estoque else 0
            return None, f"Estoque insuficiente. Disponivel: {disponivel}."
        self._estoque_ctrl.remover(produto_id, quantidade)
        item = ItemPedido(
            self._proximo_item_id,
            pedido_id,
            produto_id,
            produto.nome,
            produto.preco,
            quantidade,
        )
        self._proximo_item_id += 1
        pedido.adicionar_item(item)
        self._salvar()
        return item, None

    def fechar(self, pedido_id: int) -> Tuple[Optional[Pedido], Optional[str]]:
        pedido = self.buscar_por_id(pedido_id)
        if not pedido:
            return None, "Pedido nao encontrado."
        if not pedido.esta_aberto():
            return None, "Pedido nao esta aberto."
        if not pedido.itens:
            return None, "Pedido sem itens. Adicione itens antes de fechar."
        pedido.fechar()
        self._salvar()
        return pedido, None

    def marcar_pago(self, pedido_id: int):
        pedido = self.buscar_por_id(pedido_id)
        if pedido:
            pedido.marcar_pago()
            self._mesa_ctrl.liberar(pedido.mesa_id)
            self._salvar()

    def buscar_por_id(self, id_pedido: int) -> Optional[Pedido]:
        for p in self._pedidos:
            if p.id == id_pedido:
                return p
        return None

    def listar(self) -> List[Pedido]:
        return list(self._pedidos)

    def listar_abertos(self) -> List[Pedido]:
        return [p for p in self._pedidos if p.esta_aberto()]

    def listar_pagos(self) -> List[Pedido]:
        return [p for p in self._pedidos if p.esta_pago()]
