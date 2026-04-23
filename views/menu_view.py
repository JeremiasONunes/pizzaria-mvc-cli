from views.cliente_view import ClienteView
from views.mesa_view import MesaView
from views.pagamento_view import PagamentoView
from views.pedido_view import PedidoView
from views.produto_view import ProdutoView


class MenuView:
    def __init__(
        self,
        cliente_view: ClienteView,
        produto_view: ProdutoView,
        mesa_view: MesaView,
        pedido_view: PedidoView,
        pagamento_view: PagamentoView,
    ):
        self._cliente_view = cliente_view
        self._produto_view = produto_view
        self._mesa_view = mesa_view
        self._pedido_view = pedido_view
        self._pagamento_view = pagamento_view

    def executar(self):
        print("\n==========================================")
        print("    SISTEMA DE GERENCIAMENTO DE PIZZARIA")
        print("==========================================")
        while True:
            print("\n--- MENU PRINCIPAL ---")
            print("1 - Gerenciar Clientes")
            print("2 - Gerenciar Produtos e Estoque")
            print("3 - Gerenciar Mesas")
            print("4 - Gerenciar Pedidos")
            print("5 - Pagamento")
            print("0 - Sair")
            opcao = input("Opcao: ").strip()
            if opcao == "1":
                self._cliente_view.exibir_menu()
            elif opcao == "2":
                self._produto_view.exibir_menu()
            elif opcao == "3":
                self._mesa_view.exibir_menu()
            elif opcao == "4":
                self._pedido_view.exibir_menu()
            elif opcao == "5":
                self._pagamento_view.exibir_menu()
            elif opcao == "0":
                print("\nSistema encerrado. Ate logo.")
                break
            else:
                print("Opcao invalida.")
