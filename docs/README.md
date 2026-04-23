# Sistema de Gerenciamento de Pizzaria

## 1. Descricao do Sistema

O Sistema de Gerenciamento de Pizzaria e uma aplicacao de linha de comando (CLI)
desenvolvida em Python para automatizar as operacoes diarias de uma pizzaria.

O sistema cobre o ciclo operacional completo:

- Cadastro de clientes, produtos (pizzas, bebidas, etc.) e mesas
- Controle de estoque com debito automatico ao registrar pedidos
- Abertura e gerenciamento de pedidos vinculados a mesas
- Adicao de itens com calculo automatico de totais
- Processamento de pagamentos com multiplos metodos
- Fechamento financeiro diario com relatorio de faturamento

---

## 2. Arquitetura MVC

O projeto segue estritamente o padrao **MVC (Model-View-Controller)**, com
separacao clara de responsabilidades entre as tres camadas.

```
sistema-pizzaria/
  models/       -> entidades de negocio (dados e comportamentos)
  controllers/  -> regras de negocio e coordenacao
  views/        -> interface com o usuario (CLI)
  docs/
  main.py
```

### Model (`/models`)

Representa as entidades do dominio. Cada classe encapsula seus atributos,
oferece getters/setters quando necessario e define comportamentos proprios.
Os Models nao conhecem Controllers nem Views.

Classes: `Cliente`, `Produto`, `Estoque`, `Mesa`, `Pedido`, `ItemPedido`, `Pagamento`

### View (`/views`)

Responsavel exclusivamente pela interface com o usuario. Exibe menus, coleta
entradas via `input()` e formata saidas no terminal. Nao contem logica de negocio.

Classes: `MenuView`, `ClienteView`, `ProdutoView`, `MesaView`, `PedidoView`, `PagamentoView`

### Controller (`/controllers`)

Intermediario entre View e Model. Recebe dados brutos da View, aplica validacoes
e regras de negocio, coordena os Models e retorna resultados para a View.

Classes: `ClienteController`, `ProdutoController`, `EstoqueController`,
         `MesaController`, `PedidoController`, `PagamentoController`

### Fluxo de dependencia

```
View  ->  Controller  ->  Model
```

A View chama metodos do Controller. O Controller manipula os Models.
Os Models nunca referenciam Controllers ou Views.

### Injecao de dependencia

Os Controllers que dependem de outros Controllers recebem essas dependencias
via construtor (injecao de dependencia), evitando acoplamento rigido e
facilitando testes isolados.

```python
pedido_ctrl  = PedidoController(mesa_ctrl, produto_ctrl, estoque_ctrl)
pagamento_ctrl = PagamentoController(pedido_ctrl)
```

---

## 3. Diagrama M.E.R (Modelo Entidade-Relacionamento)

### Entidades

#### Cliente

| Campo    | Tipo | Descricao           |
|----------|------|---------------------|
| id       | int  | Identificador unico |
| nome     | str  | Nome do cliente     |
| telefone | str  | Telefone de contato |

#### Produto

| Campo     | Tipo  | Descricao                        |
|-----------|-------|----------------------------------|
| id        | int   | Identificador unico              |
| nome      | str   | Nome do produto                  |
| preco     | float | Preco unitario                   |
| categoria | str   | Categoria (pizza / bebida / etc) |

#### Estoque

| Campo      | Tipo | Descricao                  |
|------------|------|----------------------------|
| produto_id | int  | Referencia ao Produto (FK) |
| quantidade | int  | Quantidade disponivel      |

#### Mesa

| Campo  | Tipo | Descricao              |
|--------|------|------------------------|
| id     | int  | Identificador unico    |
| numero | int  | Numero da mesa         |
| status | str  | "livre" ou "ocupada"   |

#### Pedido

| Campo      | Tipo  | Descricao                           |
|------------|-------|-------------------------------------|
| id         | int   | Identificador unico                 |
| mesa_id    | int   | Referencia a Mesa (FK)              |
| cliente_id | int   | Referencia a Cliente (FK, opcional) |
| status     | str   | "aberto", "fechado" ou "pago"       |
| total      | float | Valor total calculado               |

#### ItemPedido

| Campo          | Tipo  | Descricao                       |
|----------------|-------|---------------------------------|
| id             | int   | Identificador unico             |
| pedido_id      | int   | Referencia ao Pedido (FK)       |
| produto_id     | int   | Referencia ao Produto (FK)      |
| nome_produto   | str   | Nome do produto no momento      |
| preco_unitario | float | Preco no momento da venda       |
| quantidade     | int   | Quantidade solicitada           |
| subtotal       | float | preco_unitario x quantidade     |

#### Pagamento

| Campo     | Tipo  | Descricao                  |
|-----------|-------|----------------------------|
| id        | int   | Identificador unico        |
| pedido_id | int   | Referencia ao Pedido (FK)  |
| valor     | float | Valor total pago           |
| metodo    | str   | Forma de pagamento         |

### Relacionamentos

```
Cliente -----(0,N)-----> Pedido
Mesa    -----(1,N)-----> Pedido
Pedido  -----(1,N)-----> ItemPedido
Produto -----(1,N)-----> ItemPedido
Produto -----(1,1)-----> Estoque
Pedido  -----(1,1)-----> Pagamento
```

**Cliente -> Pedido (1:N, opcional)**
Um cliente pode estar associado a varios pedidos ao longo do tempo. Um pedido
pode existir sem cliente (atendimento anonimo). Relacao opcional.

**Mesa -> Pedido (1:N)**
Uma mesa pode gerar varios pedidos ao longo do dia (um por vez, enquanto ocupada).
Cada pedido pertence obrigatoriamente a uma unica mesa.

**Pedido -> ItemPedido (1:N)**
Um pedido contem um ou mais itens. Cada ItemPedido pertence a exatamente um pedido.
O total do pedido e calculado como a soma dos subtotais de seus itens.

**Produto -> ItemPedido (1:N)**
Um produto pode aparecer em varios itens de pedidos distintos. Cada ItemPedido
referencia um unico produto. O nome e preco sao copiados no momento da venda para
preservar historico.

**Produto -> Estoque (1:1)**
Cada produto possui exatamente um registro de estoque. O estoque e debitado
automaticamente ao adicionar um item ao pedido.

**Pedido -> Pagamento (1:1)**
Cada pedido possui no maximo um pagamento. O registro do pagamento encerra o
pedido e libera a mesa correspondente.

---

## 4. Fluxo do Sistema

### Cadastro inicial

1. Cadastrar produtos informando nome, categoria, preco e quantidade inicial
2. Cadastrar mesas com numero identificador
3. (Opcional) Cadastrar clientes com nome e telefone

### Abertura de pedido

1. Acessar "Gerenciar Pedidos" > "Abrir pedido"
2. Selecionar uma mesa livre pela lista exibida
3. (Opcional) Vincular o pedido a um cliente cadastrado
4. O sistema cria o pedido com status "aberto" e marca a mesa como "ocupada"

### Insercao de itens

1. Acessar "Adicionar item ao pedido"
2. Selecionar o pedido aberto desejado
3. Informar o ID do produto e a quantidade
4. O sistema verifica disponibilidade em estoque
5. Se disponivel, debita do estoque, cria o ItemPedido e recalcula o total

### Pagamento

1. Acessar "Pagamento" > "Realizar pagamento"
2. Selecionar o pedido pendente
3. Conferir o total exibido
4. Escolher o metodo: dinheiro, cartao_credito, cartao_debito ou pix
5. O sistema registra o Pagamento, muda o status do pedido para "pago" e
   libera a mesa

### Fechamento do dia

1. Acessar "Pagamento" > "Fechamento do dia"
2. O sistema exibe:
   - Quantidade total de pedidos pagos no dia
   - Faturamento total acumulado
   - Lista de todos os pagamentos registrados

---

## 5. Como Executar

### Pre-requisitos

- Python 3.8 ou superior
- Sem dependencias externas (somente biblioteca padrao)

### Executar o sistema

```bash
# Navegar ate a pasta raiz do projeto
cd "sistema pizzaria"

# Iniciar o sistema
python main.py
```

### Navegacao no menu

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

Cada opcao leva a um submenu especifico. Digite `0` em qualquer tela para voltar
ao menu anterior.

### Fluxo recomendado para primeiro uso

1. Cadastrar pelo menos um produto (opcao 2)
2. Cadastrar pelo menos uma mesa (opcao 3)
3. Abrir um pedido (opcao 4 > 1)
4. Adicionar itens ao pedido (opcao 4 > 2)
5. Realizar o pagamento (opcao 5 > 1)
6. Consultar o fechamento do dia (opcao 5 > 2)

### Observacoes

- Os dados sao mantidos em memoria durante a sessao
- Ao encerrar o sistema os dados nao sao persistidos
- Nenhuma instalacao adicional e necessaria
