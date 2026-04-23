class Pagamento:
    METODOS_ACEITOS = ["dinheiro", "cartao_credito", "cartao_debito", "pix"]
    def __init__(self, id_pagamento: int, pedido_id: int, valor: float, metodo: str):
        self._id = id_pagamento
        self._pedido_id = pedido_id
        self._valor = valor
        self._metodo = metodo
    @property
    def id(self) -> int:
        return self._id
    @property
    def pedido_id(self) -> int:
        return self._pedido_id
    @property
    def valor(self) -> float:
        return self._valor
    @property
    def metodo(self) -> str:
        return self._metodo
    def __str__(self) -> str:
        return (
            f"[{self._id}] Pedido {self._pedido_id}"
            f" | R$ {self._valor:.2f} | {self._metodo}"
        )
