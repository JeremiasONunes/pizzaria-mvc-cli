from controllers.cliente_controller import ClienteController


class ClienteView:
    def __init__(self, controller: ClienteController):
        self._ctrl = controller

    def exibir_menu(self):
        while True:
            print("\n--- CLIENTES ---")
            print("1 - Cadastrar cliente")
            print("2 - Listar clientes")
            print("3 - Buscar cliente por nome")
            print("0 - Voltar")
            opcao = input("Opcao: ").strip()
            if opcao == "1":
                self._cadastrar()
            elif opcao == "2":
                self._listar()
            elif opcao == "3":
                self._buscar_por_nome()
            elif opcao == "0":
                break
            else:
                print("Opcao invalida.")

    def _cadastrar(self):
        print("\n-- Cadastro de Cliente --")
        nome = input("Nome: ").strip()
        telefone = input("Telefone: ").strip()
        cliente, erro = self._ctrl.cadastrar(nome, telefone)
        if erro:
            print(f"Erro: {erro}")
        else:
            print(f"Cliente cadastrado com sucesso: {cliente}")

    def _listar(self):
        clientes = self._ctrl.listar()
        if not clientes:
            print("Nenhum cliente cadastrado.")
            return
        print("\n-- Lista de Clientes --")
        for c in clientes:
            print(c)

    def _buscar_por_nome(self):
        nome = input("Nome para busca: ").strip()
        resultados = self._ctrl.buscar_por_nome(nome)
        if not resultados:
            print("Nenhum cliente encontrado.")
            return
        for c in resultados:
            print(c)
