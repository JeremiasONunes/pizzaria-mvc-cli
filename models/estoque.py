class Estoque:
    def __init__(self, produto_id: int, quantidade: int):
        self._produto_id = produto_id
        self._quantidade = quantidade
    @property
    def produto_id(self) -> int:
        return self._produto_id
    @property
    def quantidade(self) -> int:
        return self._quantidade
    def adicionar(self, qtd: int):
        if qtd > 0:
            self._quantidade += qtd
    def remover(self, qtd: int) -> bool:
        if qtd > self._quantidade:
            return False
        self._quantidade -= qtd
        return True
    def tem_disponivel(self, qtd: int) -> bool:
        return self._quantidade >= qtd
    def __str__(self) -> str:
        return f"Produto ID {self._produto_id} | Estoque: {self._quantidade}"
