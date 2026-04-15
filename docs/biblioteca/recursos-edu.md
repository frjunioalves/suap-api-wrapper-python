# RecursoEdu

Recurso do módulo acadêmico da API do SUAP (`/api/edu/`).

Acessado via `client.edu`.

```python
from suap_api import SuapClient

with SuapClient() as client:
    periodos = client.edu.get_periods()
```

---

## Métodos

### `get_periods()`

Lista os semestres letivos do aluno.

**Endpoint:** `GET /api/edu/periodos`

**Retorno:** `list`

```python
periodos = client.edu.get_periods()
# [{"semestre": "2024.2", ...}, {"semestre": "2024.1", ...}]
```

**Exceções:** `SuapNotLoggedInError`, `SuapTokenExpiredError`, `SuapConnectionError`

---

### `get_diaries(semestre)`

Lista os diários do aluno em um semestre letivo.

**Endpoint:** `GET /api/edu/diarios/{semestre}`

**Parâmetros:**

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `semestre` | `str` | Semestre no formato `"AAAA.P"` (ex: `"2024.1"`) |

**Retorno:** `list` — cada item contém `id`, `disciplina`, `situacao` e outros campos.

```python
diarios = client.edu.get_diaries("2024.1")
id_diario = diarios[0]["id"]
```

**Exceções:** `SuapNotLoggedInError`, `SuapNotFoundError`, `SuapConnectionError`

---

### `get_diary_professors(id_diario)`

Lista os professores de um diário.

**Endpoint:** `GET /api/edu/diarios/{id_diario}/professores`

**Parâmetros:**

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `id_diario` | `int` | ID do diário, obtido via `get_diaries()` |

**Retorno:** `list`

```python
professores = client.edu.get_diary_professors(42)
```

**Exceções:** `SuapNotFoundError`, `SuapValidationError`, `SuapConnectionError`

---

### `get_diary_classes(id_diario)`

Lista as aulas registradas em um diário.

**Endpoint:** `GET /api/edu/diarios/{id_diario}/aulas`

**Parâmetros:**

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `id_diario` | `int` | ID do diário, obtido via `get_diaries()` |

**Retorno:** `list` — cada item contém `data`, `quantidade`, `conteudo` e `faltas`.

```python
aulas = client.edu.get_diary_classes(42)
```

**Exceções:** `SuapNotFoundError`, `SuapValidationError`, `SuapConnectionError`

---

### `get_diary_materials(id_diario)`

Lista os materiais disponíveis em um diário.

**Endpoint:** `GET /api/edu/diarios/{id_diario}/materiais`

**Parâmetros:**

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `id_diario` | `int` | ID do diário, obtido via `get_diaries()` |

**Retorno:** `list` — cada item contém `id`, `titulo` e `tipo`.

```python
materiais = client.edu.get_diary_materials(42)
id_material = materiais[0]["id"]
```

**Exceções:** `SuapNotFoundError`, `SuapValidationError`, `SuapConnectionError`

---

### `get_material(id_material)`

Obtém os detalhes de um material específico.

**Endpoint:** `GET /api/edu/materiais/{id_material}`

**Parâmetros:**

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `id_material` | `int` | ID do material, obtido via `get_diary_materials()` |

**Retorno:** `dict`

```python
material = client.edu.get_material(10)
print(material["titulo"])
```

**Exceções:** `SuapNotFoundError`, `SuapValidationError`, `SuapConnectionError`

---

### `get_material_pdf(id_diario, id_material)`

Baixa o conteúdo binário de um material em PDF.

**Endpoint:** `GET /api/edu/materiais/{id_diario}/{id_material}/pdf/`

**Parâmetros:**

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `id_diario` | `int` | ID do diário ao qual o material pertence |
| `id_material` | `int` | ID do material |

**Retorno:** `bytes` — conteúdo binário do PDF.

```python
pdf_bytes = client.edu.get_material_pdf(42, 10)

# Salvar em arquivo
with open("aula.pdf", "wb") as f:
    f.write(pdf_bytes)
```

**Exceções:** `SuapNotFoundError`, `SuapValidationError`, `SuapConnectionError`

---

### `get_diary_assignments(id_diario)`

Lista os trabalhos de um diário.

**Endpoint:** `GET /api/edu/diarios/{id_diario}/trabalhos`

**Parâmetros:**

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `id_diario` | `int` | ID do diário, obtido via `get_diaries()` |

**Retorno:** `list` — cada item contém `titulo`, `descricao` e `data_entrega`.

```python
trabalhos = client.edu.get_diary_assignments(42)
```

**Exceções:** `SuapNotFoundError`, `SuapValidationError`, `SuapConnectionError`

---

### `get_disciplines(semestre)`

Lista as disciplinas com notas, faltas e situação final.

**Endpoint:** `GET /api/edu/disciplinas/{semestre}`

**Parâmetros:**

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `semestre` | `str` | Semestre no formato `"AAAA.P"` (ex: `"2024.1"`) |

**Retorno:** `list`

```python
disciplinas = client.edu.get_disciplines("2024.1")
for d in disciplinas:
    print(d["disciplina"], d["situacao"])
```

**Exceções:** `SuapNotFoundError`, `SuapConnectionError`

---

### `get_student_data()`

Obtém os dados acadêmicos do aluno com foco no curso.

**Endpoint:** `GET /api/edu/meus-dados-aluno/`

**Retorno:** `dict` — curso, turma, situação de matrícula.

```python
dados = client.edu.get_student_data()
print(dados["curso"])
```

**Exceções:** `SuapNotLoggedInError`, `SuapTokenExpiredError`, `SuapConnectionError`

---

### `get_graduation_requirements()`

Obtém os requisitos de conclusão do curso.

**Endpoint:** `GET /api/edu/requisitos-conclusao/`

**Retorno:** `dict` — carga horária total exigida, cumprida, componentes pendentes.

```python
conclusao = client.edu.get_graduation_requirements()
print(conclusao["ch_total"])
```

**Exceções:** `SuapNotLoggedInError`, `SuapTokenExpiredError`, `SuapConnectionError`
