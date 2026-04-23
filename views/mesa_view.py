from controllers.mesa_controller import MesaController


class MesaView:
    def __init__(self, controller: MesaController):
        self._ctrl = controller

    def exibir_menu(self):
        while True:
            print("\n--- MESAS ---")
            print("1 - Cadastrar mesa")
            print("2 - Listar mesas")
            print("0 - Voltar")
            opcao = input("Opcao: ").strip()
            if opcao == "1":
                self._cadastrar()
            elif opcao == "2":
                self._listar()
            elif opcao == "0":
                break
            else:
                print("Opcao invalida.")

    def _cadastrar(self):
        print("\n-- Cadastro de Mesa --")
        try:
            numero = int(input("Numero da mesa: ").strip())
        except ValueError:
            print("Erro: numero invalido.")
            return
        mesa, erro = self._ctrl.cadastrar(numero)
        if erro:
            print(f"Erro: {erro}")
        else:
            print(f"Mesa cadastrada: {mesa}")

    def _listar(self):
        mesas = self._ctrl.listar()
        if not mesas:
            print("Nenhuma mesa cadastrada.")
            return
        print("\n-- Lista de Mesas --")
        for m in mesas:
            print(m)
