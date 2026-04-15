# Contribuindo

---

## Estrutura do projeto

```
suap-api-wrapper/
├── suap_api/
│   ├── __init__.py           # exports públicos
│   ├── client.py             # SuapClient
│   ├── cli.py                # comandos Click
│   ├── config.py             # gestão de configuração (~/.suap/)
│   ├── exceptions.py         # exceções customizadas
│   └── resources/
│       ├── __init__.py
│       ├── token.py          # TokenResource
│       ├── comum.py          # CommonResource
│       └── edu.py            # EduResource
├── tests/
│   ├── __init__.py
│   ├── test_client.py
│   ├── test_cli.py
│   └── test_config.py
├── docs/                     # páginas da documentação (MkDocs)
├── claude-docs/              # planejamento interno
├── mkdocs.yml
└── pyproject.toml
```

---

## Configurar o ambiente de desenvolvimento

```bash
git clone https://github.com/Junio-Alves/suap-api-wrapper.git
cd suap-api-wrapper
pip install ".[dev]"
```

---

## Rodando os testes

```bash
pytest tests/ -v
```

---

## Checagem de tipos

```bash
mypy suap_api/
```

---

## Como adicionar um novo endpoint

Siga estas quatro etapas:

### 1. Adicione o método no recurso correto

Se o endpoint é `/api/edu/`, edite `suap_api/resources/edu.py`:

```python
def get_meu_novo_recurso(self, param: str) -> list:
    """Descrição do que o método faz.

    Realiza um ``GET /api/edu/meu-recurso/{param}``.

    Args:
        param: Descrição do parâmetro.

    Returns:
        Lista de ...

    Raises:
        SuapNotFoundError: Se ...
        SuapConnectionError: Se não for possível conectar.

    Example:
        >>> resultado = client.edu.get_meu_novo_recurso("valor")
    """
    return self._client._do_request("GET", f"/api/edu/meu-recurso/{param}")
```

### 2. Adicione o comando na CLI

Em `suap_api/cli.py`:

```python
@main.command("meu-recurso")
@click.argument("param")
def meu_recurso(param: str) -> None:
    """Descrição do comando. Exemplo: suap meu-recurso valor"""
    with handle_errors():
        with SuapClient() as client:
            _print_json(client.edu.get_meu_novo_recurso(param))
```

### 3. Escreva o teste

Em `tests/test_client.py` (usando `responses` para mockar a API):

```python
import responses

@responses.activate
def test_get_meu_novo_recurso():
    responses.add(
        responses.GET,
        "https://suap.ifpi.edu.br/api/edu/meu-recurso/valor",
        json=[{"id": 1}],
        status=200,
    )
    with SuapClient(base_url="https://suap.ifpi.edu.br", token="tok") as client:
        resultado = client.edu.get_meu_novo_recurso("valor")
    assert resultado == [{"id": 1}]
```

### 4. Documente

Adicione uma seção à página relevante em `docs/biblioteca/recursos-edu.md` e em `docs/cli/edu.md`.

---

## Visualizar a documentação localmente

```bash
pip install ".[docs]"
mkdocs serve
```

Acesse `http://127.0.0.1:8000`.

---

## Build da documentação

```bash
mkdocs build
```

O site estático é gerado em `site/`.
