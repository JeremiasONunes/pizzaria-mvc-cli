from typing import Dict, List, Optional, Tuple

from models.pagamento import Pagamento
from models.pedido import Pedido
from controllers.pedido_controller import PedidoController


class PagamentoController:
    def __init__(self, pedido_ctrl: PedidoController):
        self._pagamentos: List[Pagamento] = []
        self._proximo_id = 1
        self._pedido_ctrl = pedido_ctrl
        self._carregar()

    def _carregar(self):
        from models.database import Database
        dados = Database.carregar()
        for pg in dados.get("pagamentos", []):
            self._pagamentos.append(
                Pagamento(pg["id"], pg["pedido_id"], pg["valor"], pg["metodo"])
            )
        self._proximo_id = dados.get("contadores", {}).get("pagamento", 1)

    def _salvar(self):
        from models.database import Database
        dados = Database.carregar()
        dados["pagamentos"] = [
            {
                "id": pg.id,
                "pedido_id": pg.pedido_id,
                "valor": pg.valor,
                "metodo": pg.metodo,
            }
            for pg in self._pagamentos
        ]
        dados["contadores"]["pagamento"] = self._proximo_id
        Database.salvar(dados)

    def processar(
        self, pedido_id: int, metodo: str
    ) -> Tuple[Optional[Pagamento], Optional[str]]:
        pedido = self._pedido_ctrl.buscar_por_id(pedido_id)
        if not pedido:
            return None, "Pedido nao encontrado."
        if pedido.esta_pago():
            return None, "Pedido ja foi pago."
        if not pedido.itens:
            return None, "Pedido sem itens."
        if metodo not in Pagamento.METODOS_ACEITOS:
            opcoes = ", ".join(Pagamento.METODOS_ACEITOS)
            return None, f"Metodo invalido. Opcoes: {opcoes}"
        # Encerra o pedido caso ainda esteja aberto
        if pedido.esta_aberto():
            pedido.fechar()
        pagamento = Pagamento(self._proximo_id, pedido_id, pedido.total, metodo)
        self._pagamentos.append(pagamento)
        self._proximo_id += 1
        self._pedido_ctrl.marcar_pago(pedido_id)
        self._salvar()
        return pagamento, None

    def fechamento_do_dia(self) -> Dict:
        pagos = self._pedido_ctrl.listar_pagos()
        faturamento = sum(p.total for p in pagos)
        return {
            "total_pedidos_pagos": len(pagos),
            "faturamento_total": faturamento,
            "pagamentos": list(self._pagamentos),
        }

    def listar(self) -> List[Pagamento]:
        return list(self._pagamentos)
