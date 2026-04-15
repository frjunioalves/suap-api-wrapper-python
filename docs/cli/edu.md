# CLI — Módulo Edu

Comandos relacionados à vida acadêmica: semestres, diários, aulas, materiais, trabalhos e notas.

---

## `suap periodos`

Lista os semestres letivos do aluno.

```bash
suap periodos
```

**Exemplo de saída:**

```json
[
  { "semestre": "2024.2", "situacao": "Em andamento" },
  { "semestre": "2024.1", "situacao": "Encerrado" },
  { "semestre": "2023.2", "situacao": "Encerrado" }
]
```

---

## `suap diarios <semestre>`

Lista os diários do aluno em um semestre letivo.

```bash
suap diarios 2024.1
```

**Exemplo de saída:**

```json
[
  {
    "id": 42,
    "disciplina": "Algoritmos e Estruturas de Dados",
    "componente_curricular": "AED",
    "situacao": "Aprovado"
  },
  {
    "id": 43,
    "disciplina": "Banco de Dados",
    "componente_curricular": "BD",
    "situacao": "Aprovado"
  }
]
```

!!! tip
    Anote o campo `id` de cada diário — ele é necessário para os comandos `aulas`, `materiais`, `trabalhos` e `professores`.

---

## `suap disciplinas <semestre>`

Lista as disciplinas com notas por etapa, faltas e situação final.

```bash
suap disciplinas 2024.1
```

**Exemplo de saída:**

```json
[
  {
    "disciplina": "Algoritmos e Estruturas de Dados",
    "nota_etapa_1": 8.5,
    "nota_etapa_2": 9.0,
    "media": 8.75,
    "faltas": 4,
    "situacao": "Aprovado"
  }
]
```

---

## `suap dados-aluno`

Exibe os dados acadêmicos do aluno: curso, turma, situação de matrícula.

```bash
suap dados-aluno
```

---

## `suap conclusao`

Exibe os requisitos de conclusão do curso: carga horária total exigida, cumprida e componentes pendentes.

```bash
suap conclusao
```

---

## `suap professores <id_diario>`

Lista os professores de um diário.

```bash
suap professores 42
```

**Exemplo de saída:**

```json
[
  {
    "nome": "Prof. Maria Oliveira",
    "email": "maria.oliveira@ifpi.edu.br"
  }
]
```

---

## `suap aulas <id_diario>`

Lista as aulas registradas em um diário com data, conteúdo e faltas.

```bash
suap aulas 42
```

**Exemplo de saída:**

```json
[
  {
    "data": "2024-03-04",
    "quantidade": 2,
    "conteudo": "Introdução a listas encadeadas",
    "faltas": 0
  }
]
```

---

## `suap materiais <id_diario>`

Lista os materiais disponíveis em um diário.

```bash
suap materiais 42
```

**Exemplo de saída:**

```json
[
  { "id": 10, "titulo": "Aula 01 - Listas", "tipo": "PDF" },
  { "id": 11, "titulo": "Aula 02 - Pilhas", "tipo": "PDF" }
]
```

!!! tip
    Anote o campo `id` do material para usar com `suap material` e `suap material-pdf`.

---

## `suap material <id_material>`

Exibe os detalhes de um material específico.

```bash
suap material 10
```

**Exemplo de saída:**

```json
{
  "id": 10,
  "titulo": "Aula 01 - Listas",
  "tipo": "PDF",
  "data_publicacao": "2024-03-05",
  "descricao": "Slides da primeira aula sobre listas encadeadas."
}
```

---

## `suap material-pdf <id_diario> <id_material>`

Baixa o PDF de um material e imprime o caminho do arquivo temporário criado.

```bash
suap material-pdf 42 10
```

**Saída:**

```
/tmp/suap_material_10_abc123.pdf
```

!!! tip "Abrir automaticamente"
    No Linux, combine com `xdg-open` para abrir o PDF direto:

    ```bash
    xdg-open $(suap material-pdf 42 10)
    ```

---

## `suap trabalhos <id_diario>`

Lista os trabalhos de um diário com título, descrição e prazo.

```bash
suap trabalhos 42
```

**Exemplo de saída:**

```json
[
  {
    "id": 5,
    "titulo": "Lista de Exercícios 1",
    "descricao": "Implemente uma lista encadeada simples.",
    "data_entrega": "2024-03-15"
  }
]
```
