from typing import List, Optional, Tuple

from models.database import Database
from models.produto import Produto


class ProdutoController:
    def __init__(self):
        self._produtos: List[Produto] = []
        self._proximo_id = 1
        self._carregar()

    def _carregar(self):
        dados = Database.carregar()
        for d in dados.get("produtos", []):
            self._produtos.append(Produto(d["id"], d["nome"], d["preco"], d["categoria"]))
        self._proximo_id = dados.get("contadores", {}).get("produto", 1)

    def _salvar(self):
        dados = Database.carregar()
        dados["produtos"] = [
            {"id": p.id, "nome": p.nome, "preco": p.preco, "categoria": p.categoria}
            for p in self._produtos
        ]
        dados["contadores"]["produto"] = self._proximo_id
        Database.salvar(dados)

    def cadastrar(
        self, nome: str, preco: float, categoria: str
    ) -> Tuple[Optional[Produto], Optional[str]]:
        nome = nome.strip()
        if not nome:
            return None, "Nome nao pode ser vazio."
        if preco <= 0:
            return None, "Preco deve ser maior que zero."
        produto = Produto(self._proximo_id, nome, preco, categoria.strip())
        self._produtos.append(produto)
        self._proximo_id += 1
        self._salvar()
        return produto, None

    def listar(self) -> List[Produto]:
        return list(self._produtos)

    def buscar_por_id(self, id_produto: int) -> Optional[Produto]:
        for p in self._produtos:
            if p.id == id_produto:
                return p
        return None
