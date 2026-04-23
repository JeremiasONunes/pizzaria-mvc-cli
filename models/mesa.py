class Mesa:
    STATUS_LIVRE = "livre"
    STATUS_OCUPADA = "ocupada"
    def __init__(self, id_mesa: int, numero: int):
        self._id = id_mesa
        self._numero = numero
        self._status = Mesa.STATUS_LIVRE
    @property
    def id(self) -> int:
        return self._id
    @property
    def numero(self) -> int:
        return self._numero
    @property
    def status(self) -> str:
        return self._status
    def ocupar(self):
        self._status = Mesa.STATUS_OCUPADA
    def liberar(self):
        self._status = Mesa.STATUS_LIVRE
    def esta_livre(self) -> bool:
        return self._status == Mesa.STATUS_LIVRE
    def __str__(self) -> str:
        return f"[{self._id}] Mesa {self._numero} | Status: {self._status}"
