from typing import List, Optional, Tuple

from models.cliente import Cliente
from models.database import Database


class ClienteController:
    def __init__(self):
        self._clientes: List[Cliente] = []
        self._proximo_id = 1
        self._carregar()

    def _carregar(self):
        dados = Database.carregar()
        for d in dados.get("clientes", []):
            self._clientes.append(Cliente(d["id"], d["nome"], d["telefone"]))
        self._proximo_id = dados.get("contadores", {}).get("cliente", 1)

    def _salvar(self):
        dados = Database.carregar()
        dados["clientes"] = [
            {"id": c.id, "nome": c.nome, "telefone": c.telefone}
            for c in self._clientes
        ]
        dados["contadores"]["cliente"] = self._proximo_id
        Database.salvar(dados)

    def cadastrar(self, nome: str, telefone: str) -> Tuple[Optional[Cliente], Optional[str]]:
        nome = nome.strip()
        if not nome:
            return None, "Nome nao pode ser vazio."
        cliente = Cliente(self._proximo_id, nome, telefone.strip())
        self._clientes.append(cliente)
        self._proximo_id += 1
        self._salvar()
        return cliente, None

    def listar(self) -> List[Cliente]:
        return list(self._clientes)

    def buscar_por_id(self, id_cliente: int) -> Optional[Cliente]:
        for c in self._clientes:
            if c.id == id_cliente:
                return c
        return None

    def buscar_por_nome(self, nome: str) -> List[Cliente]:
        termo = nome.lower()
        return [c for c in self._clientes if termo in c.nome.lower()]
