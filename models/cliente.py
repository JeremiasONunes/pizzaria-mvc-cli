class Cliente:
    def __init__(self, id_cliente: int, nome: str, telefone: str):
        self._id = id_cliente
        self._nome = nome
        self._telefone = telefone
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
    def telefone(self) -> str:
        return self._telefone
    @telefone.setter
    def telefone(self, valor: str):
        self._telefone = valor
    def __str__(self) -> str:
        return f"[{self._id}] {self._nome} | Tel: {self._telefone}"
