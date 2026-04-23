from controllers.pagamento_controller import PagamentoController
from controllers.pedido_controller import PedidoController
from models.pagamento import Pagamento


class PagamentoView:
    def __init__(
        self,
        pagamento_ctrl: PagamentoController,
        pedido_ctrl: PedidoController,
    ):
        self._pagamento_ctrl = pagamento_ctrl
        self._pedido_ctrl = pedido_ctrl

    def exibir_menu(self):
        while True:
            print("\n--- PAGAMENTO ---")
            print("1 - Realizar pagamento")
            print("2 - Fechamento do dia")
            print("0 - Voltar")
            opcao = input("Opcao: ").strip()
            if opcao == "1":
                self._realizar_pagamento()
            elif opcao == "2":
                self._fechamento_do_dia()
            elif opcao == "0":
                break
            else:
                print("Opcao invalida.")

    def _realizar_pagamento(self):
        todos = self._pedido_ctrl.listar()
        pendentes = [p for p in todos if not p.esta_pago()]
        if not pendentes:
            print("Nenhum pedido pendente de pagamento.")
            return
        print("\n-- Pedidos Pendentes --")
        for p in pendentes:
            print(p)
        try:
            pedido_id = int(input("ID do pedido: ").strip())
        except ValueError:
            print("Erro: ID invalido.")
            return
        pedido = self._pedido_ctrl.buscar_por_id(pedido_id)
        if not pedido:
            print("Pedido nao encontrado.")
            return
        if pedido.esta_pago():
            print("Este pedido ja foi pago.")
            return
        print(f"\nTotal a pagar: R$ {pedido.total:.2f}")
        print("Metodos de pagamento disponíveis:")
        for i, m in enumerate(Pagamento.METODOS_ACEITOS, 1):
            print(f"  {i} - {m}")
        try:
            escolha = int(input("Escolha o metodo (numero): ").strip())
            metodo = Pagamento.METODOS_ACEITOS[escolha - 1]
        except (ValueError, IndexError):
            print("Metodo invalido.")
            return
        pagamento, erro = self._pagamento_ctrl.processar(pedido_id, metodo)
        if erro:
            print(f"Erro: {erro}")
        else:
            print(f"Pagamento realizado: {pagamento}")
            print("Mesa liberada.")

    def _fechamento_do_dia(self):
        relatorio = self._pagamento_ctrl.fechamento_do_dia()
        print("\n" + "=" * 50)
        print("           FECHAMENTO DO DIA")
        print("=" * 50)
        print(f"Total de pedidos pagos:  {relatorio['total_pedidos_pagos']}")
        print(f"Faturamento total:       R$ {relatorio['faturamento_total']:.2f}")
        print("\n-- Detalhamento dos Pagamentos --")
        if not relatorio["pagamentos"]:
            print("  Nenhum pagamento registrado.")
        for pg in relatorio["pagamentos"]:
            print(f"  {pg}")
        print("=" * 50)
