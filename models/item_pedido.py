class ItemPedido:
    def __init__(
        self,
        id_item: int,
        pedido_id: int,
        produto_id: int,
        nome_produto: str,
        preco_unitario: float,
        quantidade: int,
    ):
        self._id = id_item
        self._pedido_id = pedido_id
        self._produto_id = produto_id
        self._nome_produto = nome_produto
        self._preco_unitario = preco_unitario
        self._quantidade = quantidade
        self._subtotal = preco_unitario * quantidade
    @property
    def id(self) -> int:
        return self._id
    @property
    def pedido_id(self) -> int:
        return self._pedido_id
    @property
    def produto_id(self) -> int:
        return self._produto_id
    @property
    def nome_produto(self) -> str:
        return self._nome_produto
    @property
    def preco_unitario(self) -> float:
        return self._preco_unitario
    @property
    def quantidade(self) -> int:
        return self._quantidade
    @property
    def subtotal(self) -> float:
        return self._subtotal
    def __str__(self) -> str:
        return (
            f"  {self._nome_produto} x{self._quantidade}"
            f" @ R$ {self._preco_unitario:.2f} = R$ {self._subtotal:.2f}"
        )
