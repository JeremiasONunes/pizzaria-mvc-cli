from controllers.cliente_controller import ClienteController
from controllers.estoque_controller import EstoqueController
from controllers.mesa_controller import MesaController
from controllers.pagamento_controller import PagamentoController
from controllers.pedido_controller import PedidoController
from controllers.produto_controller import ProdutoController
from views.cliente_view import ClienteView
from views.menu_view import MenuView
from views.mesa_view import MesaView
from views.pagamento_view import PagamentoView
from views.pedido_view import PedidoView
from views.produto_view import ProdutoView


def main():
    # Instancia os controllers com injecao de dependencia
    cliente_ctrl = ClienteController()
    produto_ctrl = ProdutoController()
    estoque_ctrl = EstoqueController()
    mesa_ctrl = MesaController()
    pedido_ctrl = PedidoController(mesa_ctrl, produto_ctrl, estoque_ctrl)
    pagamento_ctrl = PagamentoController(pedido_ctrl)

    # Instancia as views passando os controllers necessarios
    cliente_view = ClienteView(cliente_ctrl)
    produto_view = ProdutoView(produto_ctrl, estoque_ctrl)
    mesa_view = MesaView(mesa_ctrl)
    pedido_view = PedidoView(pedido_ctrl, cliente_ctrl, mesa_ctrl)
    pagamento_view = PagamentoView(pagamento_ctrl, pedido_ctrl)

    # Inicia o menu principal
    menu = MenuView(cliente_view, produto_view, mesa_view, pedido_view, pagamento_view)
    menu.executar()


if __name__ == "__main__":
    main()
