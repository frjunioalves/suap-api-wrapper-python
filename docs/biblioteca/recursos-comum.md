# RecursoComum

Recurso de dados comuns da API do SUAP (`/api/comum/`).

Acessado via `client.comum`.

```python
from suap_api import SuapClient

with SuapClient() as client:
    dados = client.comum.get_my_data()
```

---

## Métodos

### `get_my_data()`

Obtém os dados pessoais do usuário autenticado.

**Endpoint:** `GET /api/comum/meus-dados/`

**Retorno:** `DadosPessoais`

```python
dados = client.comum.get_my_data()
print(dados.nome_usual)   # "João da Silva"
print(dados.matricula)    # "20221234TADS0014"
print(dados.email)        # "joao.silva@academico.ifpi.edu.br"
```

**Atributos disponíveis:**

| Atributo | Tipo |
|---|---|
| `id` | `int` |
| `matricula` | `str` |
| `nome_usual` | `str` |
| `cpf` | `str` |
| `rg` | `str` |
| `email` | `str` |
| `tipo_sanguineo` | `str` |
| `foto` | `str` |
| `data_nascimento` | `str` |
| `naturalidade` | `str` |
| `tipo_vinculo` | `str` |

**Exceções:**

| Exceção | Quando |
|---|---|
| `SuapNotLoggedInError` | Sem sessão ativa |
| `SuapTokenExpiredError` | Token expirado e não renovável |
| `SuapConnectionError` | Falha de rede ou timeout |
