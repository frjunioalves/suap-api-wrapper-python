# RecursoEdu

Recurso do módulo acadêmico da API do SUAP (`/api/edu/`).

Acessado via `client.edu`.

```python
from suap_api import SuapClient

with SuapClient() as client:
    periodos = client.edu.get_periods()
```

!!! tip "JSON original"
    Todo objeto retornado por este recurso expõe `.raw` com o dicionário original da API. Consulte [Acesso ao JSON original](index.md#acesso-ao-json-original) para mais detalhes.

---

## Métodos

### `get_periods()`

Lista os semestres letivos do aluno.

**Endpoint:** `GET /api/edu/periodos`

**Retorno:** `list[Periodo]`

| Atributo | Tipo |
|---|---|
| `semestre` | `str` |
| `situacao` | `str` |

```python
periodos = client.edu.get_periods()
print(periodos[0].semestre)  # "2024.2"
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

**Retorno:** `list[Diario]`

| Atributo | Tipo |
|---|---|
| `id` | `int` |
| `disciplina` | `str` |
| `componente_curricular` | `str` |
| `situacao` | `str` |

```python
diarios = client.edu.get_diaries("2024.1")
id_diario = diarios[0].id
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

**Retorno:** `list[Professor]`

| Atributo | Tipo |
|---|---|
| `nome` | `str` |
| `email` | `str` |

```python
professores = client.edu.get_diary_professors(42)
print(professores[0].nome)
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

**Retorno:** `list[Aula]`

| Atributo | Tipo |
|---|---|
| `data` | `str` |
| `quantidade` | `int` |
| `conteudo` | `str` |
| `faltas` | `int` |

```python
aulas = client.edu.get_diary_classes(42)
print(aulas[0].data, aulas[0].faltas)
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

**Retorno:** `list[Material]`

| Atributo | Tipo |
|---|---|
| `id` | `int` |
| `titulo` | `str` |
| `tipo` | `str` |
| `data_publicacao` | `str` |
| `descricao` | `str` |

```python
materiais = client.edu.get_diary_materials(42)
id_material = materiais[0].id
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

**Retorno:** `Material`

```python
material = client.edu.get_material(10)
print(material.titulo)
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

**Retorno:** `list[Trabalho]`

| Atributo | Tipo |
|---|---|
| `id` | `int` |
| `titulo` | `str` |
| `descricao` | `str` |
| `data_entrega` | `str` |

```python
trabalhos = client.edu.get_diary_assignments(42)
print(trabalhos[0].titulo)
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

**Retorno:** `list[Disciplina]`

| Atributo | Tipo |
|---|---|
| `disciplina` | `str` |
| `nota_etapa_1` | `Any` |
| `nota_etapa_2` | `Any` |
| `media` | `Any` |
| `faltas` | `int` |
| `situacao` | `str` |

```python
disciplinas = client.edu.get_disciplines("2024.1")
for d in disciplinas:
    print(d.disciplina, d.situacao)

# Acesso ao JSON original, inclusive notas aninhadas
print(disciplinas[0].raw)
print(disciplinas[0].notas[0].raw)
```

**Exceções:** `SuapNotFoundError`, `SuapConnectionError`

---

### `get_student_data()`

Obtém os dados acadêmicos do aluno com foco no curso.

**Endpoint:** `GET /api/edu/meus-dados-aluno/`

**Retorno:** `DadosAcademicos`

| Atributo | Tipo |
|---|---|
| `curso` | `str` |
| `turma` | `str` |
| `situacao` | `str` |

```python
dados = client.edu.get_student_data()
print(dados.curso)
```

**Exceções:** `SuapNotLoggedInError`, `SuapTokenExpiredError`, `SuapConnectionError`

---

### `get_graduation_requirements()`

Obtém os requisitos de conclusão do curso.

**Endpoint:** `GET /api/edu/requisitos-conclusao/`

**Retorno:** `RequisitosConclusao`

| Atributo | Tipo |
|---|---|
| `ch_total` | `int` |
| `ch_cumprida` | `int` |
| `pendencias` | `Any` |

```python
conclusao = client.edu.get_graduation_requirements()
print(conclusao.ch_total)
```

**Exceções:** `SuapNotLoggedInError`, `SuapTokenExpiredError`, `SuapConnectionError`
