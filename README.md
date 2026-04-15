# suap-api-wrapper 🎓

![PyPI](https://img.shields.io/pypi/v/suap-api-wrapper)
![Python](https://img.shields.io/pypi/pyversions/suap-api-wrapper)
![License](https://img.shields.io/pypi/l/suap-api-wrapper)
![Downloads](https://img.shields.io/pypi/dm/suap-api-wrapper)

CLI e biblioteca Python para interagir com a API v2 do SUAP. Funciona com qualquer instituição que utilize o SUAP (IFPI, IFRN, IFCE, etc.), basta informar a URL da sua instância no login.

📚 **[Documentação completa](https://frjunioalves.github.io/suap-api-wrapper-python)**

---

## ⚙️ Requisitos

- Python 3.8+
- pip

---

## 📦 Instalação

Instale diretamente do PyPI:

```bash
pip install suap-api-wrapper
```

Após a instalação, o comando `suap` estará disponível no terminal.

Para instalar a partir do código-fonte:

```bash
git clone https://github.com/Junio-Alves/suap-api-wrapper.git
cd suap-api-wrapper
pip install .
```

Para instalar também as dependências de desenvolvimento (testes, mypy):

```bash
pip install ".[dev]"
```

---

## 🖥️ Uso da CLI

### Login

```bash
suap login
```

Você será solicitado a informar:

1. **URL da instância** — a URL completa do seu SUAP. Formatos aceitos:
   - `https://suap.ifpi.edu.br`
   - `suap.ifpi.edu.br` (o `https://` é adicionado automaticamente)
2. **Matrícula**
3. **Senha** — ocultada durante a digitação

Os tokens JWT são salvos em `~/.suap/tokens.json` com permissão restrita (`600`). A URL e a matrícula são salvas em `~/.suap/config.json`, também com permissão `600`.

---

### Logout

```bash
suap logout
```

Remove os tokens do `keyring` e apaga o arquivo de configuração.

---

### Dados pessoais

```bash
suap meus-dados
```

---

### Períodos letivos

```bash
suap periodos
```

---

### Diários de um semestre

```bash
suap diarios <semestre>
```

Exemplo:

```bash
suap diarios 2024.1
```

---

### Professores de um diário

```bash
suap professores <id_diario>
```

---

### Aulas de um diário

```bash
suap aulas <id_diario>
```

---

### Materiais de um diário

```bash
suap materiais <id_diario>
```

---

### Detalhes de um material

```bash
suap material <id_material>
```

---

### Baixar PDF de um material

```bash
suap material-pdf <id_diario> <id_material>
```

Salva o PDF em um arquivo temporário e imprime o caminho. Exemplo:

```bash
suap material-pdf 42 10
# /tmp/suap_material_10_abc123.pdf
```

---

### Trabalhos de um diário

```bash
suap trabalhos <id_diario>
```

---

### Disciplinas de um semestre

```bash
suap disciplinas <semestre>
```

Exemplo:

```bash
suap disciplinas 2024.1
```

---

### Dados acadêmicos do aluno

```bash
suap dados-aluno
```

---

### Requisitos de conclusão do curso

```bash
suap conclusao
```

---

## 🚀 Fluxo típico de uso

```bash
# 1. Login
suap login

# 2. Ver os semestres disponíveis
suap periodos

# 3. Listar os diários de um semestre
suap diarios 2024.1

# 4. Com o ID de um diário, ver aulas, materiais e trabalhos
suap aulas 42
suap materiais 42
suap trabalhos 42

# 5. Baixar o PDF de um material
suap material-pdf 42 10 -o aula1.pdf
```

---

## 🐍 Uso como biblioteca

```python
from suap_api import SuapClient

with SuapClient() as client:
    dados = client.get_my_data()
    periodos = client.get_periods()

    diarios = client.get_diaries("2024.1")
    if diarios:
        id_diario = diarios[0]["id"]
        aulas = client.get_diary_classes(id_diario)
        materiais = client.get_diary_materials(id_diario)
        trabalhos = client.get_diary_assignments(id_diario)

        # Baixar PDF de um material (retorna bytes)
        if materiais:
            pdf_bytes = client.get_material_pdf(id_diario, materiais[0]["id"])
            # use os bytes como quiser: salvar, exibir, enviar, etc.

    dados_aluno = client.get_student_data()
    conclusao = client.get_graduation_requirements()
```

Para uso sem sessão salva (passando credenciais diretamente no código):

```python
from suap_api import SuapClient

with SuapClient(
    base_url="https://suap.ifpi.edu.br",
    username="20221234",
    password="sua_senha",
) as client:
    dados = client.comum.get_my_data()
```

---

## ⚠️ Tratamento de erros

Todas as exceções herdam de `SuapError`:

| Exceção | Quando ocorre |
|---|---|
| `SuapAuthError` | Matrícula ou senha incorretos |
| `SuapConnectionError` | Falha de rede, URL errada, timeout, SSL |
| `SuapTokenExpiredError` | Sessão expirada (refresh falhou) |
| `SuapNotLoggedInError` | Nenhuma sessão encontrada |
| `SuapValidationError` | Parâmetro inválido enviado à API (HTTP 422) |
| `SuapNotFoundError` | Recurso não encontrado (HTTP 404) |
| `SuapForbiddenError` | Sem permissão de acesso (HTTP 403) |
| `SuapServerError` | Erro interno do servidor SUAP (HTTP 5xx) |
| `SuapRequestError` | Outros erros HTTP |

```python
from suap_api import SuapClient, SuapNotFoundError, SuapValidationError

try:
    with SuapClient() as client:
        aulas = client.get_diary_classes(99999)
except SuapNotFoundError:
    print("Diário não encontrado.")
except SuapValidationError as e:
    print(f"Parâmetro inválido: {e}")
```

---

## 🛠️ Desenvolvimento

### Rodando os testes

```bash
pytest tests/ -v
```

### Checagem de tipos

```bash
mypy suap_api/
```

---

## 📁 Estrutura do projeto

```
suap-api-wrapper/
├── suap_api/
│   ├── __init__.py       # exports públicos
│   ├── client.py         # SuapClient
│   ├── cli.py            # comandos Click
│   ├── config.py         # gestão de configuração (~/.suap/)
│   └── exceptions.py     # exceções customizadas
├── tests/
│   ├── test_client.py
│   ├── test_cli.py
│   └── test_config.py
├── docs/
│   └── plan.md
└── pyproject.toml
```

---

## 🔒 Segurança

- Os tokens JWT são armazenados em `~/.suap/tokens.json` com permissão `600` (somente o dono pode ler/escrever).
- O arquivo `~/.suap/config.json` é criado com permissão `600` (somente o dono pode ler/escrever).
- SSL é sempre verificado. Não há opção para desativá-lo.
- Todas as requisições têm timeout de 10 segundos.

---

## 📄 Licença

Distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 👤 Autor

**Junio Alves** — [frjunioalves@hotmail.com](mailto:frjunioalves@hotmail.com) — [github.com/Junio-Alves](https://github.com/Junio-Alves)

Contribuições, issues e pull requests são bem-vindos!

---

Copyright (c) 2026 Junio Alves — licenciado sob a [MIT License](LICENSE).
