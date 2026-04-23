import copy
import json
import os

_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db.txt")

_ESTRUTURA_PADRAO = {
    "clientes": [],
    "produtos": [],
    "estoques": {},
    "mesas": [],
    "pedidos": [],
    "pagamentos": [],
    "contadores": {
        "cliente": 1,
        "produto": 1,
        "mesa": 1,
        "pedido": 1,
        "item": 1,
        "pagamento": 1,
    },
}


class Database:
    @staticmethod
    def carregar() -> dict:
        if not os.path.exists(_DB_PATH):
            return copy.deepcopy(_ESTRUTURA_PADRAO)
        try:
            with open(_DB_PATH, "r", encoding="utf-8") as f:
                dados = json.load(f)
            # garante chaves ausentes em arquivos legados
            for chave, valor in _ESTRUTURA_PADRAO.items():
                if chave not in dados:
                    dados[chave] = copy.deepcopy(valor)
            return dados
        except (json.JSONDecodeError, IOError):
            return copy.deepcopy(_ESTRUTURA_PADRAO)

    @staticmethod
    def salvar(dados: dict):
        with open(_DB_PATH, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
