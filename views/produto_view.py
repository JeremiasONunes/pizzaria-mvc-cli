from controllers.estoque_controller import EstoqueController
from controllers.produto_controller import ProdutoController


class ProdutoView:
    def __init__(self, produto_ctrl: ProdutoController, estoque_ctrl: EstoqueController):
        self._produto_ctrl = produto_ctrl
        self._estoque_ctrl = estoque_ctrl

    def exibir_menu(self):
        while True:
            print("\n--- PRODUTOS E ESTOQUE ---")
            print("1 - Cadastrar produto")
            print("2 - Listar produtos com estoque")
            print("3 - Repor estoque")
            print("0 - Voltar")
            opcao = input("Opcao: ").strip()
            if opcao == "1":
                self._cadastrar()
            elif opcao == "2":
                self._listar()
            elif opcao == "3":
                self._repor_estoque()
            elif opcao == "0":
                break
            else:
                print("Opcao invalida.")

    def _cadastrar(self):
        print("\n-- Cadastro de Produto --")
        nome = input("Nome: ").strip()
        categoria = input("Categoria (pizza/bebida/outro): ").strip()
        try:
            preco = float(input("Preco (R$): ").strip().replace(",", "."))
            quantidade = int(input("Quantidade inicial em estoque: ").strip())
        except ValueError:
            print("Erro: valor numerico invalido.")
            return
        produto, erro = self._produto_ctrl.cadastrar(nome, preco, categoria)
        if erro:
            print(f"Erro: {erro}")
            return
        self._estoque_ctrl.inicializar(produto.id, quantidade)
        print(f"Produto cadastrado: {produto}")
        print(f"Estoque inicial: {quantidade} unidades.")

    def _listar(self):
        produtos = self._produto_ctrl.listar()
        if not produtos:
            print("Nenhum produto cadastrado.")
            return
        print("\n-- Produtos em Estoque --")
        print(f"{'ID':<5} {'Nome':<25} {'Categoria':<12} {'Preco':>10} {'Estoque':>8}")
        print("-" * 65)
        for p in produtos:
            estoque = self._estoque_ctrl.obter(p.id)
            qtd = estoque.quantidade if estoque else 0
            print(
                f"{p.id:<5} {p.nome:<25} {p.categoria:<12}"
                f" R$ {p.preco:>8.2f} {qtd:>8}"
            )

    def _repor_estoque(self):
        self._listar()
        if not self._produto_ctrl.listar():
            return
        try:
            produto_id = int(input("ID do produto: ").strip())
            quantidade = int(input("Quantidade a repor: ").strip())
        except ValueError:
            print("Erro: valor invalido.")
            return
        sucesso, erro = self._estoque_ctrl.adicionar(produto_id, quantidade)
        if erro:
            print(f"Erro: {erro}")
        else:
            estoque = self._estoque_ctrl.obter(produto_id)
            print(f"Estoque atualizado. Total: {estoque.quantidade}")
