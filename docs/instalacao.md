# Instalação

## Requisitos

- Python **3.8** ou superior
- pip

---

## Instalação via PyPI (recomendado)

```bash
pip install suap-api-wrapper
```

Após a instalação, o comando `suap` estará disponível no terminal:

```bash
suap --help
```

---

## Instalação a partir do código-fonte

Clone o repositório e instale o pacote:

```bash
git clone https://github.com/Junio-Alves/suap-api-wrapper.git
cd suap-api-wrapper
pip install .
```

---

## Dependências

O pacote instala automaticamente:

| Dependência | Versão mínima | Uso |
|---|---|---|
| `requests` | 2.28 | Requisições HTTP à API |
| `click` | 8.0 | Interface de linha de comando |

---

## Instalação para desenvolvimento

Para instalar também as ferramentas de teste e checagem de tipos:

```bash
pip install ".[dev]"
```

Inclui: `pytest`, `responses`, `mypy` e `types-requests`.

---

## Instalação para documentação

Para instalar as dependências de build da documentação:

```bash
pip install ".[docs]"
```

Inclui: `mkdocs`, `mkdocs-material` e `pymdown-extensions`.

Para visualizar a documentação localmente:

```bash
mkdocs serve
```

---

## Verificando a instalação

```bash
suap --help
```

Saída esperada:

```
Usage: suap [OPTIONS] COMMAND [ARGS]...

  SUAP API CLI — acesse o SUAP pela linha de comando.

Options:
  --help  Show this message and exit.

Commands:
  aulas        Lista as aulas de um diario.
  conclusao    Exibe os requisitos de conclusao do curso.
  dados-aluno  Exibe os dados academicos do aluno (curso, situacao, etc).
  diarios      Lista os diarios do aluno em um semestre.
  disciplinas  Lista as disciplinas do aluno em um semestre.
  login        Realiza login no SUAP.
  logout       Encerra a sessao atual.
  material     Exibe um material especifico.
  material-pdf Baixa o PDF de um material em arquivo temporario.
  materiais    Lista os materiais de um diario.
  meus-dados   Exibe os dados pessoais do usuario logado.
  periodos     Lista os semestres letivos do aluno.
  professores  Lista os professores de um diario.
  trabalhos    Lista os trabalhos de um diario.
```
