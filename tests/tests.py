"""
Testes automatizados do Sistema de Gerenciamento de Pizzaria.

Cobertura:
    - Models: Cliente, Produto, Estoque, Mesa, Pedido, ItemPedido, Pagamento
    - Controllers: ClienteController, ProdutoController, EstoqueController,
                   MesaController, PedidoController, PagamentoController
    - Regras de negocio: estoque, validacoes, fluxo completo

Execucao:
    python tests/tests.py
"""

import sys
import traceback
from pathlib import Path

# Garante que a raiz do projeto esteja no sys.path independente de onde o
# script e executado (ex.: python tests/tests.py ou cd tests && python tests.py)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

_DB_PATH = Path(__file__).resolve().parent.parent / "db.txt"


def _limpar_db():
    """Remove o arquivo db.txt para garantir estado limpo entre suites de teste."""
    if _DB_PATH.exists():
        _DB_PATH.unlink()

# ---------------------------------------------------------------------------
# Infraestrutura minima de testes
# ---------------------------------------------------------------------------

_resultados = {"passou": 0, "falhou": 0, "erros": []}


def _ok(descricao: str):
    _resultados["passou"] += 1
    print(f"  [OK] {descricao}")


def _falha(descricao: str, detalhe: str = ""):
    _resultados["falhou"] += 1
    msg = f"  [FALHA] {descricao}"
    if detalhe:
        msg += f" -> {detalhe}"
    print(msg)
    _resultados["erros"].append(msg)


def afirmar(condicao: bool, descricao: str, detalhe: str = ""):
    if condicao:
        _ok(descricao)
    else:
        _falha(descricao, detalhe)


def secao(titulo: str):
    print(f"\n{'=' * 55}")
    print(f"  {titulo}")
    print("=" * 55)


def resumo():
    total = _resultados["passou"] + _resultados["falhou"]
    print(f"\n{'=' * 55}")
    print(f"  RESULTADO: {_resultados['passou']}/{total} testes passaram")
    if _resultados["erros"]:
        print("\n  Falhas encontradas:")
        for e in _resultados["erros"]:
            print(f"  {e}")
    print("=" * 55)
    return _resultados["falhou"] == 0


# ---------------------------------------------------------------------------
# Factories para isolar cada suite de testes
# ---------------------------------------------------------------------------

def _criar_controllers():
    _limpar_db()
    from controllers.cliente_controller import ClienteController
    from controllers.estoque_controller import EstoqueController
    from controllers.mesa_controller import MesaController
    from controllers.pagamento_controller import PagamentoController
    from controllers.pedido_controller import PedidoController
    from controllers.produto_controller import ProdutoController

    cliente_ctrl = ClienteController()
    produto_ctrl = ProdutoController()
    estoque_ctrl = EstoqueController()
    mesa_ctrl = MesaController()
    pedido_ctrl = PedidoController(mesa_ctrl, produto_ctrl, estoque_ctrl)
    pagamento_ctrl = PagamentoController(pedido_ctrl)
    return cliente_ctrl, produto_ctrl, estoque_ctrl, mesa_ctrl, pedido_ctrl, pagamento_ctrl


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

def testar_model_cliente():
    secao("Model: Cliente")
    from models.cliente import Cliente

    c = Cliente(1, "Joao Silva", "11999990000")
    afirmar(c.id == 1, "id correto")
    afirmar(c.nome == "Joao Silva", "nome correto")
    afirmar(c.telefone == "11999990000", "telefone correto")

    c.nome = "Joao Souza"
    afirmar(c.nome == "Joao Souza", "setter nome")

    c.telefone = "11888880000"
    afirmar(c.telefone == "11888880000", "setter telefone")

    afirmar("Joao Souza" in str(c), "__str__ contem nome")


def testar_model_produto():
    secao("Model: Produto")
    from models.produto import Produto

    p = Produto(1, "Pizza Calabresa", 42.50, "pizza")
    afirmar(p.id == 1, "id correto")
    afirmar(p.nome == "Pizza Calabresa", "nome correto")
    afirmar(p.preco == 42.50, "preco correto")
    afirmar(p.categoria == "pizza", "categoria correta")

    p.preco = 45.00
    afirmar(p.preco == 45.00, "setter preco")

    p.categoria = "especial"
    afirmar(p.categoria == "especial", "setter categoria")

    afirmar("R$" in str(p) or "45" in str(p), "__str__ contem preco")


def testar_model_estoque():
    secao("Model: Estoque")
    from models.estoque import Estoque

    e = Estoque(1, 10)
    afirmar(e.produto_id == 1, "produto_id correto")
    afirmar(e.quantidade == 10, "quantidade inicial correta")
    afirmar(e.tem_disponivel(10), "tem_disponivel igual ao estoque")
    afirmar(not e.tem_disponivel(11), "tem_disponivel acima do estoque retorna False")

    e.adicionar(5)
    afirmar(e.quantidade == 15, "adicionar incrementa corretamente")

    e.adicionar(0)
    afirmar(e.quantidade == 15, "adicionar zero nao altera")

    e.adicionar(-3)
    afirmar(e.quantidade == 15, "adicionar negativo nao altera")

    resultado = e.remover(5)
    afirmar(resultado is True, "remover retorna True quando ha estoque")
    afirmar(e.quantidade == 10, "quantidade apos remover correta")

    resultado_falha = e.remover(100)
    afirmar(resultado_falha is False, "remover acima do estoque retorna False")
    afirmar(e.quantidade == 10, "quantidade nao alterada apos remover com falha")


def testar_model_mesa():
    secao("Model: Mesa")
    from models.mesa import Mesa

    m = Mesa(1, 5)
    afirmar(m.id == 1, "id correto")
    afirmar(m.numero == 5, "numero correto")
    afirmar(m.status == Mesa.STATUS_LIVRE, "status inicial livre")
    afirmar(m.esta_livre(), "esta_livre retorna True quando livre")

    m.ocupar()
    afirmar(m.status == Mesa.STATUS_OCUPADA, "status apos ocupar")
    afirmar(not m.esta_livre(), "esta_livre retorna False quando ocupada")

    m.liberar()
    afirmar(m.status == Mesa.STATUS_LIVRE, "status apos liberar")
    afirmar(m.esta_livre(), "esta_livre True apos liberar")


def testar_model_pedido():
    secao("Model: Pedido")
    from models.item_pedido import ItemPedido
    from models.pedido import Pedido

    p = Pedido(1, 2, cliente_id=10)
    afirmar(p.id == 1, "id correto")
    afirmar(p.mesa_id == 2, "mesa_id correto")
    afirmar(p.cliente_id == 10, "cliente_id correto")
    afirmar(p.status == Pedido.STATUS_ABERTO, "status inicial aberto")
    afirmar(p.esta_aberto(), "esta_aberto True")
    afirmar(p.total == 0.0, "total inicial zero")
    afirmar(len(p.itens) == 0, "itens inicial vazio")

    item = ItemPedido(1, 1, 1, "Pizza", 40.00, 2)
    p.adicionar_item(item)
    afirmar(len(p.itens) == 1, "item adicionado")
    afirmar(p.total == 80.00, "total recalculado apos adicionar item")

    p.fechar()
    afirmar(p.status == Pedido.STATUS_FECHADO, "status apos fechar")
    afirmar(not p.esta_aberto(), "esta_aberto False apos fechar")
    afirmar(not p.esta_pago(), "esta_pago False antes de pagar")

    p.marcar_pago()
    afirmar(p.status == Pedido.STATUS_PAGO, "status apos marcar_pago")
    afirmar(p.esta_pago(), "esta_pago True")


def testar_model_item_pedido():
    secao("Model: ItemPedido")
    from models.item_pedido import ItemPedido

    item = ItemPedido(1, 10, 5, "Bebida", 8.50, 3)
    afirmar(item.id == 1, "id correto")
    afirmar(item.pedido_id == 10, "pedido_id correto")
    afirmar(item.produto_id == 5, "produto_id correto")
    afirmar(item.nome_produto == "Bebida", "nome_produto correto")
    afirmar(item.preco_unitario == 8.50, "preco_unitario correto")
    afirmar(item.quantidade == 3, "quantidade correta")
    afirmar(item.subtotal == 25.50, "subtotal calculado corretamente")


def testar_model_pagamento():
    secao("Model: Pagamento")
    from models.pagamento import Pagamento

    pg = Pagamento(1, 7, 95.00, "pix")
    afirmar(pg.id == 1, "id correto")
    afirmar(pg.pedido_id == 7, "pedido_id correto")
    afirmar(pg.valor == 95.00, "valor correto")
    afirmar(pg.metodo == "pix", "metodo correto")
    afirmar("pix" in str(pg), "__str__ contem metodo")
    afirmar(len(Pagamento.METODOS_ACEITOS) >= 4, "metodos aceitos definidos")


# ---------------------------------------------------------------------------
# Controllers
# ---------------------------------------------------------------------------

def testar_cliente_controller():
    secao("Controller: ClienteController")
    cc, *_ = _criar_controllers()

    cliente, erro = cc.cadastrar("Ana Lima", "11912345678")
    afirmar(erro is None, "cadastrar cliente valido sem erro")
    afirmar(cliente is not None, "retorna objeto Cliente")
    afirmar(cliente.nome == "Ana Lima", "nome cadastrado correto")

    _, erro2 = cc.cadastrar("", "11900000000")
    afirmar(erro2 is not None, "rejeita nome vazio")

    cc.cadastrar("Bruno Costa", "11988887777")
    cc.cadastrar("Bruno Alves", "11977776666")
    lista = cc.listar()
    afirmar(len(lista) == 3, "listar retorna todos os clientes")

    encontrado = cc.buscar_por_id(cliente.id)
    afirmar(encontrado is not None, "buscar_por_id encontra cliente existente")
    afirmar(encontrado.id == cliente.id, "buscar_por_id retorna cliente correto")

    nao_encontrado = cc.buscar_por_id(9999)
    afirmar(nao_encontrado is None, "buscar_por_id retorna None para ID inexistente")

    resultados = cc.buscar_por_nome("Bruno")
    afirmar(len(resultados) == 2, "buscar_por_nome retorna multiplos resultados")

    sem_resultado = cc.buscar_por_nome("ZZZ")
    afirmar(len(sem_resultado) == 0, "buscar_por_nome retorna lista vazia sem resultado")


def testar_produto_controller():
    secao("Controller: ProdutoController")
    _, pc, ec, *_ = _criar_controllers()

    produto, erro = pc.cadastrar("Pizza Quatro Queijos", 52.00, "pizza")
    afirmar(erro is None, "cadastrar produto valido sem erro")
    afirmar(produto is not None, "retorna objeto Produto")

    _, erro2 = pc.cadastrar("", 10.00, "bebida")
    afirmar(erro2 is not None, "rejeita nome vazio")

    _, erro3 = pc.cadastrar("Suco", 0, "bebida")
    afirmar(erro3 is not None, "rejeita preco zero")

    _, erro4 = pc.cadastrar("Suco", -5.00, "bebida")
    afirmar(erro4 is not None, "rejeita preco negativo")

    pc.cadastrar("Refrigerante", 8.00, "bebida")
    lista = pc.listar()
    afirmar(len(lista) == 2, "listar retorna todos os produtos")

    encontrado = pc.buscar_por_id(produto.id)
    afirmar(encontrado is not None, "buscar_por_id encontra produto")

    nao_encontrado = pc.buscar_por_id(9999)
    afirmar(nao_encontrado is None, "buscar_por_id None para inexistente")


def testar_estoque_controller():
    secao("Controller: EstoqueController")
    _, pc, ec, *_ = _criar_controllers()

    produto, _ = pc.cadastrar("Pizza Bacon", 48.00, "pizza")
    ec.inicializar(produto.id, 15)
    est = ec.obter(produto.id)
    afirmar(est is not None, "inicializar cria estoque")
    afirmar(est.quantidade == 15, "quantidade inicial correta")

    sucesso, erro = ec.adicionar(produto.id, 5)
    afirmar(sucesso is True, "adicionar retorna True")
    afirmar(erro is None, "adicionar sem erro")
    afirmar(ec.obter(produto.id).quantidade == 20, "quantidade apos adicionar")

    _, erro2 = ec.adicionar(produto.id, 0)
    afirmar(erro2 is not None, "adicionar zero retorna erro")

    _, erro3 = ec.adicionar(9999, 5)
    afirmar(erro3 is not None, "adicionar para produto sem estoque retorna erro")

    afirmar(ec.verificar_disponibilidade(produto.id, 20), "disponibilidade exata OK")
    afirmar(not ec.verificar_disponibilidade(produto.id, 21), "indisponivel acima do estoque")
    afirmar(not ec.verificar_disponibilidade(9999, 1), "indisponivel para produto sem estoque")

    resultado = ec.remover(produto.id, 10)
    afirmar(resultado is True, "remover retorna True com estoque")
    afirmar(ec.obter(produto.id).quantidade == 10, "quantidade apos remover correta")

    resultado_falha = ec.remover(produto.id, 999)
    afirmar(resultado_falha is False, "remover retorna False sem estoque suficiente")

    lista = ec.listar()
    afirmar(len(lista) == 1, "listar retorna todos os estoques")


def testar_mesa_controller():
    secao("Controller: MesaController")
    *_, mc, _, _ = _criar_controllers()
    mc = mc  # mesa_controller esta na posicao 3
    cc, pc, ec, mc, pedido_c, pg_c = _criar_controllers()

    mesa, erro = mc.cadastrar(1)
    afirmar(erro is None, "cadastrar mesa valida sem erro")
    afirmar(mesa is not None, "retorna objeto Mesa")

    _, erro2 = mc.cadastrar(1)
    afirmar(erro2 is not None, "rejeita numero de mesa duplicado")

    mc.cadastrar(2)
    mc.cadastrar(3)
    lista = mc.listar()
    afirmar(len(lista) == 3, "listar retorna todas as mesas")

    livres = mc.listar_livres()
    afirmar(len(livres) == 3, "todas livres inicialmente")

    resultado = mc.ocupar(mesa.id)
    afirmar(resultado is True, "ocupar mesa livre retorna True")
    afirmar(mc.buscar_por_id(mesa.id).status == "ocupada", "status ocupada apos ocupar")

    resultado2 = mc.ocupar(mesa.id)
    afirmar(resultado2 is False, "ocupar mesa ja ocupada retorna False")

    livres_depois = mc.listar_livres()
    afirmar(len(livres_depois) == 2, "livres reduzidas apos ocupar")

    mc.liberar(mesa.id)
    afirmar(mc.buscar_por_id(mesa.id).status == "livre", "status livre apos liberar")

    nao_encontrado = mc.buscar_por_id(9999)
    afirmar(nao_encontrado is None, "buscar_por_id None para inexistente")


def testar_pedido_controller():
    secao("Controller: PedidoController")
    cc, pc, ec, mc, pedido_c, pg_c = _criar_controllers()

    produto, _ = pc.cadastrar("Pizza Portuguesa", 50.00, "pizza")
    bebida, _ = pc.cadastrar("Suco de Laranja", 10.00, "bebida")
    ec.inicializar(produto.id, 5)
    ec.inicializar(bebida.id, 3)
    mesa, _ = mc.cadastrar(1)

    # Abrir pedido
    pedido, erro = pedido_c.abrir(mesa.id)
    afirmar(erro is None, "abrir pedido em mesa livre sem erro")
    afirmar(pedido is not None, "retorna objeto Pedido")
    afirmar(mc.buscar_por_id(mesa.id).status == "ocupada", "mesa marcada como ocupada")

    # Tentar abrir outro pedido na mesma mesa
    _, erro2 = pedido_c.abrir(mesa.id)
    afirmar(erro2 is not None, "rejeita abrir pedido em mesa ocupada")

    # Abrir em mesa inexistente
    _, erro3 = pedido_c.abrir(9999)
    afirmar(erro3 is not None, "rejeita abrir pedido em mesa inexistente")

    # Adicionar itens
    item1, err_item = pedido_c.adicionar_item(pedido.id, produto.id, 2)
    afirmar(err_item is None, "adicionar item valido sem erro")
    afirmar(item1 is not None, "retorna ItemPedido")
    afirmar(item1.subtotal == 100.00, "subtotal do item correto")
    afirmar(ec.obter(produto.id).quantidade == 3, "estoque debitado corretamente")

    item2, _ = pedido_c.adicionar_item(pedido.id, bebida.id, 1)
    p_atualizado = pedido_c.buscar_por_id(pedido.id)
    afirmar(p_atualizado.total == 110.00, "total do pedido recalculado corretamente")
    afirmar(len(p_atualizado.itens) == 2, "pedido tem dois itens")

    # Adicionar item com estoque insuficiente
    _, erro_est = pedido_c.adicionar_item(pedido.id, bebida.id, 999)
    afirmar(erro_est is not None, "rejeita quantidade acima do estoque")
    afirmar(ec.obter(bebida.id).quantidade == 2, "estoque nao alterado apos rejeicao")

    # Adicionar item com quantidade invalida
    _, erro_qtd = pedido_c.adicionar_item(pedido.id, produto.id, 0)
    afirmar(erro_qtd is not None, "rejeita quantidade zero")

    # Adicionar item a pedido inexistente
    _, erro_pid = pedido_c.adicionar_item(9999, produto.id, 1)
    afirmar(erro_pid is not None, "rejeita pedido inexistente")

    # Adicionar produto inexistente
    _, erro_prod = pedido_c.adicionar_item(pedido.id, 9999, 1)
    afirmar(erro_prod is not None, "rejeita produto inexistente")

    # Fechar pedido vazio (nova mesa/pedido)
    mesa2, _ = mc.cadastrar(2)
    pedido_vazio, _ = pedido_c.abrir(mesa2.id)
    _, erro_fechar_vazio = pedido_c.fechar(pedido_vazio.id)
    afirmar(erro_fechar_vazio is not None, "rejeita fechar pedido sem itens")

    # Fechar pedido com itens
    pedido_fechado, erro_fechar = pedido_c.fechar(pedido.id)
    afirmar(erro_fechar is None, "fechar pedido com itens sem erro")
    afirmar(pedido_fechado.status == "fechado", "status fechado apos fechar")

    # Adicionar item a pedido fechado
    _, erro_fechado = pedido_c.adicionar_item(pedido.id, produto.id, 1)
    afirmar(erro_fechado is not None, "rejeita adicionar item a pedido fechado")

    # Listar abertos
    abertos = pedido_c.listar_abertos()
    afirmar(len(abertos) == 1, "listar_abertos retorna apenas pedidos abertos")


def testar_pagamento_controller():
    secao("Controller: PagamentoController")
    cc, pc, ec, mc, pedido_c, pg_c = _criar_controllers()

    produto, _ = pc.cadastrar("Pizza Especial", 60.00, "pizza")
    ec.inicializar(produto.id, 10)
    mesa, _ = mc.cadastrar(1)

    pedido, _ = pedido_c.abrir(mesa.id)
    pedido_c.adicionar_item(pedido.id, produto.id, 1)

    # Metodo invalido
    _, erro_metodo = pg_c.processar(pedido.id, "cheque")
    afirmar(erro_metodo is not None, "rejeita metodo de pagamento invalido")

    # Pedido inexistente
    _, erro_pid = pg_c.processar(9999, "pix")
    afirmar(erro_pid is not None, "rejeita pedido inexistente")

    # Pagamento valido
    pagamento, erro = pg_c.processar(pedido.id, "cartao_credito")
    afirmar(erro is None, "processar pagamento valido sem erro")
    afirmar(pagamento is not None, "retorna objeto Pagamento")
    afirmar(pagamento.valor == 60.00, "valor do pagamento correto")
    afirmar(pagamento.metodo == "cartao_credito", "metodo registrado correto")

    # Mesa liberada apos pagamento
    afirmar(mc.buscar_por_id(mesa.id).status == "livre", "mesa liberada apos pagamento")

    # Pedido marcado como pago
    pago = pedido_c.buscar_por_id(pedido.id)
    afirmar(pago.esta_pago(), "pedido marcado como pago")

    # Tentar pagar de novo
    _, erro_duplo = pg_c.processar(pedido.id, "pix")
    afirmar(erro_duplo is not None, "rejeita pagamento duplicado")

    # Fechamento do dia
    mesa2, _ = mc.cadastrar(2)
    pedido2, _ = pedido_c.abrir(mesa2.id)
    pedido_c.adicionar_item(pedido2.id, produto.id, 2)
    pg_c.processar(pedido2.id, "dinheiro")

    relatorio = pg_c.fechamento_do_dia()
    afirmar(relatorio["total_pedidos_pagos"] == 2, "fechamento conta pedidos pagos corretamente")
    afirmar(relatorio["faturamento_total"] == 180.00, "faturamento total correto")
    afirmar(len(relatorio["pagamentos"]) == 2, "relatorio lista todos os pagamentos")


# ---------------------------------------------------------------------------
# Fluxo de integracao completo
# ---------------------------------------------------------------------------

def testar_fluxo_completo():
    secao("Integracao: Fluxo completo do dia")
    cc, pc, ec, mc, pedido_c, pg_c = _criar_controllers()

    # Setup
    cliente, _ = cc.cadastrar("Carlos Ferreira", "11900001111")
    pizza, _ = pc.cadastrar("Pizza Margherita", 45.90, "pizza")
    bebida, _ = pc.cadastrar("Agua Mineral", 5.00, "bebida")
    ec.inicializar(pizza.id, 10)
    ec.inicializar(bebida.id, 20)
    mc.cadastrar(1)
    mc.cadastrar(2)
    mc.cadastrar(3)

    # Mesa 1 — pedido com cliente, paga no pix
    pedido1, _ = pedido_c.abrir(1, cliente.id)
    pedido_c.adicionar_item(pedido1.id, pizza.id, 2)
    pedido_c.adicionar_item(pedido1.id, bebida.id, 2)
    afirmar(pedido_c.buscar_por_id(pedido1.id).total == 101.80, "total mesa 1 correto")
    pg_c.processar(pedido1.id, "pix")

    # Mesa 2 — pedido anonimo, paga no dinheiro
    pedido2, _ = pedido_c.abrir(2)
    pedido_c.adicionar_item(pedido2.id, pizza.id, 1)
    pg_c.processar(pedido2.id, "dinheiro")

    # Mesa 3 — pedido aberto (nao pago)
    pedido3, _ = pedido_c.abrir(3)
    pedido_c.adicionar_item(pedido3.id, bebida.id, 3)

    # Verificacoes
    afirmar(mc.buscar_por_id(1).status == "livre", "mesa 1 livre apos pagamento")
    afirmar(mc.buscar_por_id(2).status == "livre", "mesa 2 livre apos pagamento")
    afirmar(mc.buscar_por_id(3).status == "ocupada", "mesa 3 ainda ocupada")

    afirmar(ec.obter(pizza.id).quantidade == 7, "estoque de pizza correto apos vendas")
    afirmar(ec.obter(bebida.id).quantidade == 15, "estoque de bebida correto apos vendas")

    relatorio = pg_c.fechamento_do_dia()
    faturamento_esperado = round(101.80 + 45.90, 2)
    afirmar(
        relatorio["total_pedidos_pagos"] == 2,
        "fechamento: quantidade de pedidos pagos",
    )
    afirmar(
        round(relatorio["faturamento_total"], 2) == faturamento_esperado,
        f"fechamento: faturamento correto ({faturamento_esperado})",
        str(relatorio["faturamento_total"]),
    )
    pagos = pedido_c.listar_pagos()
    afirmar(len(pagos) == 2, "listar_pagos retorna apenas pagos")


# ---------------------------------------------------------------------------
# Ponto de entrada
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        testar_model_cliente()
        testar_model_produto()
        testar_model_estoque()
        testar_model_mesa()
        testar_model_pedido()
        testar_model_item_pedido()
        testar_model_pagamento()
        testar_cliente_controller()
        testar_produto_controller()
        testar_estoque_controller()
        testar_mesa_controller()
        testar_pedido_controller()
        testar_pagamento_controller()
        testar_fluxo_completo()
    except Exception:
        print("\n[ERRO CRITICO] Excecao nao tratada durante os testes:")
        traceback.print_exc()
        sys.exit(1)

    passou = resumo()
    sys.exit(0 if passou else 1)
