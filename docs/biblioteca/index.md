# Biblioteca Python — Visão Geral

O `suap-api-wrapper` pode ser usado diretamente como biblioteca Python para integrar dados do SUAP em scripts, bots ou aplicações.

---

## Quando usar a biblioteca vs. a CLI

| Cenário | Recomendado |
|---|---|
| Consulta rápida no terminal | CLI (`suap periodos`) |
| Script que processa dados automaticamente | Biblioteca |
| Bot de notificação (Discord, Telegram…) | Biblioteca |
| Aplicação web que exibe dados do SUAP | Biblioteca |
| Integração com outras ferramentas Python | Biblioteca |

---

## Os três modos de inicialização

### Modo 1 — Sessão salva

Requer que o usuário tenha executado `suap login` previamente.
Lê a URL base e os tokens de `~/.suap/`.

```python
from suap_api import SuapClient

with SuapClient() as client:
    dados = client.comum.get_my_data()
```

### Modo 2 — Credenciais diretas

Autentica no momento da criação, sem depender de sessão salva.
Útil em scripts automatizados com credenciais em variáveis de ambiente.

```python
import os
from suap_api import SuapClient

with SuapClient(
    base_url="https://suap.ifpi.edu.br",
    username=os.environ["SUAP_USER"],
    password=os.environ["SUAP_PASS"],
) as client:
    dados = client.comum.get_my_data()
```

### Modo 3 — Token manual

Para quem já possui um access token JWT obtido por outro meio.

```python
from suap_api import SuapClient

with SuapClient(
    base_url="https://suap.ifpi.edu.br",
    token="eyJ0eXAiOiJKV1Qi...",
) as client:
    dados = client.comum.get_my_data()
```

!!! warning
    No modo 3 não há refresh automático — se o token expirar, uma `SuapTokenExpiredError` será levantada.

---

## Context manager

O `SuapClient` implementa o protocolo de context manager (`__enter__` / `__exit__`).
O uso com `with` garante que a sessão HTTP seja fechada corretamente ao final:

```python
# Correto — sessão fechada automaticamente
with SuapClient() as client:
    ...

# Também funciona, mas você precisa fechar manualmente
client = SuapClient()
try:
    ...
finally:
    client._session.close()
```

---

## Recursos disponíveis

O cliente organiza os endpoints em três recursos:

| Atributo | Classe | Endpoints |
|---|---|---|
| `client.token` | `TokenResource` | Autenticação JWT |
| `client.comum` | `CommonResource` | Dados pessoais |
| `client.edu` | `EduResource` | Módulo acadêmico completo |

---

## Acesso ao JSON original

Todo objeto retornado pela biblioteca expõe um atributo `.raw` com o dicionário original recebido da API, antes de qualquer conversão ou limpeza de dados. Isso é útil para depuração, logging ou acesso a campos ainda não mapeados nos modelos.

```python
with SuapClient() as client:
    dados = client.comum.get_my_data()

    # JSON completo retornado pela API
    print(dados.raw)

    # Funciona em objetos aninhados também
    print(dados.vinculo.raw)

    disciplinas = client.edu.get_disciplines("2024.1")
    print(disciplinas[0].raw)           # dict da disciplina
    print(disciplinas[0].notas[0].raw)  # dict da nota
```

O atributo `.raw` nunca é `None` — retorna um `dict` vazio `{}` se o modelo for construído manualmente, fora do fluxo normal da API.

!!! note
    O `.raw` preserva todos os campos da resposta da API, inclusive os que não têm mapeamento no modelo. Campos de texto que o cliente normaliza para `None` (ex: `"NoneNone"`) aparecem com o valor original no `.raw`.

---

## Exemplo completo

```python
from suap_api import SuapClient, SuapNotFoundError

with SuapClient() as client:
    # Dados pessoais
    dados = client.comum.get_my_data()
    print(f"Olá, {dados.nome_usual}!")

    # Semestres e diários
    periodos = client.edu.get_periods()
    ultimo = periodos[0].semestre
    diarios = client.edu.get_diaries(ultimo)

    for diario in diarios:
        id_d = diario.id
        try:
            materiais = client.edu.get_diary_materials(id_d)
            if materiais:
                pdf = client.edu.get_material_pdf(id_d, materiais[0].id)
                with open(f"material_{id_d}.pdf", "wb") as f:
                    f.write(pdf)
        except SuapNotFoundError:
            pass
```
