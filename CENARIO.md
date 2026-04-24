# Cenário do Cliente — Sistema de Gerenciamento de Pizzaria

---

## Apresentação do Projeto

### O Cliente

**Pizzaria** é uma pizzaria de bairro em pleno crescimento. O dono, **Seu Antônio**, atende clientes no salão com 10 mesas, vende por telefone e está sempre com dificuldade de controlar pedidos, estoque e fechar o caixa no final do dia.

Hoje tudo é feito no papel: o garçom anota o pedido num bloco, a cozinha não sabe o que tem em estoque, e Seu Antônio fecha o caixa somando cupons na calculadora. Vez ou outra perde venda por falta de produto, ou esquece de cobrar uma mesa.

---

## O Problema

> *"Toda semana tenho problema diferente. Semana passada vendi pizza que não tinha ingrediente. Essa semana esqueci de cobrar a mesa 7. Preciso de alguma coisa que me ajude a organizar isso tudo."*
> — **Seu Antônio, proprietário**

Os principais problemas levantados na entrevista com o cliente:

| Problema | Impacto |
|----------|---------|
| Pedidos anotados no papel | Perda de informação, erro no valor cobrado |
| Sem controle de estoque | Venda de produtos sem disponibilidade |
| Sem controle de mesas | Mesa ocupada não registrada, cobranças esquecidas |
| Fechamento manual do caixa | Erros de contagem, demora ao fim do dia |
| Sem histórico de clientes | Não sabe quem são seus clientes frequentes |

---

## A Solução

Você foi contratado como desenvolvedor para construir um **sistema de gerenciamento para a Pizzaria Bella Napoli**. O sistema deve rodar no terminal do computador da pizzaria (sem necessidade de internet ou instalação complexa) e resolver todos os problemas levantados.

### O que o sistema deve fazer

#### Gerenciar Clientes
- Cadastrar clientes com nome e telefone
- Consultar clientes pelo nome para agilizar o atendimento
- Manter histórico mesmo após reiniciar o sistema

#### Gerenciar Produtos
- Cadastrar pizzas, bebidas e outros itens com nome, preço e categoria
- Consultar o cardápio a qualquer momento

#### Controlar Estoque
- Registrar a quantidade disponível de cada produto
- Impedir que um pedido seja feito com produto em falta
- Debitar automaticamente o estoque quando um item é adicionado ao pedido

#### Gerenciar Mesas
- Cadastrar as mesas do salão com número identificador
- Saber quais mesas estão livres ou ocupadas em tempo real
- Liberar a mesa automaticamente quando o pagamento é processado

#### Registrar Pedidos
- Abrir um pedido vinculado a uma mesa (e opcionalmente a um cliente)
- Adicionar itens ao pedido com quantidade
- Calcular o total automaticamente
- Fechar o pedido quando o cliente pedir a conta

#### Processar Pagamentos
- Registrar o pagamento com o método escolhido pelo cliente (dinheiro, cartão de crédito, cartão de débito ou Pix)
- Gerar o fechamento do dia com total faturado e quantidade de pedidos pagos

#### Persistir os Dados
- Todos os dados devem ser salvos em um arquivo (`db.txt`) automaticamente
- Ao reiniciar o sistema, todos os dados devem ser carregados de volta

---

## Regras de Negócio

Estas são as regras que o sistema deve respeitar em qualquer situação:

1. **Não é possível abrir pedido em mesa ocupada** — a mesa precisa estar livre
2. **Não é possível adicionar item sem estoque disponível** — o sistema deve informar o erro
3. **Não é possível fechar pedido vazio** — é preciso ter pelo menos um item
4. **Não é possível pagar pedido já pago** — pagamento duplicado deve ser rejeitado
5. **A mesa só é liberada após o pagamento** — não basta fechar o pedido
6. **O estoque é debitado no momento em que o item é adicionado ao pedido**
7. **Métodos de pagamento aceitos:** `dinheiro`, `cartao_credito`, `cartao_debito`, `pix`

---

## Arquitetura Exigida

O sistema deve ser desenvolvido seguindo a **arquitetura MVC** (Model-View-Controller):

```
┌─────────────────────────────────────────────────────────────┐
│                        USUÁRIO (terminal)                   │
└───────────────────────────┬─────────────────────────────────┘
                            │
                    ┌───────▼────────┐
                    │   VIEW (CLI)   │  ← exibe menus, lê inputs
                    └───────┬────────┘
                            │
                  ┌─────────▼──────────┐
                  │   CONTROLLER       │  ← valida, decide, coordena
                  └─────────┬──────────┘
                            │
              ┌─────────────▼──────────────┐
              │   MODEL + DATABASE         │  ← dados, entidades, db.txt
              └────────────────────────────┘
```

- **Models:** representam as entidades do negócio (dados e comportamentos)
- **Controllers:** contêm toda a lógica de negócio e validações
- **Views:** exibem informações e recebem dados do usuário — sem lógica de negócio
- **Database:** persiste todos os dados em `db.txt` no formato JSON

---

## Mapeamento das Sprints

O projeto será desenvolvido em **7 sprints de 2h40min** cada.

---

### Sprint 1 — Planejamento e Modelagem ✅ Concluído

**Objetivo:** entender o domínio do problema e documentar antes de codar.

**O que fazer:**
- Ler o enunciado completo e levantar dúvidas
- Identificar todas as entidades do sistema e seus atributos
- Construir o **Diagrama MER** (Modelo Entidade-Relacionamento) com todas as relações
- Esboçar os menus CLI de cada funcionalidade

**Entregáveis:**
- `docs/mer.pdf` — diagrama MER completo
- Esboço dos menus de cada tela

---

### Sprint 2 — Estrutura do Projeto e Views 🔄 Em andamento

**Objetivo:** criar o esqueleto do projeto e implementar todas as interfaces de menu.

**O que fazer:**

**Parte 1 — Estrutura de pastas**
Criar a organização abaixo na raiz do projeto:
```
sistema-pizzaria/
├── controllers/
│   └── __init__.py
├── docs/
│   └── README.md
├── models/
│   └── __init__.py
├── views/
│   └── __init__.py
├── main.py
└── README.md
```

**Parte 2 — Criar os 6 arquivos de view**

| Arquivo | Menu |
|---------|------|
| `views/menu_view.py` | Menu principal (opções 1–5 + sair) |
| `views/cliente_view.py` | Cadastrar, listar, buscar cliente |
| `views/produto_view.py` | Cadastrar, listar, buscar produto |
| `views/mesa_view.py` | Cadastrar, listar, ocupar, liberar |
| `views/pedido_view.py` | Abrir, adicionar item, fechar, listar |
| `views/pagamento_view.py` | Processar pagamento, fechamento do dia |

Cada view deve ter a estrutura:
```python
class ClienteView:
    def __init__(self, controller):
        self._controller = controller

    def executar(self):
        while True:
            # exibe menu, lê opção, chama método privado ou break
            ...

    def _cadastrar(self): pass
    def _listar(self):    pass
    def _buscar(self):    pass
```

> Os controllers ainda não existem — os métodos privados ficam com `pass` por enquanto.

**Entregáveis:**
- Estrutura de pastas correta com `__init__.py` em cada pacote
- 6 views implementadas com menus funcionando (loop + opções)

---

### Sprint 3 — Camada de Models ⏳ Pendente

**Objetivo:** implementar as 7 entidades do sistema com POO.

**O que fazer:**

| Arquivo | Atributos principais | Comportamentos |
|---------|---------------------|----------------|
| `models/cliente.py` | `id`, `nome`, `telefone` | getters/setters, `__str__` |
| `models/produto.py` | `id`, `nome`, `preco`, `categoria` | setter valida preço > 0, `__str__` |
| `models/estoque.py` | `produto_id`, `quantidade` | `adicionar()`, `remover()`, `tem_disponivel()` |
| `models/mesa.py` | `id`, `numero`, `status` | `ocupar()`, `liberar()`, `esta_livre()` |
| `models/item_pedido.py` | `id`, `pedido_id`, `produto_id`, `preco_unitario`, `quantidade` | `subtotal` (calculado) |
| `models/pedido.py` | `id`, `mesa_id`, `status`, `itens`, `total` | `adicionar_item()`, `fechar()`, `marcar_pago()` |
| `models/pagamento.py` | `id`, `pedido_id`, `valor`, `metodo` | `METODOS_ACEITOS`, `__str__` |

**Regra importante:** os models **não acessam o banco**. Eles só representam os dados na memória.

**Entregáveis:**
- 7 arquivos em `models/` funcionando
- Todas as entidades instanciáveis e com `__str__`

---

### Sprint 4 — Controllers Parte 1 ⏳ Pendente

**Objetivo:** implementar a lógica de negócio dos três primeiros controllers e conectar às views.

**O que fazer:**

**`ClienteController`**
- `cadastrar(nome, telefone)` — valida nome não vazio, lança `ValueError` se inválido
- `listar()` — retorna todos os clientes
- `buscar_por_id(id)` — retorna `Cliente` ou `None`
- `buscar_por_nome(nome)` — busca parcial, case-insensitive

**`ProdutoController`**
- `cadastrar(nome, preco, categoria)` — valida nome e preço > 0
- `listar()`, `buscar_por_id(id)`

**`EstoqueController`**
- `inicializar(produto_id, quantidade)` — cria estoque para o produto
- `adicionar(produto_id, quantidade)` — erro se produto sem estoque ou qtd ≤ 0
- `remover(produto_id, quantidade)` — remove se houver disponibilidade
- `verificar_disponibilidade(produto_id, quantidade)` — retorna `True/False`
- `listar()`

**Conectar views:**
- `views/cliente_view.py` → implementar `_cadastrar`, `_listar`, `_buscar`
- `views/produto_view.py` → implementar todos os métodos

> **Regra de ouro:** a view nunca acessa atributos internos do controller. Só chama métodos públicos.

**Entregáveis:**
- 3 controllers funcionando com validações
- Views de cliente e produto operacionais

---

### Sprint 5 — Controllers Parte 2 e Persistência ⏳ Pendente

**Objetivo:** implementar os controllers restantes, criar a persistência em arquivo e conectar todas as views.

**O que fazer:**

**`models/database.py` — a camada de persistência**

```python
class Database:
    @staticmethod
    def carregar() -> dict:
        # lê db.txt (JSON); se não existir, retorna estrutura padrão vazia

    @staticmethod
    def salvar(dados: dict):
        # grava todos os dados em db.txt formatado
```

**Padrão de persistência nos controllers:**
```python
def _carregar(self):
    dados = Database.carregar()
    # reconstrói objetos a partir do dict

def _salvar(self):
    dados = Database.carregar()   # lê tudo primeiro
    dados["clientes"] = [...]     # atualiza só a sua seção
    Database.salvar(dados)        # grava tudo de volta
```

> `_carregar()` é chamado no `__init__`. `_salvar()` é chamado após toda operação que altera dados.

**`MesaController`** — `cadastrar`, `listar`, `listar_livres`, `ocupar`, `liberar`, `buscar_por_id`

**`PedidoController`** *(recebe `mesa_ctrl`, `produto_ctrl`, `estoque_ctrl` no construtor)*
- `abrir(mesa_id, cliente_id)` — valida mesa livre → ocupa → cria pedido
- `adicionar_item(pedido_id, produto_id, quantidade)` — valida estoque → debita → recalcula total
- `fechar(pedido_id)` — exige pelo menos um item

**`PagamentoController`** *(recebe `pedido_ctrl` no construtor)*
- `processar(pedido_id, metodo)` — valida método → fecha pedido → registra pagamento → libera mesa
- `fechamento_do_dia()` — retorna total de pedidos pagos e faturamento
- `listar()`

**Entregáveis:**
- `models/database.py` funcionando
- Todos os 6 controllers com persistência
- `db.txt` criado automaticamente
- Todas as 6 views conectadas

---

### Sprint 6 — Integração e Finalização ⏳ Pendente

**Objetivo:** unir todas as camadas no `main.py`, validar o sistema completo e documentar.

**O que fazer:**

**`main.py` — ponto de entrada**
```python
# instanciar controllers com injeção de dependência
pedido_ctrl    = PedidoController(mesa_ctrl, produto_ctrl, estoque_ctrl)
pagamento_ctrl = PagamentoController(pedido_ctrl)

# iniciar o menu principal
menu = MenuView(...)
menu.executar()
```

**Roteiro de validação manual** (executar do zero):
1. Cadastrar um cliente
2. Cadastrar dois produtos com estoque
3. Cadastrar três mesas
4. Abrir pedido → adicionar itens → fechar → pagar
5. Verificar fechamento do dia
6. Fechar o sistema e reabrir — **os dados devem persistir**

**`README.md`** — documentar o projeto:
- Descrição, tecnologias, estrutura de arquivos, como executar, regras de negócio

**Entregáveis:**
- `main.py` funcional com injeção de dependências
- Sistema 100% operacional via `python main.py`
- Dados persistindo entre sessões em `db.txt`
- `README.md` finalizado

---

### Sprint 7 — Backlog e Roda de Conversa ⏳ Pendente

**Objetivo:** reflexão sobre o projeto desenvolvido, discussão em grupo e registro do aprendizado.

**O que fazer:**
- Demonstrar o sistema funcionando para a turma
- Discutir em grupo: o que foi mais difícil? O que faria diferente?
- Levantar melhorias e funcionalidades que ficaram no backlog
- Registrar aprendizados sobre MVC, POO, persistência e arquitetura de software

**Sugestões de backlog para discussão:**
- Relatório de vendas por período
- Desconto e cupom no pedido
- Múltiplos atendentes com login
- Exportação do fechamento em `.csv`
- Testes automatizados

---

## Resumo Geral

| Sprint | Dia | Tema | Principais Entregas |
|--------|-----|------|---------------------|
| Sprint 1 | Dia 1 ✅ | Planejamento e MER | `docs/mer.pdf`, esboço dos menus |
| Sprint 2 | Dia 2 🔄 | Estrutura e Views | 6 views, estrutura de pastas |
| Sprint 3 | Dia 3 | Models | 7 entidades em `models/` |
| Sprint 4 | Dia 4 | Controllers Parte 1 | 3 controllers + views de cliente/produto |
| Sprint 5 | Dia 5 | Controllers Parte 2 + Persistência | 3 controllers + `database.py` + todas as views |
| Sprint 6 | Dia 6 | Integração e Finalização | `main.py`, sistema rodando, `README.md` |
| Sprint 7 | Dia 7 | Backlog e Roda de Conversa | Demonstração + reflexão em grupo |

---

## Estrutura Final do Projeto

```
sistema-pizzaria/
├── controllers/
│   ├── __init__.py
│   ├── cliente_controller.py
│   ├── estoque_controller.py
│   ├── mesa_controller.py
│   ├── pagamento_controller.py
│   ├── pedido_controller.py
│   └── produto_controller.py
├── docs/
│   ├── mer.pdf
│   └── README.md
├── models/
│   ├── __init__.py
│   ├── cliente.py
│   ├── database.py
│   ├── estoque.py
│   ├── item_pedido.py
│   ├── mesa.py
│   ├── pagamento.py
│   ├── pedido.py
│   └── produto.py
├── views/
│   ├── __init__.py
│   ├── cliente_view.py
│   ├── menu_view.py
│   ├── mesa_view.py
│   ├── pagamento_view.py
│   ├── pedido_view.py
│   └── produto_view.py
├── db.txt        ← gerado automaticamente pelo sistema
├── main.py
└── README.md
```
