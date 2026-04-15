# suap-api-wrapper

**CLI e biblioteca Python para interagir com a API v2 do SUAP.**

Funciona com qualquer instituição que utilize o SUAP — IFPI, IFRN, IFCE e outras.
Basta informar a URL da sua instância no primeiro login.

---

<div class="grid cards" markdown>

-   **📥 Instalação**

    ---

    Instale via pip ou diretamente do repositório.

    [→ Instalação](instalacao.md)

-   **🔑 Autenticação**

    ---

    Como o login, tokens e refresh automático funcionam.

    [→ Autenticação](autenticacao.md)

-   **💻 CLI**

    ---

    Acesse o SUAP direto do terminal com `suap <comando>`.

    [→ CLI](cli/index.md)

-   **🐍 Biblioteca Python**

    ---

    Integre dados do SUAP em scripts, bots ou aplicações.

    [→ Biblioteca Python](biblioteca/index.md)

-   **⚠️ Exceções**

    ---

    Referência de todas as exceções lançadas pelo wrapper.

    [→ Exceções](excecoes.md)

-   **🔒 Segurança**

    ---

    Boas práticas para proteger suas credenciais e tokens.

    [→ Segurança](seguranca.md)

-   **🤝 Contribuindo**

    ---

    Como contribuir com o projeto, abrir issues e enviar PRs.

    [→ Contribuindo](contribuindo.md)

</div>

---

## Quick start

### 1. Instale

```bash
git clone https://github.com/Junio-Alves/suap-api-wrapper.git
cd suap-api-wrapper
pip install .
```

### 2. Faça login

```bash
suap login
```

Você será solicitado a informar a URL do seu SUAP, matrícula e senha.

### 3. Use

=== "CLI"

    ```bash
    # Ver seus dados pessoais
    suap meus-dados

    # Listar semestres
    suap periodos

    # Listar diários de um semestre
    suap diarios 2024.1

    # Ver aulas de um diário (use o ID retornado acima)
    suap aulas 42
    ```

=== "Biblioteca Python"

    ```python
    from suap_api import SuapClient

    with SuapClient() as client:
        dados = client.comum.get_my_data()
        periodos = client.edu.get_periods()
        diarios = client.edu.get_diaries("2024.1")

        if diarios:
            id_diario = diarios[0]["id"]
            aulas = client.edu.get_diary_classes(id_diario)
    ```

---

## Compatibilidade

Qualquer instituição que utilize o SUAP. Formatos de URL aceitos no login:

| Formato digitado | Resultado |
|---|---|
| `suap.ifpi.edu.br` | `https://suap.ifpi.edu.br` |
| `https://suap.ifpi.edu.br/` | `https://suap.ifpi.edu.br` |
| `https://suap.ifpi.edu.br/api/v2` | `https://suap.ifpi.edu.br` |
