from typing import List, Optional, Tuple

from models.database import Database
from models.mesa import Mesa


class MesaController:
    def __init__(self):
        self._mesas: List[Mesa] = []
        self._proximo_id = 1
        self._carregar()

    def _carregar(self):
        dados = Database.carregar()
        for d in dados.get("mesas", []):
            mesa = Mesa(d["id"], d["numero"])
            if d["status"] == Mesa.STATUS_OCUPADA:
                mesa.ocupar()
            self._mesas.append(mesa)
        self._proximo_id = dados.get("contadores", {}).get("mesa", 1)

    def _salvar(self):
        dados = Database.carregar()
        dados["mesas"] = [
            {"id": m.id, "numero": m.numero, "status": m.status}
            for m in self._mesas
        ]
        dados["contadores"]["mesa"] = self._proximo_id
        Database.salvar(dados)

    def cadastrar(self, numero: int) -> Tuple[Optional[Mesa], Optional[str]]:
        for m in self._mesas:
            if m.numero == numero:
                return None, f"Mesa numero {numero} ja cadastrada."
        mesa = Mesa(self._proximo_id, numero)
        self._mesas.append(mesa)
        self._proximo_id += 1
        self._salvar()
        return mesa, None

    def listar(self) -> List[Mesa]:
        return list(self._mesas)

    def listar_livres(self) -> List[Mesa]:
        return [m for m in self._mesas if m.esta_livre()]

    def buscar_por_id(self, id_mesa: int) -> Optional[Mesa]:
        for m in self._mesas:
            if m.id == id_mesa:
                return m
        return None

    def ocupar(self, id_mesa: int) -> bool:
        mesa = self.buscar_por_id(id_mesa)
        if mesa and mesa.esta_livre():
            mesa.ocupar()
            self._salvar()
            return True
        return False

    def liberar(self, id_mesa: int) -> bool:
        mesa = self.buscar_por_id(id_mesa)
        if mesa:
            mesa.liberar()
            self._salvar()
            return True
        return False
