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

**Retorno:** `dict`

```python
dados = client.comum.get_my_data()
```

**Exemplo de retorno:**

```json
{
  "id": 1234,
  "matricula": "20221234TADS0014",
  "nome_usual": "João da Silva",
  "cpf": "***.***.***-**",
  "rg": "1234567",
  "email": "joao.silva@academico.ifpi.edu.br",
  "tipo_sanguineo": "O+",
  "foto": "https://suap.ifpi.edu.br/media/foto.jpg",
  "data_nascimento": "2000-01-01",
  "naturalidade": "Teresina",
  "tipo_vinculo": "Aluno"
}
```

**Exceções:**

| Exceção | Quando |
|---|---|
| `SuapNotLoggedInError` | Sem sessão ativa |
| `SuapTokenExpiredError` | Token expirado e não renovável |
| `SuapConnectionError` | Falha de rede ou timeout |
