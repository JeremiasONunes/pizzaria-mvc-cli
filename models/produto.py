class Produto:
    def __init__(self, id_produto: int, nome: str, preco: float, categoria: str):
        self._id = id_produto
        self._nome = nome
        self._preco = preco
        self._categoria = categoria
    @property
    def id(self) -> int:
        return self._id
    @property
    def nome(self) -> str:
        return self._nome
    @nome.setter
    def nome(self, valor: str):
        self._nome = valor
    @property
    def preco(self) -> float:
        return self._preco
    @preco.setter
    def preco(self, valor: float):
        self._preco = valor
    @property
    def categoria(self) -> str:
        return self._categoria
    @categoria.setter
    def categoria(self, valor: str):
        self._categoria = valor

    def __str__(self) -> str:
        return f"[{self._id}] {self._nome} | R$ {self._preco:.2f} | {self._categoria}"
