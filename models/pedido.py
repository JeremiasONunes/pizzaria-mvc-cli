from typing import List, Optional

from models.item_pedido import ItemPedido
class Pedido:
    STATUS_ABERTO = "aberto"
    STATUS_FECHADO = "fechado"
    STATUS_PAGO = "pago"
    def __init__(self, id_pedido: int, mesa_id: int, cliente_id: Optional[int] = None):
        self._id = id_pedido
        self._mesa_id = mesa_id
        self._cliente_id = cliente_id
        self._itens: List[ItemPedido] = []
        self._status = Pedido.STATUS_ABERTO
        self._total = 0.0
    @property
    def id(self) -> int:
        return self._id
    @property
    def mesa_id(self) -> int:
        return self._mesa_id
    @property
    def cliente_id(self) -> Optional[int]:
        return self._cliente_id
    @property
    def itens(self) -> List[ItemPedido]:
        return list(self._itens)
    @property
    def status(self) -> str:
        return self._status
    @property
    def total(self) -> float:
        return self._total
    def adicionar_item(self, item: ItemPedido):
        self._itens.append(item)
        self._recalcular_total()
    def _recalcular_total(self):
        self._total = sum(i.subtotal for i in self._itens)
    def fechar(self):
        self._status = Pedido.STATUS_FECHADO
    def marcar_pago(self):
        self._status = Pedido.STATUS_PAGO
    def esta_aberto(self) -> bool:
        return self._status == Pedido.STATUS_ABERTO
    def esta_pago(self) -> bool:
        return self._status == Pedido.STATUS_PAGO
    def __str__(self) -> str:
        return (
            f"[{self._id}] Mesa {self._mesa_id}"
            f" | Status: {self._status}"
            f" | Total: R$ {self._total:.2f}"
        )
