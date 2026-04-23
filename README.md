# Sistema de Gerenciamento de Pizzaria

Sistema de gerenciamento operacional para pizzarias desenvolvido em Python,
com arquitetura MVC, orientacao a objetos e interface em terminal (CLI).

---

## Sumario

- [Visao Geral](#visao-geral)
- [Funcionalidades](#funcionalidades)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Arquitetura MVC](#arquitetura-mvc)
- [Como Executar](#como-executar)
- [Testes Automatizados](#testes-automatizados)
- [Fluxo de Uso](#fluxo-de-uso)
- [Regras de Negocio](#regras-de-negocio)
- [Documentacao Tecnica](#documentacao-tecnica)

---

## Visao Geral

O sistema cobre o ciclo operacional completo de uma pizzaria:

- Cadastro de clientes, produtos e mesas
- Controle de estoque com atualizacao automatica ao registrar pedidos
- Abertura e gerenciamento de pedidos vinculados a mesas
- Calculo automatico de totais
- Processamento de pagamentos com multiplos metodos
- Relatorio de fechamento financeiro diario

---

## Funcionalidades

| Modulo            | Funcionalidades                                                  |
|-------------------|------------------------------------------------------------------|
| Clientes          | Cadastrar, listar, buscar por nome                               |
| Produtos          | Cadastrar com categoria e preco, listar                          |
| Estoque           | Controle automatico, reposicao manual, bloqueio por falta        |
| Mesas             | Cadastrar, listar, controle de status (livre / ocupada)          |
| Pedidos           | Abrir, adicionar itens, fechar, listar abertos                   |
| Pagamentos        | Processar pagamento, fechamento do dia com relatorio             |

---

## Estrutura do Projeto

```
sistema pizzaria/
  models/
    cliente.py          Entidade Cliente
    produto.py          Entidade Produto
    estoque.py          Entidade Estoque
    mesa.py             Entidade Mesa
    pedido.py           Entidade Pedido
    item_pedido.py      Entidade ItemPedido
    pagamento.py        Entidade Pagamento
  controllers/
    cliente_controller.py
    produto_controller.py
    estoque_controller.py
    mesa_controller.py
    pedido_controller.py
    pagamento_controller.py
  views/
    menu_view.py        Menu principal interativo
    cliente_view.py
    produto_view.py
    mesa_view.py
    pedido_view.py
    pagamento_view.py
  docs/
    README.md           Documentacao tecnica detalhada (MER, fluxos, MVC)
  main.py               Ponto de entrada da aplicacao
  tests.py              Suite de testes automatizados (144 casos)
```

---

## Arquitetura MVC

O projeto segue o padrao **Model-View-Controller** com separacao estrita
de responsabilidades.

```
View  ->  Controller  ->  Model
```

- **Model** — representa as entidades de negocio. Contem atributos encapsulados,
  construtores e comportamentos proprios. Nao conhece Controllers nem Views.

- **Controller** — aplica as regras de negocio, valida dados, coordena os Models
  e retorna resultados para a View.

- **View** — exibe menus no terminal, coleta entradas do usuario e formata saidas.
  Nao contem logica de negocio.

Os Controllers que dependem de outros Controllers recebem essas dependencias
via construtor (injecao de dependencia):

```python
pedido_ctrl    = PedidoController(mesa_ctrl, produto_ctrl, estoque_ctrl)
pagamento_ctrl = PagamentoController(pedido_ctrl)
```

---

## Como Executar

### Pre-requisitos

- Python 3.8 ou superior
- Nenhuma dependencia externa

### Executar o sistema

```bash
python main.py
```

### Executar os testes

```bash
python tests.py
```

### Menu principal

```
==========================================
    SISTEMA DE GERENCIAMENTO DE PIZZARIA
==========================================

--- MENU PRINCIPAL ---
1 - Gerenciar Clientes
2 - Gerenciar Produtos e Estoque
3 - Gerenciar Mesas
4 - Gerenciar Pedidos
5 - Pagamento
0 - Sair
```

Cada opcao abre um submenu especifico. Digite `0` em qualquer tela para voltar.

---

## Testes Automatizados

O projeto inclui uma suite completa de testes sem dependencias externas.

```bash
python tests.py
```

### Cobertura

| Suite                       | Casos | O que e testado                                             |
|-----------------------------|-------|-------------------------------------------------------------|
| Model: Cliente              | 6     | Atributos, getters, setters, __str__                        |
| Model: Produto              | 8     | Atributos, getters, setters, __str__                        |
| Model: Estoque              | 11    | Adicionar, remover, disponibilidade, limites                |
| Model: Mesa                 | 8     | Status livre/ocupada, metodos ocupar/liberar                |
| Model: Pedido               | 14    | Status, adicao de itens, recalculo de total                 |
| Model: ItemPedido           | 7     | Atributos e calculo de subtotal                             |
| Model: Pagamento            | 6     | Atributos, metodos aceitos                                  |
| Controller: Cliente         | 10    | Cadastro, listagem, busca por ID e por nome, validacoes     |
| Controller: Produto         | 8     | Cadastro, validacoes de nome e preco, listagem              |
| Controller: Estoque         | 14    | Inicializar, adicionar, remover, disponibilidade            |
| Controller: Mesa            | 11    | Cadastro, duplicidade, ocupar/liberar, listar livres        |
| Controller: Pedido          | 21    | Abrir, itens, fechar, estoque, pedido fechado, validacoes   |
| Controller: Pagamento       | 12    | Metodo invalido, duplicidade, liberacao de mesa, fechamento |
| Integracao: Fluxo completo  | 9     | Ciclo operacional com 3 mesas, estoque e faturamento        |
| **Total**                   | **145** |                                                           |

Saida esperada ao final:

```
=======================================================
  RESULTADO: 144/144 testes passaram
=======================================================
```

---

## Fluxo de Uso

### Primeiro uso (configuracao inicial)

1. **Opcao 2** — Cadastrar produtos (nome, categoria, preco, estoque inicial)
2. **Opcao 3** — Cadastrar mesas (numero identificador)
3. **Opcao 1** — (Opcional) Cadastrar clientes

### Atendimento

```
Abrir pedido
    -> Opcao 4 > 1
    -> Selecionar mesa livre
    -> Vincular a um cliente (opcional)

Adicionar itens
    -> Opcao 4 > 2
    -> Informar ID do pedido, ID do produto e quantidade
    -> O sistema verifica estoque, debita e recalcula o total

Fechar pedido
    -> Opcao 4 > 5
    -> Encerra a fase de adicao de itens

Pagar
    -> Opcao 5 > 1
    -> Selecionar pedido, confirmar total
    -> Escolher metodo: dinheiro, cartao_credito, cartao_debito ou pix
    -> Mesa e liberada automaticamente
```

### Fechamento do dia

```
Opcao 5 > 2
```

Exibe o total de pedidos pagos e o faturamento acumulado do dia.

---

## Regras de Negocio

- Todo pedido deve estar vinculado a uma mesa
- So e possivel abrir pedido em mesa com status **livre**
- Ao abrir um pedido, a mesa passa para status **ocupada**
- Itens so podem ser adicionados a pedidos com status **aberto**
- O sistema bloqueia a venda se o estoque for insuficiente
- O estoque e debitado automaticamente ao adicionar cada item
- O total do pedido e calculado automaticamente pela soma dos subtotais
- O pagamento encerra o pedido (status **pago**) e libera a mesa
- O fechamento do dia soma apenas pedidos com status **pago**

---

## Documentacao Tecnica

Para detalhes sobre o modelo entidade-relacionamento (MER), diagrama de
relacionamentos entre entidades e explicacao aprofundada da arquitetura MVC,
consulte:

[docs/README.md](docs/README.md)
