# Autenticação

## Como funciona

O SUAP usa **JWT (JSON Web Tokens)** para autenticação. O wrapper gerencia o par de tokens automaticamente:

- **Access token** — usado em todas as requisições à API. Tem validade curta.
- **Refresh token** — usado para renovar o access token quando ele expira. Não requer nova senha.

Quando o access token expira, o wrapper renova-o silenciosamente usando o refresh token. Você só precisará fazer login novamente se a sessão completa expirar.

---

## Login

```bash
suap login
```

O comando solicita três informações:

1. **URL da instância SUAP** — a URL do portal da sua instituição
2. **Matrícula** — seu número de matrícula
3. **Senha** — digitada com caracteres ocultados (`*`)

### Formatos de URL aceitos

Você pode digitar a URL em qualquer um destes formatos:

```
suap.ifpi.edu.br
https://suap.ifpi.edu.br
https://suap.ifpi.edu.br/
https://suap.ifpi.edu.br/api/v2
```

O wrapper normaliza automaticamente para `https://suap.ifpi.edu.br`.

---

## Logout

```bash
suap logout
```

Remove os tokens salvos e o arquivo de configuração. Após o logout, qualquer comando que exija sessão retornará um erro pedindo para executar `suap login`.

---

## Onde os dados são salvos

Após o login, dois arquivos são criados em `~/.suap/`:

| Arquivo | Conteúdo | Permissão |
|---|---|---|
| `~/.suap/config.json` | URL base e matrícula | `600` |
| `~/.suap/tokens.json` | Access token e refresh token | `600` |

A permissão `600` garante que somente o dono do sistema pode ler ou modificar esses arquivos.

!!! warning "Segurança"
    Nunca compartilhe o conteúdo de `~/.suap/tokens.json`. Os tokens permitem acesso completo à sua conta SUAP enquanto válidos.

---

## Uso sem login prévio (biblioteca)

Ao usar como biblioteca, você pode autenticar diretamente no código sem precisar do `suap login`:

=== "Com credenciais"

    ```python
    from suap_api import SuapClient

    with SuapClient(
        base_url="https://suap.ifpi.edu.br",
        username="20221234",
        password="sua_senha",
    ) as client:
        dados = client.comum.get_my_data()
    ```

=== "Com token JWT"

    ```python
    from suap_api import SuapClient

    with SuapClient(
        base_url="https://suap.ifpi.edu.br",
        token="eyJ0eXAiOiJKV1QiLCJhbGci...",
    ) as client:
        dados = client.comum.get_my_data()
    ```

!!! tip "Credenciais em código"
    Evite hardcodar senhas no código. Use variáveis de ambiente ou arquivos `.env` e nunca commite credenciais em repositórios.

---

## Renovação automática do token

Quando o access token expira (HTTP 401), o cliente tenta renová-lo automaticamente usando o refresh token — sem intervenção do usuário. Se o refresh token também expirou, uma `SuapTokenExpiredError` é levantada com a mensagem:

```
Sessão expirada. Execute `suap login` novamente.
```
