from typing import Dict, List, Optional, Tuple

from models.database import Database
from models.estoque import Estoque


class EstoqueController:
    def __init__(self):
        self._estoques: Dict[int, Estoque] = {}
        self._carregar()

    def _carregar(self):
        dados = Database.carregar()
        for ed in dados.get("estoques", {}).values():
            pid = ed["produto_id"]
            self._estoques[pid] = Estoque(pid, ed["quantidade"])

    def _salvar(self):
        dados = Database.carregar()
        dados["estoques"] = {
            str(e.produto_id): {"produto_id": e.produto_id, "quantidade": e.quantidade}
            for e in self._estoques.values()
        }
        Database.salvar(dados)

    def inicializar(self, produto_id: int, quantidade: int):
        self._estoques[produto_id] = Estoque(produto_id, quantidade)
        self._salvar()

    def adicionar(self, produto_id: int, quantidade: int) -> Tuple[bool, Optional[str]]:
        if produto_id not in self._estoques:
            return False, "Produto sem registro de estoque."
        if quantidade <= 0:
            return False, "Quantidade deve ser maior que zero."
        self._estoques[produto_id].adicionar(quantidade)
        self._salvar()
        return True, None

    def remover(self, produto_id: int, quantidade: int) -> bool:
        if produto_id not in self._estoques:
            return False
        resultado = self._estoques[produto_id].remover(quantidade)
        if resultado:
            self._salvar()
        return resultado

    def verificar_disponibilidade(self, produto_id: int, quantidade: int) -> bool:
        if produto_id not in self._estoques:
            return False
        return self._estoques[produto_id].tem_disponivel(quantidade)

    def obter(self, produto_id: int) -> Optional[Estoque]:
        return self._estoques.get(produto_id)

    def listar(self) -> List[Estoque]:
        return list(self._estoques.values())
