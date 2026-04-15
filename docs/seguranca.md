# Segurança

---

## Armazenamento de tokens

Após o login, dois arquivos são criados em `~/.suap/` com permissão restrita:

| Arquivo | Conteúdo | Permissão |
|---|---|---|
| `~/.suap/config.json` | URL base e matrícula | `600` (somente dono) |
| `~/.suap/tokens.json` | Access token e refresh token | `600` (somente dono) |

A permissão `600` significa que nenhum outro usuário do sistema pode ler ou modificar esses arquivos.

!!! warning "Atenção"
    Nunca compartilhe o conteúdo de `~/.suap/tokens.json`. Os tokens permitem acesso completo à sua conta SUAP enquanto válidos.

---

## SSL sempre verificado

Todas as requisições à API verificam o certificado SSL do servidor. Não há opção para desativar essa verificação.

Se a URL informada no login usar HTTP em vez de HTTPS, o wrapper automaticamente reescreve para HTTPS.

---

## Timeout em todas as requisições

Todas as requisições têm timeout padrão de **10 segundos** (`SuapClient.TIMEOUT = 10`).
Isso evita que scripts fiquem bloqueados indefinidamente por problemas de rede.

Se o timeout for atingido, uma `SuapConnectionError` é levantada.

---

## Credenciais em código

!!! danger "Nunca faça isso"
    ```python
    # ERRADO — senha exposta no código-fonte
    with SuapClient(
        base_url="https://suap.ifpi.edu.br",
        username="20221234",
        password="minha_senha_123",
    ) as client:
        ...
    ```

Use variáveis de ambiente:

```python
import os
from suap_api import SuapClient

with SuapClient(
    base_url=os.environ["SUAP_URL"],
    username=os.environ["SUAP_USER"],
    password=os.environ["SUAP_PASS"],
) as client:
    ...
```

Ou um arquivo `.env` (com a biblioteca `python-dotenv`):

```bash
# .env  —  nunca commite este arquivo
SUAP_URL=https://suap.ifpi.edu.br
SUAP_USER=20221234
SUAP_PASS=minha_senha
```

Adicione `.env` ao `.gitignore`:

```
# .gitignore
.env
~/.suap/
```

---

## Logout e limpeza

Ao executar `suap logout`, os tokens são removidos de `~/.suap/tokens.json` e o arquivo `~/.suap/config.json` é apagado.

Para remoção manual completa:

```bash
rm -rf ~/.suap/
```
