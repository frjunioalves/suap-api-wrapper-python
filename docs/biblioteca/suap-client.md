# SuapClient

Cliente principal para a API do SUAP. Ponto de entrada da biblioteca.

```python
from suap_api import SuapClient
```

---

## Construtor

```python
SuapClient(
    base_url: str | None = None,
    username: str | None = None,
    password: str | None = None,
    token: str | None = None,
)
```

### Parâmetros

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `base_url` | `str \| None` | URL base da instância SUAP (ex: `"https://suap.ifpi.edu.br"`). Se `None`, carrega da sessão salva. |
| `username` | `str \| None` | Matrícula do aluno. Usado com `password` para autenticação automática. |
| `password` | `str \| None` | Senha da conta SUAP. Usado com `username`. |
| `token` | `str \| None` | Access token JWT para uso imediato, sem autenticação. |

### Exceções levantadas no construtor

| Exceção | Quando |
|---|---|
| `SuapAuthError` | `username`/`password` inválidos |
| `SuapNotLoggedInError` | Chamado sem argumentos e sem sessão salva |

---

## Atributos públicos

| Atributo | Tipo | Descrição |
|---|---|---|
| `base_url` | `str` | URL base normalizada da instância SUAP |
| `TIMEOUT` | `int` | Timeout em segundos para todas as requisições (padrão: `10`) |
| `token` | `TokenResource` | Recurso de autenticação |
| `comum` | `CommonResource` | Recurso de dados comuns |
| `edu` | `EduResource` | Recurso do módulo acadêmico |

---

## Context manager

O cliente implementa `__enter__` e `__exit__` para uso com `with`:

```python
# A sessão HTTP é fechada automaticamente ao sair do bloco
with SuapClient() as client:
    dados = client.comum.get_my_data()
```

---

## Exemplos

=== "Sessão salva"

    ```python
    with SuapClient() as client:
        dados = client.comum.get_my_data()
    ```

=== "Credenciais diretas"

    ```python
    with SuapClient(
        base_url="https://suap.ifpi.edu.br",
        username="20221234",
        password="minha_senha",
    ) as client:
        dados = client.comum.get_my_data()
    ```

=== "Token manual"

    ```python
    with SuapClient(
        base_url="https://suap.ifpi.edu.br",
        token="eyJ0eXAiOiJKV1Qi...",
    ) as client:
        dados = client.comum.get_my_data()
    ```

---

## Renovação automática de token

Quando uma requisição retorna HTTP 401, o cliente tenta renovar o access token
usando o refresh token antes de repetir a requisição. Isso é transparente para o
código consumidor.

Se o refresh também falhar, levanta `SuapTokenExpiredError`.

!!! note
    A renovação automática só ocorre nos modos **sessão salva** e
    **credenciais diretas**. No modo **token manual** não há refresh token
    disponível.
