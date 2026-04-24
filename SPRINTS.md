# Sprints Diárias — Sistema de Gerenciamento de Pizzaria

> **Carga horária por sprint:** 2h40min  
> **Total:** 7 dias · Arquitetura MVC · Python puro (sem bibliotecas externas)

---

## Visão Geral

| Sprint | Dia | Status | Tema |
|--------|-----|--------|------|
| Sprint 1 | Dia 1 | ✅ Concluído | Planejamento, MER e Design das Interfaces |
| Sprint 2 | Dia 2 | 🔄 Em andamento | Estrutura do Projeto e Criação das Views |
| Sprint 3 | Dia 3 | ⏳ Pendente | Camada de Models |
| Sprint 4 | Dia 4 | ⏳ Pendente | Controllers — Parte 1 |
| Sprint 5 | Dia 5 | ⏳ Pendente | Controllers — Parte 2 e Persistência |
| Sprint 6 | Dia 6 | ⏳ Pendente | Integração, main.py e Finalização |
| Sprint 7 | Dia 7 | ⏳ Pendente | backlog do sistema completo |

---

## Sprint 1 — Planejamento, MER e Design das Interfaces
**Duração:** 2h40min &nbsp;|&nbsp; **Status:** ✅ Concluído

### Objetivo
Entender o domínio do sistema, modelar as entidades e esboçar as interfaces de linha de comando.

### Tarefas
- [ ] Ler o enunciado e entender as regras de negócio da pizzaria
- [ ] Identificar as entidades: `Cliente`, `Produto`, `Estoque`, `Mesa`, `Pedido`, `ItemPedido`, `Pagamento`
- [ ] Criar o diagrama MER com todos os relacionamentos
- [ ] Documentar as entidades e atributos em `docs/mer.pdf`
- [ ] Esboçar os menus CLI de cada entidade (no papel ou digitalmente)

### Entregáveis
- `docs/README.md` com diagrama MER e descrição das entidades
- Esboço dos menus CLI

---

## Sprint 2 — Estrutura do Projeto e Criação das Views
**Duração:** 2h40min &nbsp;|&nbsp; **Status:** 🔄 Em andamento

### Objetivo
Montar a estrutura de pastas do projeto e criar os arquivos de interface (views) com os menus CLI implementados.

---

### Parte 1 — Continuação do Sprint 1 *(se necessário)*
- [ ] Revisar e finalizar o diagrama MER
- [ ] Complementar a documentação em `docs/README.md`

---

### Parte 2 — Estrutura do Projeto *(nova tarefa)*

Criar a seguinte estrutura de pastas e arquivos na raiz do projeto:

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
├── main.py          ← arquivo vazio por enquanto
└── README.md        ← descrição geral (pode ficar vazio por enquanto)
```

> **Dica:** os arquivos `__init__.py` ficam vazios. Eles apenas dizem ao Python que a pasta é um pacote importável.

---

### Parte 3 — Criação dos Arquivos de Views *(nova tarefa)*

Criar os 6 arquivos de view dentro de `views/`:

| Arquivo | Responsabilidade |
|---------|-----------------|
| `views/menu_view.py` | Menu principal com opções 1–5 e saída (0) |
| `views/cliente_view.py` | Submenu: cadastrar, listar, buscar cliente |
| `views/produto_view.py` | Submenu: cadastrar, listar, buscar produto |
| `views/mesa_view.py` | Submenu: cadastrar, listar, ocupar, liberar mesa |
| `views/pedido_view.py` | Submenu: abrir pedido, adicionar item, fechar pedido, listar |
| `views/pagamento_view.py` | Submenu: processar pagamento, fechamento do dia |

#### Requisitos de cada view
- Cada view recebe seu respectivo **controller por parâmetro no construtor** (`__init__`)
- Implementar método `executar()` com loop do menu (`while True`)
- Usar `input()` para capturar dados e `print()` para exibir resultados
- Tratar entradas inválidas com `try/except ValueError`
- Ao selecionar "0" ou "Voltar", encerrar o loop e retornar ao menu principal
- Os controllers **ainda não existem** — por enquanto, apenas monte os menus (pode deixar os métodos com `pass` ou `print("Em breve...")`)

#### Exemplo de estrutura esperada para `views/cliente_view.py`

```python
class ClienteView:
    def __init__(self, controller):
        self._controller = controller

    def executar(self):
        while True:
            print("\n===== CLIENTES =====")
            print("1 - Cadastrar cliente")
            print("2 - Listar clientes")
            print("3 - Buscar por nome")
            print("0 - Voltar")
            opcao = input("Opção: ").strip()

            if opcao == "1":
                self._cadastrar()
            elif opcao == "2":
                self._listar()
            elif opcao == "3":
                self._buscar()
            elif opcao == "0":
                break
            else:
                print("Opção inválida.")

    def _cadastrar(self):
        pass  # será implementado no Sprint 4

    def _listar(self):
        pass

    def _buscar(self):
        pass
```

### Entregáveis
- Estrutura de pastas criada corretamente
- 6 arquivos de view em `views/` com menus funcionando
- `__init__.py` em `views/`, `models/` e `controllers/`

---

## Sprint 3 — Camada de Models
**Duração:** 2h40min &nbsp;|&nbsp; **Status:** ⏳ Pendente

### Objetivo
Implementar as entidades do sistema com POO — atributos, propriedades, validações e representação em string.

### Tarefas

#### `models/cliente.py`
- Atributos: `id`, `nome`, `telefone`
- Propriedades com getter e setter
- `__str__` retornando dados formatados

#### `models/produto.py`
- Atributos: `id`, `nome`, `preco`, `categoria`
- Setter de `preco` deve rejeitar valores ≤ 0
- `__str__` com nome e preço formatado (`R$ X.XX`)

#### `models/estoque.py`
- Atributos: `produto_id`, `quantidade`
- `adicionar(qtd)`: ignora valores ≤ 0
- `remover(qtd)`: retorna `False` se quantidade insuficiente
- `tem_disponivel(qtd)`: retorna `True/False`

#### `models/mesa.py`
- Atributos: `id`, `numero`, `status`
- Constantes: `STATUS_LIVRE = "livre"`, `STATUS_OCUPADA = "ocupada"`
- Métodos: `ocupar()`, `liberar()`, `esta_livre()`

#### `models/item_pedido.py`
- Atributos: `id`, `pedido_id`, `produto_id`, `nome_produto`, `preco_unitario`, `quantidade`
- Propriedade calculada: `subtotal = preco_unitario * quantidade`

#### `models/pedido.py`
- Atributos: `id`, `mesa_id`, `cliente_id`, `status`, `itens`, `total`
- Status válidos: `"aberto"` → `"fechado"` → `"pago"`
- `adicionar_item(item)`: adiciona à lista e recalcula `total` automaticamente
- Métodos: `fechar()`, `marcar_pago()`, `esta_aberto()`, `esta_pago()`

#### `models/pagamento.py`
- Atributos: `id`, `pedido_id`, `valor`, `metodo`
- Constante: `METODOS_ACEITOS = ["dinheiro", "cartao_credito", "cartao_debito", "pix"]`
- `__str__` com valor e método formatados

### Entregáveis
- 7 arquivos de model em `models/`
- Todas as entidades instanciáveis e com `__str__` funcionando

---

## Sprint 4 — Controllers — Parte 1
**Duração:** 2h40min &nbsp;|&nbsp; **Status:** ⏳ Pendente

### Objetivo
Implementar a lógica de negócio dos três primeiros controllers e conectá-los às views.

### Tarefas

#### `controllers/cliente_controller.py`
- `__init__`: inicializa lista vazia e `_proximo_id = 1`
- `cadastrar(nome, telefone)`: valida nome não vazio, cria e armazena `Cliente`; lança `ValueError` em caso de erro
- `listar()`: retorna cópia da lista de clientes
- `buscar_por_id(id)`: retorna `Cliente` ou `None`
- `buscar_por_nome(nome)`: retorna lista com correspondências parciais (case-insensitive)

#### `controllers/produto_controller.py`
- `cadastrar(nome, preco, categoria)`: valida nome e preço > 0, cria `Produto`
- `listar()`: retorna todos os produtos
- `buscar_por_id(id)`: retorna `Produto` ou `None`

#### `controllers/estoque_controller.py`
- `inicializar(produto_id, quantidade)`: cria estoque inicial para um produto
- `adicionar(produto_id, quantidade)`: adiciona ao estoque existente; erro se produto sem estoque ou qtd ≤ 0
- `remover(produto_id, quantidade)`: remove se houver disponibilidade
- `verificar_disponibilidade(produto_id, quantidade)`: retorna `True/False`
- `listar()`: retorna todos os estoques

#### Conectar Views com Controllers
- Atualizar `views/cliente_view.py`: implementar `_cadastrar`, `_listar`, `_buscar` usando `ClienteController`
- Atualizar `views/produto_view.py`: implementar métodos usando `ProdutoController`

> **Lembre-se:** a view só chama métodos do controller. Nunca acesse diretamente os atributos internos do controller a partir da view.

### Entregáveis
- 3 controllers implementados e validados manualmente
- Views de cliente e produto 100% funcionais com lógica de negócio

---

## Sprint 5 — Controllers — Parte 2 e Persistência
**Duração:** 2h40min &nbsp;|&nbsp; **Status:** ⏳ Pendente

### Objetivo
Implementar os controllers restantes, criar a camada de persistência em arquivo e conectar todas as views.

### Tarefas

#### `models/database.py` — Persistência JSON

Criar a classe `Database` com dois métodos estáticos:

```python
import json, os

_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db.txt")

_ESTRUTURA_PADRAO = {
    "clientes": [], "produtos": [], "estoques": {},
    "mesas": [], "pedidos": [], "pagamentos": [],
    "contadores": {
        "cliente": 1, "produto": 1, "mesa": 1,
        "pedido": 1, "item": 1, "pagamento": 1
    }
}

class Database:
    @staticmethod
    def carregar() -> dict:
        # lê db.txt e retorna dict; se não existir, retorna _ESTRUTURA_PADRAO

    @staticmethod
    def salvar(dados: dict):
        # serializa e grava dados em db.txt (indent=2)
```

#### Adicionar `_carregar` e `_salvar` a **todos os controllers**

Padrão obrigatório:
- `_carregar()` chamado no `__init__` para restaurar estado do arquivo
- `_salvar()` chamado após toda operação que altera dados (cadastrar, ocupar, remover, etc.)
- Sempre leia o banco completo, atualize **apenas sua seção**, grave de volta — nunca sobrescreva seções de outros controllers

```python
def _salvar(self):
    dados = Database.carregar()          # lê tudo
    dados["clientes"] = [...]            # atualiza só esta seção
    dados["contadores"]["cliente"] = ... # atualiza contador
    Database.salvar(dados)               # grava tudo
```

#### `controllers/mesa_controller.py`
- `cadastrar(numero)`: valida número único, cria `Mesa`; persiste
- `listar()`, `listar_livres()`
- `ocupar(mesa_id)`: retorna `False` se já ocupada; persiste
- `liberar(mesa_id)`: persiste
- `buscar_por_id(id)`

#### `controllers/pedido_controller.py`
- Recebe `mesa_ctrl`, `produto_ctrl`, `estoque_ctrl` no construtor (injeção de dependência)
- `abrir(mesa_id, cliente_id)`: valida mesa livre → ocupa → cria `Pedido`; persiste
- `adicionar_item(pedido_id, produto_id, quantidade)`: valida estoque → cria `ItemPedido` → debita estoque → recalcula total; persiste
- `fechar(pedido_id)`: valida que pedido tem itens → muda status; persiste
- `listar_abertos()`, `buscar_por_id(id)`

#### `controllers/pagamento_controller.py`
- Recebe `pedido_ctrl` no construtor
- `processar(pedido_id, metodo)`: valida método → fecha pedido se ainda aberto → cria `Pagamento` → marca pedido como pago → libera mesa; persiste
- `fechamento_do_dia()`: retorna `{"pedidos_pagos": N, "faturamento_total": X.XX}`
- `listar()`

#### Conectar views restantes
- `views/mesa_view.py` → `MesaController`
- `views/pedido_view.py` → `PedidoController`
- `views/pagamento_view.py` → `PagamentoController`

### Entregáveis
- `models/database.py` implementado
- Todos os 6 controllers com `_carregar`/`_salvar` funcionando
- `db.txt` sendo criado automaticamente ao executar qualquer operação
- Todas as 6 views conectadas e funcionais

---

## Sprint 6 — Integração, main.py e Finalização
**Duração:** 2h40min &nbsp;|&nbsp; **Status:** ⏳ Pendente

### Objetivo
Integrar todas as camadas, criar o ponto de entrada da aplicação e finalizar o projeto.

### Tarefas

#### `main.py` — Entry Point

Instanciar todos os controllers com injeção de dependência e iniciar o menu principal:

```python
from controllers.cliente_controller import ClienteController
from controllers.produto_controller import ProdutoController
from controllers.estoque_controller import EstoqueController
from controllers.mesa_controller import MesaController
from controllers.pedido_controller import PedidoController
from controllers.pagamento_controller import PagamentoController
from views.menu_view import MenuView

cliente_ctrl    = ClienteController()
produto_ctrl    = ProdutoController()
estoque_ctrl    = EstoqueController()
mesa_ctrl       = MesaController()
pedido_ctrl     = PedidoController(mesa_ctrl, produto_ctrl, estoque_ctrl)
pagamento_ctrl  = PagamentoController(pedido_ctrl)

menu = MenuView(cliente_ctrl, produto_ctrl, estoque_ctrl,
                mesa_ctrl, pedido_ctrl, pagamento_ctrl)
menu.executar()
```

#### Validação do Fluxo Completo

Execute manualmente o seguinte roteiro para validar que o sistema está 100% funcional:

1. Cadastrar um cliente
2. Cadastrar dois produtos e inicializar estoque de cada um
3. Cadastrar três mesas
4. Abrir um pedido em uma das mesas
5. Adicionar itens ao pedido
6. Fechar o pedido
7. Processar o pagamento (escolher um método)
8. Verificar o fechamento do dia
9. Fechar o sistema e executar novamente — os dados devem persistir em `db.txt`

#### `README.md` Principal

Criar/atualizar `README.md` na raiz do projeto com:
- Descrição do sistema
- Tecnologias utilizadas (Python 3.8+, stdlib apenas)
- Estrutura de arquivos do projeto
- Como executar: `python main.py`
- Regras de negócio principais

### Entregáveis
- `main.py` funcionando com injeção de dependências
- Sistema completo executável via `python main.py`
- `db.txt` criado e populado após execução
- Dados persistidos entre sessões (fechar e reabrir o sistema)
- `README.md` finalizado
- **Sistema 100% funcional sem erros**

---

## Resumo das Entregas por Sprint

| Sprint | Arquivos Criados | Conceito Central |
|--------|-----------------|-----------------|
| Sprint 1 | `docs/README.md` | MER, modelagem de domínio |
| Sprint 2 | `views/*.py` (6 arquivos) + estrutura de pastas | CLI, POO, separação de responsabilidades |
| Sprint 3 | `models/*.py` (7 arquivos) | Entidades, encapsulamento, herança |
| Sprint 4 | `controllers/` (3 arquivos) | Lógica de negócio, validações |
| Sprint 5 | `controllers/` (3 arquivos) + `models/database.py` | Persistência, injeção de dependência |
| Sprint 6 | `main.py`, `README.md` | Integração, arquitetura MVC completa |

---

## Estrutura Final Esperada do Projeto

```
sistema-pizzaria/
├── controllers/
│   ├── __init__.py
│   ├── cliente_controller.py
│   ├── produto_controller.py
│   ├── estoque_controller.py
│   ├── mesa_controller.py
│   ├── pedido_controller.py
│   └── pagamento_controller.py
├── docs/
│   └── README.md
├── models/
│   ├── __init__.py
│   ├── database.py
│   ├── cliente.py
│   ├── produto.py
│   ├── estoque.py
│   ├── mesa.py
│   ├── pedido.py
│   ├── item_pedido.py
│   └── pagamento.py
├── views/
│   ├── __init__.py
│   ├── menu_view.py
│   ├── cliente_view.py
│   ├── produto_view.py
│   ├── mesa_view.py
│   ├── pedido_view.py
│   └── pagamento_view.py
├── db.txt           ← gerado automaticamente
├── main.py
└── README.md
```
