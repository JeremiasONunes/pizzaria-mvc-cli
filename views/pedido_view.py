from controllers.cliente_controller import ClienteController
from controllers.mesa_controller import MesaController
from controllers.pedido_controller import PedidoController
from models.pedido import Pedido


class PedidoView:
    def __init__(
        self,
        pedido_ctrl: PedidoController,
        cliente_ctrl: ClienteController,
        mesa_ctrl: MesaController,
    ):
        self._pedido_ctrl = pedido_ctrl
        self._cliente_ctrl = cliente_ctrl
        self._mesa_ctrl = mesa_ctrl

    def exibir_menu(self):
        while True:
            print("\n--- PEDIDOS ---")
            print("1 - Abrir pedido")
            print("2 - Adicionar item ao pedido")
            print("3 - Ver detalhes do pedido")
            print("4 - Listar pedidos abertos")
            print("5 - Fechar pedido")
            print("0 - Voltar")
            opcao = input("Opcao: ").strip()
            if opcao == "1":
                self._abrir()
            elif opcao == "2":
                self._adicionar_item()
            elif opcao == "3":
                self._ver_detalhes()
            elif opcao == "4":
                self._listar_abertos()
            elif opcao == "5":
                self._fechar()
            elif opcao == "0":
                break
            else:
                print("Opcao invalida.")

    def _abrir(self):
        mesas = self._mesa_ctrl.listar_livres()
        if not mesas:
            print("Nenhuma mesa livre disponivel.")
            return
        print("\n-- Mesas Disponiveis --")
        for m in mesas:
            print(m)
        try:
            mesa_id = int(input("ID da mesa: ").strip())
        except ValueError:
            print("Erro: ID invalido.")
            return
        cliente_id = None
        clientes = self._cliente_ctrl.listar()
        if clientes:
            print("Vincular a um cliente? (s/n): ", end="")
            if input().strip().lower() == "s":
                for c in clientes:
                    print(c)
                try:
                    cid = int(input("ID do cliente: ").strip())
                    if self._cliente_ctrl.buscar_por_id(cid):
                        cliente_id = cid
                    else:
                        print("Cliente nao encontrado. Pedido sem cliente.")
                except ValueError:
                    print("ID invalido. Pedido sem cliente.")
        pedido, erro = self._pedido_ctrl.abrir(mesa_id, cliente_id)
        if erro:
            print(f"Erro: {erro}")
        else:
            print(f"Pedido aberto: {pedido}")

    def _adicionar_item(self):
        abertos = self._pedido_ctrl.listar_abertos()
        if not abertos:
            print("Nenhum pedido aberto.")
            return
        print("\n-- Pedidos Abertos --")
        for p in abertos:
            print(p)
        try:
            pedido_id = int(input("ID do pedido: ").strip())
            produto_id = int(input("ID do produto: ").strip())
            quantidade = int(input("Quantidade: ").strip())
        except ValueError:
            print("Erro: valor invalido.")
            return
        item, erro = self._pedido_ctrl.adicionar_item(pedido_id, produto_id, quantidade)
        if erro:
            print(f"Erro: {erro}")
        else:
            print(f"Item adicionado:{item}")
            pedido = self._pedido_ctrl.buscar_por_id(pedido_id)
            print(f"Total do pedido: R$ {pedido.total:.2f}")

    def _ver_detalhes(self):
        try:
            pedido_id = int(input("ID do pedido: ").strip())
        except ValueError:
            print("Erro: ID invalido.")
            return
        pedido = self._pedido_ctrl.buscar_por_id(pedido_id)
        if not pedido:
            print("Pedido nao encontrado.")
            return
        self._imprimir_pedido(pedido)

    def _listar_abertos(self):
        abertos = self._pedido_ctrl.listar_abertos()
        if not abertos:
            print("Nenhum pedido aberto.")
            return
        print("\n-- Pedidos Abertos --")
        for p in abertos:
            print(p)

    def _fechar(self):
        abertos = self._pedido_ctrl.listar_abertos()
        if not abertos:
            print("Nenhum pedido aberto.")
            return
        for p in abertos:
            print(p)
        try:
            pedido_id = int(input("ID do pedido para fechar: ").strip())
        except ValueError:
            print("Erro: ID invalido.")
            return
        pedido, erro = self._pedido_ctrl.fechar(pedido_id)
        if erro:
            print(f"Erro: {erro}")
        else:
            print(f"Pedido fechado: {pedido}")

    @staticmethod
    def _imprimir_pedido(pedido: Pedido):
        print(f"\n{'=' * 45}")
        print(f" Pedido #{pedido.id} | Mesa {pedido.mesa_id}")
        print(f" Status: {pedido.status}")
        if pedido.cliente_id:
            print(f" Cliente ID: {pedido.cliente_id}")
        print(f"{'=' * 45}")
        print(" Itens:")
        if not pedido.itens:
            print("  (sem itens)")
        for item in pedido.itens:
            print(item)
        print(f"{'=' * 45}")
        print(f" TOTAL: R$ {pedido.total:.2f}")
        print(f"{'=' * 45}")
