# Plano: Documentação com MkDocs — suap-api-wrapper

## Objetivo

Criar um site de documentação para a biblioteca `suap-api-wrapper` usando [MkDocs](https://www.mkdocs.org/) com o tema [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/). A documentação deve cobrir tanto o uso da CLI quanto o uso programático via `SuapClient`.

---

## Estrutura de páginas

```
docs/
├── index.md                  # Página inicial (visão geral + quick start)
├── instalacao.md             # Requisitos e como instalar
├── autenticacao.md           # Login, logout, onde os tokens são salvos
├── cli/
│   ├── index.md              # Visão geral da CLI
│   ├── comum.md              # Comando meus-dados
│   └── edu.md                # Comandos edu: periodos, diarios, aulas…
├── biblioteca/
│   ├── index.md              # Visão geral do SuapClient
│   ├── suap-client.md        # Referência de SuapClient (init, context manager)
│   ├── recursos-comum.md     # Referência de CommonResource
│   └── recursos-edu.md       # Referência de EduResource
├── excecoes.md               # Hierarquia de exceções e quando cada uma ocorre
├── seguranca.md              # Armazenamento de tokens, SSL, timeouts
└── contribuindo.md           # Como rodar testes, mypy, estrutura do projeto
```

---

## Conteúdo por página

### `index.md` — Página inicial
- O que é o `suap-api-wrapper` e para quem serve
- Compatibilidade: qualquer instituição com SUAP (IFPI, IFRN, IFCE…)
- Quick start em 3 passos: instalar → `suap login` → primeiro comando
- Dois exemplos lado a lado: uso via CLI e uso como biblioteca

### `instalacao.md`
- Requisitos: Python 3.8+
- `pip install .` (a partir do clone)
- `pip install ".[dev]"` para desenvolvimento
- Verificar instalação: `suap --help`

### `autenticacao.md`
- Fluxo de autenticação: JWT com access token + refresh token automático
- `suap login`: campos solicitados (URL, matrícula, senha com `*`)
- Formatos de URL aceitos pelo `normalize_url`: `suap.ifpi.edu.br`, `https://…`, `https://…/api/v2`
- `suap logout`
- Onde os arquivos são salvos: `~/.suap/config.json` e `~/.suap/tokens.json`
- Renovação automática do token (sem intervenção do usuário)

### `cli/index.md`
- Listagem de todos os comandos com descrição curta (tabela)
- Como a saída é sempre JSON (para uso com `jq`, scripts, etc.)

### `cli/comum.md`
- `suap meus-dados`

### `cli/edu.md`
- `suap periodos`
- `suap diarios <semestre>`
- `suap disciplinas <semestre>`
- `suap dados-aluno`
- `suap conclusao`
- `suap diarios <id_diario>` → lista de comandos que precisam de ID de diário
- `suap professores <id_diario>`
- `suap aulas <id_diario>`
- `suap materiais <id_diario>`
- `suap material <id_material>`
- `suap trabalhos <id_diario>`
- `suap material-pdf <id_diario> <id_material>`
- Fluxo típico de uso: sequência encadeada de comandos com exemplos reais

### `biblioteca/index.md`
- Quando usar como biblioteca vs. CLI
- Os três modos de inicialização do `SuapClient`:
  1. Sessão salva (`SuapClient()`)
  2. Credenciais diretas (`base_url` + `username` + `password`)
  3. Token manual (`base_url` + `token`)
- Uso como context manager (`with SuapClient() as client`)

### `biblioteca/suap-client.md`
- Referência completa de `SuapClient.__init__`
- Atributos públicos: `base_url`, `TIMEOUT`, `token`, `comum`, `edu`
- Métodos do context manager

### `biblioteca/recursos-comum.md`
- `client.comum.get_my_data()` — parâmetros, retorno, exceções, exemplo

### `biblioteca/recursos-edu.md`
- `client.edu.get_periods()`
- `client.edu.get_diaries(semestre)`
- `client.edu.get_diary_professors(id_diario)`
- `client.edu.get_diary_classes(id_diario)`
- `client.edu.get_diary_materials(id_diario)`
- `client.edu.get_material(id_material)`
- `client.edu.get_material_pdf(id_diario, id_material)`
- `client.edu.get_diary_assignments(id_diario)`
- `client.edu.get_disciplines(semestre)`
- `client.edu.get_student_data()`
- `client.edu.get_graduation_requirements()`

### `excecoes.md`
- Hierarquia de herança (diagrama em texto/Mermaid)
- Tabela: exceção → quando ocorre → status HTTP associado
- Exemplo de tratamento com `try/except` múltiplos

### `seguranca.md`
- Permissão `600` nos arquivos de token e config
- SSL sempre verificado (sem opção de desativar)
- Timeout de 10 s em todas as requisições
- Recomendação: não hardcodar senhas no código

### `contribuindo.md`
- Estrutura do repositório
- Rodar testes: `pytest tests/ -v`
- Checagem de tipos: `mypy suap_api/`
- Como adicionar um novo endpoint (passo a passo: recurso → CLI → teste)

---

## Configuração do MkDocs (`mkdocs.yml`)

```yaml
site_name: suap-api-wrapper
site_description: Python wrapper e CLI para a API v2 do SUAP
repo_url: https://github.com/<usuario>/suap-api-wrapper

theme:
  name: material
  language: pt
  palette:
    - scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Modo escuro
    - scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Modo claro
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.top
    - content.code.copy

markdown_extensions:
  - admonition
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.tabbed:
      alternate_style: true
  - tables
  - toc:
      permalink: true

nav:
  - Início: index.md
  - Instalação: instalacao.md
  - Autenticação: autenticacao.md
  - CLI:
      - Visão Geral: cli/index.md
      - Módulo Comum: cli/comum.md
      - Módulo Edu: cli/edu.md
  - Biblioteca Python:
      - Visão Geral: biblioteca/index.md
      - SuapClient: biblioteca/suap-client.md
      - CommonResource: biblioteca/recursos-comum.md
      - EduResource: biblioteca/recursos-edu.md
  - Exceções: excecoes.md
  - Segurança: seguranca.md
  - Contribuindo: contribuindo.md
```

---

## Dependências a adicionar

Em `pyproject.toml`, nova seção `[project.optional-dependencies]`:

```toml
[project.optional-dependencies]
docs = [
    "mkdocs>=1.5",
    "mkdocs-material>=9.0",
    "pymdown-extensions>=10.0",
]
```

Instalar com:

```bash
pip install ".[docs]"
```

Visualizar localmente:

```bash
mkdocs serve
```

Build estático (para deploy):

```bash
mkdocs build
```

---

## Ordem de implementação sugerida

1. Criar `mkdocs.yml` na raiz e instalar dependências (`.[docs]`)
2. Criar `docs/index.md` com quick start funcional
3. `docs/instalacao.md` e `docs/autenticacao.md`
4. Seção CLI completa (`docs/cli/`)
5. Seção Biblioteca (`docs/biblioteca/`)
6. `docs/excecoes.md` com diagrama Mermaid da hierarquia
7. `docs/seguranca.md` e `docs/contribuindo.md`
8. Revisar navegação no `mkdocs.yml` e testar `mkdocs serve`
9. Configurar deploy (GitHub Actions → GitHub Pages ou Read the Docs)

---

## Extras opcionais

- **GitHub Actions** para publicar automaticamente em GitHub Pages a cada push na `main`
- **Badges** no `index.md`: versão do Python, licença, status do CI
- **Diagrama Mermaid** na página de exceções para mostrar a hierarquia `SuapError → …`
- **Tabs** nas páginas da biblioteca para alternar entre exemplo de código e saída esperada
- **Admonitions** (`!!! warning`, `!!! tip`) para destacar comportamentos importantes (ex: renovação automática de token, onde as senhas são salvas)
